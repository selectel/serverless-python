import os
import requests


class SelectelCredentials:
    auth_url: str = os.getenv("SELECTEL_API_AUTH_URL",
                              "https://api.selvpc.ru/identity/v3/auth/tokens")
    selectel_user_id: str = os.environ.get("SELECTEL_USER_ID")
    project_id: str = os.environ.get("SELECTEL_PROJECT_ID")
    user_name: str = os.environ.get("SELECTEL_SDK_CLIENT_USER_ID")
    user_password: str = os.environ.get("SELECTEL_SDK_CLIENT_PASSWORD")

    def get_openstack_auth(self):
        return {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "name": self.user_name,
                            "domain": {
                                "name": self.selectel_user_id
                            },
                            "password": self.user_password
                        }
                    }
                },
                "scope": {
                    "project": {
                        "id": self.project_id,
                        "domain": {"name": self.selectel_user_id}
                    }
                }
            }
        }


class Serverless(object):
    api_url: str = os.getenv("SELECTEL_API_S8S_URL",
                             "https://ru-1.api.serverless.selcloud.ru/v1")

    def __init__(self, credentials: SelectelCredentials):
        self.credentials = credentials
        self.session = None
        self.authenticate()

    def authenticate(self):
        resp = requests.post(self.credentials.auth_url,
                             json=self.credentials.get_openstack_auth())
        if resp.status_code != 201:
            raise Exception(f"Unexpected response: {resp.text}")
        self.session = requests.Session()
        self.session.headers.update({
            "Project-ID": self.credentials.project_id,
            "X-Auth-Token": resp.headers["x-subject-token"]
        })

    def _api_call(self, method, path, as_json=True, **kwargs):
        url = f"{self.api_url}/{path}"
        try:
            resp = self.session.request(method, url, **kwargs)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                self.authenticate()
                resp = self.session.request(method, url, **kwargs)
                resp.raise_for_status()
            else:
                raise e
        if as_json:
            return resp.json()
        return resp.text

    def get_modules(self):
        return self._api_call("GET", "modules")

    def get_module(self, module_id):
        return self._api_call("GET", f"modules/{module_id}", as_json=False)

    def delete_module(self, module_id):
        return self._api_call("DELETE", f"modules/{module_id}")

    def upload_module(self, file):
        if isinstance(file, str):
            file = open(file, "rb")
        resp = self._api_call("POST", "modules/upload", files={"files": file})
        return resp

    def create_function(self, action_name):
        body = dict(action_name=action_name)
        return self._api_call("POST", "functions/create", json=body)

    def get_functions(self, skip=None, limit=None, name=None,
                      sort_field=None, sort_type="desc"):
        params = dict(skip=skip, limit=limit, name=name,
                      sort_field=sort_field, sort_type=sort_type)
        return self._api_call("GET", "functions", params=params)

    def get_function(self, action_name):
        return self._api_call("GET", f"functions/{action_name}")

    def delete_function(self, action_name):
        return self._api_call("DELETE", f"functions/{action_name}")

    def edit_function(self, action_name, **kwargs):
        path = f"functions/{action_name}/edit"
        body = dict(action_name=action_name, **kwargs)
        return self._api_call("POST", path, json=body)

    def invoke_function(self, action_name, payload):
        path = f"functions/{action_name}/invoke"
        return self._api_call("POST", path, json=payload)

    def publish_function(self, action_name, is_published=True):
        return self._api_call("POST", f"functions/{action_name}/publish",
                              json=dict(publish=is_published))

    def get_feed_actions(self):
        return self._api_call("GET", "feed_actions")

    def get_feeds(self):
        return self._api_call("GET", "feeds")

    def get_feed(self, feed_name):
        return self._api_call("GET", f"feeds/{feed_name}")

    def create_feed(self, feed_name, feed_action, action_name, params=None):
        body = dict(feed_name=feed_name,
                    feed_action=feed_action,
                    action_name=action_name,
                    parameters=params)
        return self._api_call("PUT", "feeds/create", json=body)

    def delete_feed(self, feed_name):
        return self._api_call("DELETE", f"feeds/{feed_name}")

    def get_activations(self, skip=None, limit=None, name=None,
                        sort_field=None, sort_type="desc"):
        params = dict(skip=skip, limit=limit, name=name,
                      sort_field=sort_field, sort_type=sort_type)
        return self._api_call("GET", "activations", params=params)

    def get_activation_logs(self, activation_id):
        return self._api_call("GET", f"activations/{activation_id}/logs")

    def get_activation_result(self, activation_id):
        return self._api_call("GET", f"activations/{activation_id}/result")
