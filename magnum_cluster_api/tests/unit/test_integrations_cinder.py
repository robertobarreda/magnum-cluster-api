# Copyright (c) 2026 VEXXHOST, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from types import SimpleNamespace
from unittest import mock

from magnum_cluster_api.integrations import cinder


def test_get_volume_types_openstacksdk(mocker):
    types = mock.Mock(return_value=iter([SimpleNamespace(name="fast")]))
    osc = mock.Mock()
    osc.cinder.return_value = SimpleNamespace(types=types)
    mocker.patch("magnum_cluster_api.clients.get_openstack_api").return_value = osc

    assert cinder.get_volume_types(mock.Mock())[0].name == "fast"
    types.assert_called_once_with()


def test_get_default_volume_type_openstacksdk_prefers_default(mocker):
    default = {"name": "__DEFAULT__"}
    types = mock.Mock(return_value=iter([SimpleNamespace(name="fast"), default]))
    osc = mock.Mock()
    osc.cinder.return_value = SimpleNamespace(types=types)
    mocker.patch("magnum_cluster_api.clients.get_openstack_api").return_value = osc

    assert cinder.get_default_volume_type(mock.Mock()) == default


def test_get_default_boot_volume_type_openstacksdk(mocker):
    types = mock.Mock(return_value=iter([SimpleNamespace(name="fast")]))
    osc = mock.Mock()
    osc.cinder.return_value = SimpleNamespace(types=types)
    mocker.patch("magnum_cluster_api.clients.get_openstack_api").return_value = osc

    assert cinder.get_default_boot_volume_type(mock.Mock()) == "fast"
