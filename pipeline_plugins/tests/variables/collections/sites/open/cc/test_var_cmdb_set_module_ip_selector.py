# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2020 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from unittest.mock import call

from django.test import TestCase
from mock import MagicMock, patch

from pipeline_plugins.variables.collections.sites.open.cmdb.var_cmdb_set_module_ip_selector import SetModuleIpSelector

GET_CLIENT_BY_USER = "pipeline_plugins.variables.utils.get_client_by_user"
CC_GET_IPS_INFO_BY_STR = (
    "pipeline_plugins.variables.collections.sites.open.cmdb." "var_cmdb_set_module_ip_selector.cc_get_ips_info_by_str"
)
CMDB_API_FUNC_PREFIX = "pipeline_plugins.variables.utils"
LIST_BIZ_HOSTS = "{}.list_biz_hosts".format(CMDB_API_FUNC_PREFIX)
FIND_MODULE_WITH_RELATION = "{}.find_module_with_relation".format(CMDB_API_FUNC_PREFIX)
GET_SERVICE_TEMPLATE_LIST = "{}.get_service_template_list".format(CMDB_API_FUNC_PREFIX)
GET_SET_LIST = "{}.get_set_list".format(CMDB_API_FUNC_PREFIX)
GET_MODULE_LIST = "{}.get_module_list".format(CMDB_API_FUNC_PREFIX)


class MockClient(object):
    def __init__(
            self,
            search_set_return=None,
            list_biz_hosts_topo_return=None,
            find_module_with_relation_return=None,
            list_biz_hosts_return=None,
            list_service_template_return=None,
            find_module_batch_return=None,
            get_biz_internal_module_return=None
    ):
        self.cc = MagicMock()
        self.cc.list_biz_hosts_topo = MagicMock(return_value=list_biz_hosts_topo_return)
        self.cc.find_module_with_relation = MagicMock(return_value=find_module_with_relation_return)
        self.cc.list_biz_hosts = MagicMock(return_value=list_biz_hosts_return)
        self.cc.search_set = MagicMock(return_value=search_set_return)
        self.cc.list_service_template = MagicMock(return_value=list_service_template_return)
        self.cc.find_module_batch = MagicMock(return_value=find_module_batch_return)
        self.cc.get_biz_internal_module = MagicMock(return_value=get_biz_internal_module_return)


mock_project_obj = MagicMock()
mock_project = MagicMock()
mock_project.objects.get = MagicMock(return_value=mock_project_obj)

SELECT_METHOD_SUC_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)

IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_HAS_FILTER_SET_MODULUE_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)

IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_SET_MODULE_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)

IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_OTHER_SET_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)

IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_OTHER_SET_MODULE_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)

IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_NO_MODULUE_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)

IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)

IP_SELECTOR_SELECT_METHOD_NO_INNER_MODULE_SUCCESS_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)

IP_SELECTOR_SELECT_METHOD_ALL_SELECT_SET_SUCCESS_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)

IP_SELECTOR_SELECT_METHOD_ALL_SELECT_SET_MODULE_SUCCESS_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)

IP_SELECTOR_SELECT_METHOD_ALL_SELECT_MODULE_SUCCESS_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)

MANUAL_METHOD_SUC_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)
CUSTOM_METHOD_SUC_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)

CUSTOM_METHOD_BIZ_INNERIP_SUC_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)

SELECT_METHOD_BIZ_INNERIP_SUC_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)

SELECT_METHOD_FAIL_CLIENT = MockClient(
    list_biz_hosts_return={"result": False, "code": 0, "message": "success", "data": {}},
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)
MANUAL_METHOD_FAIL_CLIENT = MockClient(
    list_biz_hosts_return={"result": False, "code": 0, "message": "success", "data": {}},
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)
CUSTOM_METHOD_FAIL_CLIENT = MockClient(
    list_biz_hosts_return={"result": False, "code": 0, "message": "success", "data": {}},
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)

