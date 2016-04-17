# Copyright (c) 2016 Morgan Fainberg
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

from flask.ext import login

API_KEY_HEADER = 'Shade-API-Key'
API_KEY_HEADER_DESC = 'APIKey Auth Header: 16bytes HEX'
LOGIN_MANAGER = login.LoginManager()


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': API_KEY_HEADER
    }
}


class ShadeAPIUser(object):
    def __init__(self, key=None):
        self.key = key

    @property
    def is_authenticated(self):
        if self.key:
            return True
        return False

    @property
    def is_active(self):
        if self.key:
            return True
        return False

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.key


@LOGIN_MANAGER.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Shade-API-Key')
    # TODO: Lookup User Based on API Key
    # NOTE: This will use fernet instead of UUID long term.
    try:
        key = uuid.UUID(hex=api_key)
        return ShadeAPIUser(key=key)
    except Exception:
        pass
    return None
