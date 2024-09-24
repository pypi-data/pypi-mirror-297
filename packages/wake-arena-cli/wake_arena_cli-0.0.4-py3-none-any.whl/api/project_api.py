import urllib
from logging import Logger

import requests


class ProjectApiError(Exception):
    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code


class ProjectApi:
    __SERVER_URL = "https://wake-arena-project-api-1076910080992.europe-west3.run.app"

    def __init__(self, logger: Logger, client_id: str, token: str):
        self.logger = logger
        self.client_id = client_id
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "X-Client-Id": str(client_id),
        }

    def __check_response(self, res: requests.Response):
        isJson = res.headers.get("content-type").startswith("application/json")
        body = res.json() if isJson else res.text

        if res.status_code != 200:
            code = body.get("code") if isJson else res.status_code

            self.logger.error(f"Wake Arena Project API error: {res.status_code}")
            if code:
                self.logger.error(f"{code}")

            raise ProjectApiError(
                f"Wake Arena Project API error: {res.status_code}", code
            )

        return body

    def create_project(self, project_name: str):
        body = {"name": project_name}
        res = requests.post(
            self.__SERVER_URL + "/api/v0/projects", json=body, headers=self.headers
        )
        return self.__check_response(res)

    def get_project(self, project_id: str):
        res = requests.get(
            self.__SERVER_URL + f"/api/v0/projects/{project_id}", headers=self.headers
        )
        return self.__check_response(res)

    def get_upload_link(self, project_id: str):
        res = requests.post(
            self.__SERVER_URL + f"/api/v0/projects/{project_id}/code-upload",
            headers=self.headers,
        )
        return self.__check_response(res)

    def get_vulnerability_check(self, project_id: str, check_id: str):
        return self.__check_response(
            requests.get(
                self.__SERVER_URL + f"/api/v0/projects/{project_id}/checks/{check_id}",
                headers=self.headers,
            )
        )

    def get_vulnerability_check_state_logs(
        self, project_id: str, check_id: str, last_seen_time: str | None = None
    ):
        url = (
            self.__SERVER_URL + f"/api/v0/projects/{project_id}/checks/{check_id}/logs"
        )

        if last_seen_time:
            url += "?" + urllib.parse.urlencode({"lastSeenTime": last_seen_time})

        return self.__check_response(requests.get(url, headers=self.headers))