SELECT_METHOD_BIZ_INNERIP_NO_FILTER_SET_MODULE_SUC_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)
SELECT_METHOD_BIZ_INNERIP_NO_FILTER_SET_MODULE_SELECT_MODULE_SUC_CLIENT = MockClient(
    list_biz_hosts_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "count": 2,
            "info": [
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 1,
                    "bk_host_innerip": "192.168.15.18",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
                {
                    "bk_cloud_id": 0,
                    "bk_host_id": 2,
                    "bk_host_innerip": "192.168.15.4",
                    "bk_mac": "",
                    "bk_os_type": None,
                },
            ],
        },
    },
    list_service_template_return={
        "result": True,
        "code": 0,
        "message": "success",
        "permission": None,
        "data": {"count": 2, "info": [{"id": 51, "name": "test3"}, {"id": 50, "name": "test2"}]},
    },
    search_set_return={
        "result": True,
        "code": 0,
        "message": "",
        "data": {
            "count": 1,
            "info": [
                {"default": 1, "bk_set_id": 30, "bk_set_name": "空闲机池"},
                {"default": 0, "bk_set_id": 31, "bk_set_name": "集群1"},
                {"default": 0, "bk_set_id": 32, "bk_set_name": "集群2"},
                {"default": 0, "bk_set_id": 33, "bk_set_name": "集群3"},
                {"default": 0, "bk_set_id": 34, "bk_set_name": "集群4"},
                {"default": 0, "bk_set_id": 38, "bk_set_name": "集群5"},
                {"default": 0, "bk_set_id": 39, "bk_set_name": "集群6"},
            ],
        },
    },
    find_module_with_relation_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {"count": 2, "info": [{"bk_module_id": 60}, {"bk_module_id": 61}]},
    },
    get_biz_internal_module_return={
        "result": True,
        "code": 0,
        "message": "success",
        "data": {
            "bk_set_id": 2,
            "bk_set_name": "空闲机池",
            "module": [
                {
                    "bk_module_id": 3,
                    "bk_module_name": "空闲机"
                },
                {
                    "bk_module_id": 4,
                    "bk_module_name": "故障机"
                },
                {
                    "bk_module_id": 5,
                    "bk_module_name": "待回收"
                }
            ]
        }
    }
)
CC_GET_IPS_INFO_BY_STR_RETURN = {
    "ip_result": [
        {"InnerIP": "192.168.15.18", "Source": 0},
        {"InnerIP": "192.168.15.4", "Source": 0}
    ]
}

IP_SELECTOR_SELECT_METHOD_SUC_VALUE = {
    "var_ip_method": "select",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["空闲机池", "集群1"], "var_module": ["db"], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "集群1,集群2",
    "var_filter_module": "ls",
}
IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_HAS_FILTER_SET_MODULUE_VALUE = {
    "var_ip_method": "select",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["空闲机池", "集群1"], "var_module": ["空闲机", "db"], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "空闲机池",
    "var_filter_module": "",
}
IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_SET_MODULE_VALUE = {
    "var_ip_method": "select",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["空闲机池", "集群1"], "var_module": ["空闲机", "db"], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "空闲机池",
    "var_filter_module": "空闲机",
}
IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_OTHER_SET_VALUE = {
    "var_ip_method": "select",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["空闲机池", "集群1"], "var_module": ["空闲机", "db"], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "集群1,空闲机池",
    "var_filter_module": "",
}
IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_OTHER_SET_MODULE_VALUE = {
    "var_ip_method": "select",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["空闲机池", "集群1"], "var_module": ["空闲机", "db"], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "集群1,空闲机池",
    "var_filter_module": "空闲机",
}
IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_NO_MODULUE_VALUE = {
    "var_ip_method": "select",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["空闲机池", "集群1"], "var_module": ["db"], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "",
    "var_filter_module": "",
}
IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_VALUE = {
    "var_ip_method": "select",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["空闲机池", "集群1"], "var_module": ["空闲机", "db"], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "",
    "var_filter_module": "",
}
IP_SELECTOR_SELECT_METHOD_NO_INNER_MODULE_SUCCESS_VALUE = {
    "var_ip_method": "select",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["空闲机", "集群1"], "var_module": ["空闲机", "db"], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "集群1,集群2",
    "var_filter_module": "ls",
}

IP_SELECTOR_SELECT_METHOD_ALL_SELECT_SET_SUCCESS_VALUE = {
    "var_ip_method": "select",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["all"], "var_module": ["空闲机", "db"], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "集群1,集群2",
    "var_filter_module": "空闲机",
}

