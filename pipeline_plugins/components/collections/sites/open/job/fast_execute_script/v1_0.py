# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
# 作业平台任务状态参照表
TASK_RESULT = [
    (0, '状态未知'),
    (1, '未执行'),
    (2, '正在执行'),
    (3, '执行成功'),
    (4, '执行失败'),
    (5, '跳过'),
    (6, '忽略错误'),
    (7, '等待用户'),
    (8, '手动结束'),
    (9, '状态异常'),
    (10, '步骤强制终止中'),
    (11, '步骤强制终止成功'),
    (12, '步骤强制终止失败'),
    (-1, '接口调用失败'),
]
"""

import base64
from functools import partial

from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from gcloud.utils.ip import get_ip_by_regex
from pipeline.core.flow.io import (
    StringItemSchema,
    ObjectItemSchema,
    BooleanItemSchema,
)
from pipeline.component_framework.component import Component
from pipeline_plugins.components.collections.sites.open.job import JobService
from pipeline_plugins.components.utils import (
    cc_get_ips_info_by_str,
    get_job_instance_url,
    get_node_callback_url,
)
from gcloud.conf import settings
from gcloud.utils.handlers import handle_api_error

__group_name__ = _("作业平台(JOB)")

from pipeline_plugins.components.utils.sites.open.utils import plat_ip_reg

get_client_by_user = settings.ESB_GET_CLIENT_BY_USER

job_handle_api_error = partial(handle_api_error, __group_name__)


class JobFastExecuteScriptService(JobService):
    need_get_sops_var = True

    def inputs_format(self):
        return [
            self.InputItem(
                name=_("业务 ID"),
                key="biz_cc_id",
                type="string",
                schema=StringItemSchema(description=_("当前操作所属的 CMDB 业务 ID")),
            ),
            self.InputItem(
                name=_("脚本来源"),
                key="job_script_source",
                type="string",
                schema=StringItemSchema(
                    description=_("待执行的脚本来源，手动(manual)，业务脚本(general)，公共脚本(public)"),
                    enum=["manual", "general", "public"],
                ),
            ),
            self.InputItem(
                name=_("脚本类型"),
                key="job_script_type",
                type="string",
                schema=StringItemSchema(
                    description=_("待执行的脚本类型：shell(1) bat(2) perl(3) python(4) powershell(5)" "，仅在脚本来源为手动时生效"),
                    enum=["1", "2", "3", "4", "5"],
                ),
            ),
            self.InputItem(
                name=_("脚本内容"),
                key="job_content",
                type="string",
                schema=StringItemSchema(description=_("待执行的脚本内容，仅在脚本来源为手动时生效")),
            ),
            self.InputItem(
                name=_("公共脚本"),
                key="job_script_list_public",
                type="string",
                schema=StringItemSchema(description=_("待执行的公共脚本 ID，仅在脚本来源为公共脚本时生效")),
            ),
            self.InputItem(
                name=_("业务脚本"),
                key="job_script_list_general",
                type="string",
                schema=StringItemSchema(description=_("待执行的业务脚本 ID，仅在脚本来源为业务脚本时生效")),
            ),
            self.InputItem(
                name=_("脚本执行参数"),
                key="job_script_param",
                type="string",
                schema=StringItemSchema(description=_("脚本执行参数")),
            ),
            self.InputItem(
                name=_("是否允许跨业务"),
                key="job_across_biz",
                type="bool",
                schema=BooleanItemSchema(description=_("是否允许跨业务(跨业务需在作业平台添加白名单)，允许时，源文件IP格式需为【云区域ID:IP】")),
            ),
            self.InputItem(
                name=_("目标 IP"),
                key="job_ip_list",
                type="string",
                schema=StringItemSchema(description=_("执行脚本的目标机器 IP，多个用英文逗号 `,` 分隔")),
            ),
            self.InputItem(
                name=_("目标账户"), key="job_account", type="string", schema=StringItemSchema(description=_("执行脚本的目标机器账户")),
            ),
            self.InputItem(
                name=_("IP 存在性校验"),
                key="ip_is_exist",
                type="string",
                schema=BooleanItemSchema(description=_("是否做 IP 存在性校验，如果ip校验开关打开，校验通过的ip数量若减少，即返回错误")),
            ),
        ]

    def outputs_format(self):
        return super(JobFastExecuteScriptService, self).outputs_format() + [
            self.OutputItem(
                name=_("JOB全局变量"),
                key="log_outputs",
                type="dict",
                schema=ObjectItemSchema(
                    description=_("输出日志中提取的全局变量"),
                    property_schemas={
                        "name": StringItemSchema(description=_("全局变量名称")),
                        "value": StringItemSchema(description=_("全局变量值")),
                    },
                ),
            ),
        ]

    def execute(self, data, parent_data):
        executor = parent_data.get_one_of_inputs("executor")
        client = get_client_by_user(executor)
        if parent_data.get_one_of_inputs("language"):
            setattr(client, "language", parent_data.get_one_of_inputs("language"))
            translation.activate(parent_data.get_one_of_inputs("language"))
        biz_cc_id = data.get_one_of_inputs("biz_cc_id", parent_data.inputs.biz_cc_id)
        script_source = data.get_one_of_inputs("job_script_source")
        across_biz = data.get_one_of_inputs("job_across_biz", False)
        original_ip_list = data.get_one_of_inputs("job_ip_list")
        ip_is_exist = data.get_one_of_inputs("ip_is_exist")

        if across_biz:
            ip_info = {"ip_result": []}
            for match in plat_ip_reg.finditer(original_ip_list):
                if not match:
                    continue
                ip_str = match.group()
                cloud_id, inner_ip = ip_str.split(":")
                ip_info["ip_result"].append({"InnerIP": inner_ip, "Source": cloud_id})
        else:
            ip_info = cc_get_ips_info_by_str(
                username=executor, biz_cc_id=biz_cc_id, ip_str=original_ip_list, use_cache=False,
            )
        ip_list = [{"ip": _ip["InnerIP"], "bk_cloud_id": _ip["Source"]} for _ip in ip_info["ip_result"]]

        if ip_is_exist and not across_biz:
            # 如果ip校验开关打开且不允许跨业务，校验通过的ip数量减少，返回错误
            input_ip_set = set(get_ip_by_regex(original_ip_list))
            self.logger.info("from cmdb get valid ip list:{}, user input ip list:{}".format(ip_list, input_ip_set))
            difference_ip_list = input_ip_set.difference(set([ip_item["ip"] for ip_item in ip_list]))

            if len(ip_list) != len(input_ip_set):
                data.outputs.ex_data = _("IP 校验失败，请确认输入的 IP {} 是否合法".format(",".join(difference_ip_list)))
                return False

        job_kwargs = {
            "bk_biz_id": biz_cc_id,
            "script_timeout": data.get_one_of_inputs("job_script_timeout"),
            "account": data.get_one_of_inputs("job_account"),
            "ip_list": ip_list,
            "bk_callback_url": get_node_callback_url(self.id, getattr(self, "version", "")),
        }

        script_param = str(data.get_one_of_inputs("job_script_param"))

        if script_param:
            job_kwargs.update({"script_param": base64.b64encode(script_param.encode("utf-8")).decode("utf-8")})

        if script_source in ["general", "public"]:
            script_name = data.get_one_of_inputs("job_script_list_{}".format(script_source))
            kwargs = {"script_name": script_name}
            if script_source == "general":
                kwargs.update({"bk_biz_id": biz_cc_id})
                scripts = client.job.get_script_list(kwargs)
            else:
                scripts = client.job.get_public_script_list(kwargs)

            if scripts["result"] is False:
                api_name = "job.get_script_list" if script_source == "general" else "job.get_public_script_list"
                message = job_handle_api_error(api_name, job_kwargs, scripts)
                self.logger.error(message)
                data.outputs.ex_data = message
                return False

            # job V2接口使用的是模糊匹配，这里需要做一次精确匹配
            script_list = scripts["data"]["data"]
            selected_script = None
            for script in script_list:
                if script["name"] == script_name:
                    selected_script = script
                    break

            if not selected_script:
                api_name = "job.get_script_list" if script_source == "general" else "job.get_public_script_list"
                message = job_handle_api_error(api_name, job_kwargs, scripts)
                message += "Data validation error: can not find a script exactly named {}".format(script_name)
                self.logger.error(message)
                data.outputs.ex_data = message
                return False

            script_id = selected_script["id"]
            job_kwargs.update({"script_id": script_id})
        else:
            job_kwargs.update(
                {
                    "script_type": data.get_one_of_inputs("job_script_type"),
                    "script_content": base64.b64encode(data.get_one_of_inputs("job_content").encode("utf-8")).decode(
                        "utf-8"
                    ),
                }
            )
        job_result = client.job.fast_execute_script(job_kwargs)
        self.logger.info("job_result: {result}, job_kwargs: {kwargs}".format(result=job_result, kwargs=job_kwargs))
        if job_result["result"]:
            job_instance_id = job_result["data"]["job_instance_id"]
            data.outputs.job_inst_id = job_instance_id
            data.outputs.job_inst_name = job_result["data"]["job_instance_name"]
            data.outputs.job_inst_url = get_job_instance_url(biz_cc_id, job_instance_id)
            data.outputs.client = client
            return True
        else:
            message = job_handle_api_error("job.fast_execute_script", job_kwargs, job_result)
            self.logger.error(message)
            data.outputs.ex_data = message
            return False

    def schedule(self, data, parent_data, callback_data=None):
        return super(JobFastExecuteScriptService, self).schedule(data, parent_data, callback_data)


class JobFastExecuteScriptComponent(Component):
    name = _("快速执行脚本")
    code = "job_fast_execute_script"
    bound_service = JobFastExecuteScriptService
    version = "v1.0"
    form = "%scomponents/atoms/job/fast_execute_script/v1_0.js" % settings.STATIC_URL
    desc = (
        "插件版本legacy会依据脚本id来执行脚本，JOB平台脚本上线版本变动仍执行原来脚本。\n"
        "插件版本v1.0会依据脚本名称来执行脚本，自动同步JOB平台当前上线版本进行执行。\n"
        "注：插件版本v1.0中跨业务执行脚本时需要在作业平台添加白名单"
    )