IP_SELECTOR_SELECT_METHOD_ALL_SELECT_SET_MODULE_SUCCESS_VALUE = {
    "var_ip_method": "select",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["all"], "var_module": ["all"], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "集群1,集群2",
    "var_filter_module": "空闲机",
}

IP_SELECTOR_SELECT_METHOD_ALL_SELECT_MODULE_SUCCESS_VALUE = {
    "var_ip_method": "select",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["集群1"], "var_module": ["all"], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "集群1,集群2",
    "var_filter_module": "空闲机",
}

IP_SELECTOR_SELECT_METHOD_FAIL_VALUE = {
    "var_ip_method": "select",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["空闲机池", "集群1"], "var_module": ["db"], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "集群1,集群2",
    "var_filter_module": "ls",
}
IP_SELECTOR_MANUAL_METHOD_SUC_VALUE = {
    "var_ip_method": "manual",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["空闲机池", "集群1"], "var_module": ["db"], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "空闲机,集群1", "var_manual_module": "all,db", "var_module_name": ""},
    "var_filter_set": "集群1,集群2",
    "var_filter_module": "ls",
}
IP_SELECTOR_MANUAL_METHOD_FAIL_VALUE = {
    "var_ip_method": "manual",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["空闲机池", "集群1"], "var_module": ["db"], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "空闲机,集群1", "var_manual_module": "all,db", "var_module_name": ""},
    "var_filter_set": "集群1,集群2",
    "var_filter_module": "ls",
}
IP_SELECTOR_CUSTOM_METHOD_SUC_VALUE = {
    "var_ip_method": "custom",
    "var_ip_custom_value": "192.168.15.18,192.168.15.4",
    "var_ip_select_value": {"var_set": [], "var_module": [], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "集群1,集群2",
    "var_filter_module": "ls",
}
IP_SELECTOR_CUSTOM_METHOD_FAIL_VALUE = {
    "var_ip_method": "custom",
    "var_ip_custom_value": "192.168.15.18,192.168.15.4",
    "var_ip_select_value": {"var_set": [], "var_module": [], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "集群1,集群2",
    "var_filter_module": "ls",
}
IP_SELECTOR_CUSTOM_METHOD_BIZ_INPUT_INNER_SET_SUCCESS_VALUE = {
    "var_ip_method": "custom",
    "var_ip_custom_value": "192.168.15.18,192.168.15.4",
    "var_ip_select_value": {"var_set": [], "var_module": [], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "空闲机池,集群2",
    "var_filter_module": "ls",
}
IP_SELECTOR_CUSTOM_METHOD_BIZ_INPUT_INNER_MODULE_SUCCESS_VALUE = {
    "var_ip_method": "custom",
    "var_ip_custom_value": "192.168.15.18,192.168.15.4",
    "var_ip_select_value": {"var_set": [], "var_module": [], "var_module_name": "ip"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "",
    "var_filter_module": "空闲机",
}
IP_SELECTOR_SELECT_METHOD_BIZ_INPUT_INNER_SET_SUCCESS_VALUE = {
    "var_ip_method": "select",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["空闲机池", "集群1"], "var_module": ["空闲机"], "var_module_name": "ip,空闲机"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "空闲机池,集群2",
    "var_filter_module": "ls",
}
IP_SELECTOR_SELECT_METHOD_BIZ_INPUT_NO_FILTER_SET_MODULE_SUCCESS_VALUE = {
    "var_ip_method": "select",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["空闲机池", "集群1"], "var_module": ["空闲机"], "var_module_name": "ip,空闲机"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "",
    "var_filter_module": "",
}
IP_SELECTOR_SELECT_METHOD_BIZ_INPUT_NO_FILTER_SET_MODULE_SELECT_MODULE_SUCCESS_VALUE = {
    "var_ip_method": "select",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["空闲机池", "集群1"], "var_module": [], "var_module_name": ""},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "",
    "var_filter_module": "",
}
IP_SELECTOR_SELECT_METHOD_BIZ_INPUT_INNER_MODULE_SUCCESS_VALUE = {
    "var_ip_method": "select",
    "var_ip_custom_value": "",
    "var_ip_select_value": {"var_set": ["空闲机池", "集群1"], "var_module": ["空闲机"], "var_module_name": "ip,空闲机"},
    "var_ip_manual_value": {"var_manual_set": "", "var_manual_module": "", "var_module_name": ""},
    "var_filter_set": "集群1,集群2",
    "var_filter_module": "ls,空闲机",
}


class VarCmdbSetModuleIpSelectorTestCase(TestCase):
    def setUp(self):
        self.supplier_account = "supplier_account_token"

        self.project_patcher = patch(
            "pipeline_plugins.variables.collections.sites.open.cmdb.var_cmdb_set_module_ip_selector.Project",
            mock_project,
        )
        self.get_business_host_return = [
            {"bk_host_innerip": "1.1.1.1", "bk_cloud_id": 1, "bk_attr": 1},
            {"bk_host_innerip": "1.1.1.2", "bk_cloud_id": 2, "bk_attr": 2},
            {"bk_host_innerip": "1.1.1.3", "bk_attr": 3},
        ]
        self.bk_biz_id = 1
        mock_project_obj.bk_biz_id = self.bk_biz_id

        self.supplier_account_for_project_patcher = patch(
            "pipeline_plugins.variables.collections.sites.open.cmdb.var_cmdb_set_module_ip_selector."
            "supplier_account_for_project",
            MagicMock(return_value=self.supplier_account),
        )

        self.cc_get_ips_info_by_str_patcher = patch(
            CC_GET_IPS_INFO_BY_STR, MagicMock(return_value=CC_GET_IPS_INFO_BY_STR_RETURN)
        )
        self.cc_get_ips_info_by_str_patcher.start()

        self.pipeline_data = {"executor": "admin", "biz_cc_id": 123, "project_id": 1}

        self.project_patcher.start()
        self.supplier_account_for_project_patcher.start()

        self.select_method_success_return = "192.168.15.18,192.168.15.4"
        self.select_method_get_ip_fail_return = ""
        self.manual_method_success_return = "192.168.15.18,192.168.15.4"
        self.manual_method_fail_return = ""
        self.custom_method_success_return = "192.168.15.18,192.168.15.4"
        self.custom_method_fail_return = ""
        self.custom_method_biz_input_inner_module_success_case_return = "192.168.15.18,192.168.15.4"
        self.custom_method_biz_input_inner_set_success_case_return = "192.168.15.18,192.168.15.4"
        self.select_method_biz_input_inner_module_success_case_return = "192.168.15.18,192.168.15.4"
        self.select_method_biz_input_inner_set_success_case_return = ""
        self.select_method_no_filter_set_module_success_case_return = "192.168.15.18,192.168.15.4"
        self.select_method_no_filter_set_module_select_module_success_case_return = "192.168.15.18,192.168.15.4"

    def tearDown(self):
        self.cc_get_ips_info_by_str_patcher.stop()
        self.project_patcher.stop()
        self.supplier_account_for_project_patcher.stop()

    @patch(GET_CLIENT_BY_USER, return_value=SELECT_METHOD_SUC_CLIENT)
    def test_select_method_success_case(self, mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_SELECT_METHOD_SUC_VALUE,
            name="test_select_method_success_case",
            context={},
        )
        self.assertEqual(self.select_method_success_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": SELECT_METHOD_SUC_CLIENT.cc.find_module_with_relation,
                "calls": [call(bk_biz_id=1, bk_service_template_ids=[], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_service_template_ids=[], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'limit': 500, 'start': 0})]
            },
            {
                "func": SELECT_METHOD_SUC_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_HAS_FILTER_SET_MODULUE_CLIENT)
    def test_ip_selector_select_method_suc_no_filter_has_filter_set_modulue_success_case(self,
                                                                                         mock_get_client_by_user_return
                                                                                         ):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_HAS_FILTER_SET_MODULUE_VALUE,
            name="test_ip_selector_select_method_suc_no_filter_has_filter_set_modulue_success_case",
            context={},
        )
        self.assertEqual(self.select_method_success_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func":
                    IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_HAS_FILTER_SET_MODULUE_CLIENT.cc.find_module_with_relation,
                "calls": []
            },
            {
                "func": IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_HAS_FILTER_SET_MODULUE_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[3], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[3], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_SET_MODULE_CLIENT)
    def test_ip_selector_select_method_suc_has_filter_set_module_success_case(self, mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_SET_MODULE_VALUE,
            name="test_ip_selector_select_method_suc_has_filter_set_module_success_case",
            context={},
        )
        self.assertEqual(self.select_method_success_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_SET_MODULE_CLIENT.cc.find_module_with_relation,
                "calls": []
            },
            {
                "func": IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_SET_MODULE_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[3], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[3], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_OTHER_SET_CLIENT)
    def test_ip_selector_select_method_suc_has_filter_other_set_success_case(self, mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_OTHER_SET_VALUE,
            name="test_ip_selector_select_method_suc_has_filter_other_set_success_case",
            context={},
        )
        self.assertEqual(self.select_method_success_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_OTHER_SET_CLIENT.cc.find_module_with_relation,
                "calls": [call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'limit': 500, 'start': 0})]
            },
            {
                "func": IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_OTHER_SET_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[60, 61, 3], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[60, 61, 3], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_OTHER_SET_MODULE_CLIENT)
    def test_ip_selector_select_method_suc_has_filter_other_set_module_success_case(self,
                                                                                    mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_OTHER_SET_MODULE_VALUE,
            name="test_ip_selector_select_method_suc_has_filter_other_set_module_success_case",
            context={},
        )
        self.assertEqual(self.select_method_success_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_OTHER_SET_MODULE_CLIENT.cc.find_module_with_relation,
                "calls": [call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'limit': 500, 'start': 0})]
            },
            {
                "func": IP_SELECTOR_SELECT_METHOD_SUC_HAS_FILTER_OTHER_SET_MODULE_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[60, 61, 3], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[60, 61, 3], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_NO_MODULUE_CLIENT)
    def test_ip_selector_select_method_suc_no_filter_no_modulue_success_case(self,
                                                                             mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_NO_MODULUE_VALUE,
            name="test_ip_selector_select_method_suc_no_filter_no_modulue_success_case",
            context={},
        )
        self.assertEqual(self.select_method_success_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_NO_MODULUE_CLIENT.cc.find_module_with_relation,
                "calls": [call(bk_biz_id=1, bk_service_template_ids=[3, 4, 5], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_service_template_ids=[3, 4, 5], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'limit': 500, 'start': 0})]
            },
            {
                "func": IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_NO_MODULUE_CLIENT.cc.list_biz_hosts,
                "calls": [
                    call(bk_biz_id=1, bk_module_ids=[60, 61, 3, 4, 5], bk_supplier_account='supplier_account_token',
                         fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                    call(bk_biz_id=1, bk_module_ids=[60, 61, 3, 4, 5], bk_supplier_account='supplier_account_token',
                         fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_CLIENT)
    def test_ip_selector_select_method_suc_no_filter_success_case(self,
                                                                  mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_VALUE,
            name="test_ip_selector_select_method_suc_no_filter_success_case",
            context={},
        )
        self.assertEqual(self.select_method_success_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_CLIENT.cc.find_module_with_relation,
                "calls": [call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'limit': 500, 'start': 0})]
            },
            {
                "func": IP_SELECTOR_SELECT_METHOD_SUC_NO_FILTER_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[60, 61, 3], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[60, 61, 3], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=IP_SELECTOR_SELECT_METHOD_NO_INNER_MODULE_SUCCESS_CLIENT)
    def test_ip_selector_select_method_no_inner_module_success_case(self,
                                                                    mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_SELECT_METHOD_NO_INNER_MODULE_SUCCESS_VALUE,
            name="test_ip_selector_select_method_no_inner_module_success_case",
            context={},
        )
        self.assertEqual(self.select_method_success_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": IP_SELECTOR_SELECT_METHOD_NO_INNER_MODULE_SUCCESS_CLIENT.cc.find_module_with_relation,
                "calls": [call(bk_biz_id=1, bk_service_template_ids=[], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_service_template_ids=[], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'limit': 500, 'start': 0})]
            },
            {
                "func": IP_SELECTOR_SELECT_METHOD_NO_INNER_MODULE_SUCCESS_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=IP_SELECTOR_SELECT_METHOD_ALL_SELECT_SET_SUCCESS_CLIENT)
    def test_ip_selector_select_method_all_select_set_success__case(self,
                                                                    mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_SELECT_METHOD_ALL_SELECT_SET_SUCCESS_VALUE,
            name="test_ip_selector_select_method_all_select_set_success__case",
            context={},
        )
        self.assertEqual(self.select_method_success_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": IP_SELECTOR_SELECT_METHOD_ALL_SELECT_SET_SUCCESS_CLIENT.cc.find_module_with_relation,
                "calls": [call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31, 32], fields=['bk_module_id'],
                               page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31, 32], fields=['bk_module_id'],
                               page={'limit': 500, 'start': 0})]
            },
            {
                "func": IP_SELECTOR_SELECT_METHOD_ALL_SELECT_SET_SUCCESS_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=IP_SELECTOR_SELECT_METHOD_ALL_SELECT_SET_MODULE_SUCCESS_CLIENT)
    def test_ip_selector_select_method_all_select_set_module_success__case(self,
                                                                           mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_SELECT_METHOD_ALL_SELECT_SET_MODULE_SUCCESS_VALUE,
            name="test_ip_selector_select_method_all_select_set_module_success__case",
            context={},
        )
        self.assertEqual(self.select_method_success_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": IP_SELECTOR_SELECT_METHOD_ALL_SELECT_SET_MODULE_SUCCESS_CLIENT.cc.find_module_with_relation,
                "calls": [call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31, 32], fields=['bk_module_id'],
                               page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31, 32], fields=['bk_module_id'],
                               page={'limit': 500, 'start': 0})]
            },
            {
                "func": IP_SELECTOR_SELECT_METHOD_ALL_SELECT_SET_MODULE_SUCCESS_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=IP_SELECTOR_SELECT_METHOD_ALL_SELECT_MODULE_SUCCESS_CLIENT)
    def test_ip_selector_select_method_all_select_module_success_case(self,
                                                                      mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_SELECT_METHOD_ALL_SELECT_MODULE_SUCCESS_VALUE,
            name="test_ip_selector_select_method_all_select_module_success_case",
            context={},
        )
        self.assertEqual(self.select_method_success_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": IP_SELECTOR_SELECT_METHOD_ALL_SELECT_MODULE_SUCCESS_CLIENT.cc.find_module_with_relation,
                "calls": [call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'limit': 500, 'start': 0})]
            },
            {
                "func": IP_SELECTOR_SELECT_METHOD_ALL_SELECT_MODULE_SUCCESS_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=SELECT_METHOD_FAIL_CLIENT)
    def test_select_method_get_ip_fail_case(self, mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_SELECT_METHOD_FAIL_VALUE,
            name="test_select_method_get_ip_fail_case",
            context={},
        )
        self.assertEqual(self.select_method_get_ip_fail_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": SELECT_METHOD_FAIL_CLIENT.cc.find_module_with_relation,
                "calls": []
            },
            {
                "func": SELECT_METHOD_FAIL_CLIENT.cc.list_biz_hosts,
                "calls": []
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=MANUAL_METHOD_SUC_CLIENT)
    def test_manual_method_success_case(self, mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_MANUAL_METHOD_SUC_VALUE,
            name="test_manual_method_success_case",
            context={},
        )
        self.assertEqual(self.manual_method_success_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": MANUAL_METHOD_SUC_CLIENT.cc.find_module_with_relation,
                "calls": [call(bk_biz_id=1, bk_service_template_ids=[], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_service_template_ids=[], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'limit': 500, 'start': 0})]
            },
            {
                "func": MANUAL_METHOD_SUC_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=MANUAL_METHOD_FAIL_CLIENT)
    def test_manual_method_fail_case(self, mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_MANUAL_METHOD_FAIL_VALUE,
            name="test_manual_method_success_case",
            context={},
        )
        self.assertEqual(self.manual_method_fail_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": MANUAL_METHOD_FAIL_CLIENT.cc.find_module_with_relation,
                "calls": []
            },
            {
                "func": MANUAL_METHOD_FAIL_CLIENT.cc.list_biz_hosts,
                "calls": []
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=CUSTOM_METHOD_SUC_CLIENT)
    def test_custom_method_success_case(self, mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_CUSTOM_METHOD_SUC_VALUE,
            name="test_custom_method_success_case",
            context={},
        )
        self.assertEqual(self.custom_method_success_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": CUSTOM_METHOD_SUC_CLIENT.cc.find_module_with_relation,
                "calls": [call(bk_biz_id=1, bk_service_template_ids=[], bk_set_ids=[31, 32], fields=['bk_module_id'],
                               page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_service_template_ids=[], bk_set_ids=[31, 32], fields=['bk_module_id'],
                               page={'limit': 500, 'start': 0})]
            },
            {
                "func": CUSTOM_METHOD_SUC_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=CUSTOM_METHOD_FAIL_CLIENT)
    def test_custom_method_fail_case(self, mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_CUSTOM_METHOD_FAIL_VALUE,
            name="test_manual_method_success_case",
            context={},
        )
        self.assertEqual(self.custom_method_fail_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": CUSTOM_METHOD_FAIL_CLIENT.cc.find_module_with_relation,
                "calls": []
            },
            {
                "func": CUSTOM_METHOD_FAIL_CLIENT.cc.list_biz_hosts,
                "calls": []
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=CUSTOM_METHOD_BIZ_INNERIP_SUC_CLIENT)
    def test_custom_method_biz_input_inner_set_success_case(self, mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_CUSTOM_METHOD_BIZ_INPUT_INNER_SET_SUCCESS_VALUE,
            name="test_custom_method_biz_innerip_success_case",
            context={},
        )
        self.assertEqual(self.custom_method_biz_input_inner_module_success_case_return,
                         set_module_ip_selector.get_value())
        call_assert([
            {
                "func": CUSTOM_METHOD_BIZ_INNERIP_SUC_CLIENT.cc.find_module_with_relation,
                "calls": [call(bk_biz_id=1, bk_service_template_ids=[], bk_set_ids=[32], fields=['bk_module_id'],
                               page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_service_template_ids=[], bk_set_ids=[32], fields=['bk_module_id'],
                               page={'limit': 500, 'start': 0})]
            },
            {
                "func": CUSTOM_METHOD_BIZ_INNERIP_SUC_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=CUSTOM_METHOD_BIZ_INNERIP_SUC_CLIENT)
    def test_custom_method_biz_input_inner_module_success_case(self, mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_CUSTOM_METHOD_BIZ_INPUT_INNER_MODULE_SUCCESS_VALUE,
            name="test_custom_method_biz_input_inner_module_success_case",
            context={},
        )
        self.assertEqual(self.custom_method_biz_input_inner_set_success_case_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": CUSTOM_METHOD_BIZ_INNERIP_SUC_CLIENT.cc.find_module_with_relation,
                "calls": [call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31, 32, 33, 34, 38, 39],
                               fields=['bk_module_id'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31, 32, 33, 34, 38, 39],
                               fields=['bk_module_id'], page={'limit': 500, 'start': 0})]
            },
            {
                "func": CUSTOM_METHOD_BIZ_INNERIP_SUC_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[60, 61, 3], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[60, 61, 3], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=SELECT_METHOD_BIZ_INNERIP_SUC_CLIENT)
    def test_select_method_biz_input_inner_module_success_case(self, mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_SELECT_METHOD_BIZ_INPUT_INNER_MODULE_SUCCESS_VALUE,
            name="test_select_method_biz_innerip_success_case",
            context={},
        )
        self.assertEqual(self.select_method_biz_input_inner_module_success_case_return,
                         set_module_ip_selector.get_value())
        call_assert([
            {
                "func": SELECT_METHOD_BIZ_INNERIP_SUC_CLIENT.cc.find_module_with_relation,
                "calls": [call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31], fields=['bk_module_id'],
                               page={'limit': 500, 'start': 0})]
            },
            {
                "func": SELECT_METHOD_BIZ_INNERIP_SUC_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=SELECT_METHOD_BIZ_INNERIP_SUC_CLIENT)
    def test_select_method_biz_input_inner_set_success_case(self, mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_SELECT_METHOD_BIZ_INPUT_INNER_SET_SUCCESS_VALUE,
            name="test_select_method_biz_input_inner_set_success_case",
            context={},
        )
        self.assertEqual(self.select_method_biz_input_inner_set_success_case_return, set_module_ip_selector.get_value())
        call_assert([
            {
                "func": SELECT_METHOD_BIZ_INNERIP_SUC_CLIENT.cc.find_module_with_relation,
                "calls": []
            },
            {
                "func": SELECT_METHOD_BIZ_INNERIP_SUC_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[60, 61], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=SELECT_METHOD_BIZ_INNERIP_NO_FILTER_SET_MODULE_SUC_CLIENT)
    def test_select_method_no_filter_set_module_success_case(self, mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_SELECT_METHOD_BIZ_INPUT_NO_FILTER_SET_MODULE_SUCCESS_VALUE,
            name="test_select_method_no_filter_set_module_success_case",
            context={},
        )
        self.assertEqual(self.select_method_no_filter_set_module_success_case_return,
                         set_module_ip_selector.get_value())
        call_assert([
            {
                "func": SELECT_METHOD_BIZ_INNERIP_NO_FILTER_SET_MODULE_SUC_CLIENT.cc.find_module_with_relation,
                "calls": [
                    call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31], fields=['bk_module_id'],
                         page={'start': 0, 'limit': 1}
                         ),
                    call(bk_biz_id=1, bk_service_template_ids=[3], bk_set_ids=[31], fields=['bk_module_id'],
                         page={'limit': 500, 'start': 0}
                         )
                ]
            },
            {
                "func": SELECT_METHOD_BIZ_INNERIP_NO_FILTER_SET_MODULE_SUC_CLIENT.cc.list_biz_hosts,
                "calls": [call(bk_biz_id=1, bk_module_ids=[60, 61, 3], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                          call(bk_biz_id=1, bk_module_ids=[60, 61, 3], bk_supplier_account='supplier_account_token',
                               fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])

    @patch(GET_CLIENT_BY_USER, return_value=SELECT_METHOD_BIZ_INNERIP_NO_FILTER_SET_MODULE_SELECT_MODULE_SUC_CLIENT)
    def test_select_method_no_filter_set_module_select_module_success_case(self, mock_get_client_by_user_return):
        set_module_ip_selector = SetModuleIpSelector(
            pipeline_data=self.pipeline_data,
            value=IP_SELECTOR_SELECT_METHOD_BIZ_INPUT_NO_FILTER_SET_MODULE_SELECT_MODULE_SUCCESS_VALUE,
            name="test_select_method_no_filter_set_module_select_module_success_case",
            context={},
        )
        self.assertEqual(self.select_method_no_filter_set_module_select_module_success_case_return,
                         set_module_ip_selector.get_value())
        call_assert([
            {
                "func":
                    SELECT_METHOD_BIZ_INNERIP_NO_FILTER_SET_MODULE_SELECT_MODULE_SUC_CLIENT.cc.find_module_with_relation, # noqa
                "calls": [
                    call(bk_biz_id=1, bk_service_template_ids=[3, 4, 5], bk_set_ids=[31], fields=['bk_module_id'],
                         page={'start': 0, 'limit': 1}),
                    call(bk_biz_id=1, bk_service_template_ids=[3, 4, 5], bk_set_ids=[31], fields=['bk_module_id'],
                         page={'limit': 500, 'start': 0})
                ]
            },
            {
                "func": SELECT_METHOD_BIZ_INNERIP_NO_FILTER_SET_MODULE_SELECT_MODULE_SUC_CLIENT.cc.list_biz_hosts,
                "calls": [
                    call(bk_biz_id=1, bk_module_ids=[60, 61, 3, 4, 5], bk_supplier_account='supplier_account_token',
                         fields=['bk_host_innerip'], page={'start': 0, 'limit': 1}),
                    call(bk_biz_id=1, bk_module_ids=[60, 61, 3, 4, 5], bk_supplier_account='supplier_account_token',
                         fields=['bk_host_innerip'], page={'limit': 500, 'start': 0})]
            }
        ])


def call_assert(calls_list):
    for call_item in calls_list:
        call_item["func"].assert_has_calls(calls=call_item["calls"])
