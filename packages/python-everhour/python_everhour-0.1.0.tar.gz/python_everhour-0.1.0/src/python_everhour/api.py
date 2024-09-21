import logging
import random
from datetime import datetime
from python_everhour import config
import requests

log = logging.getLogger(__name__)


class EverhourAPI:
    base_url =  config.everhour.base_url
    api_key: str

    def __init__(self, api_key: str):
        self.api_key = api_key

    @property
    def _header(self):
        return {"Content-Type": "application/json", "X-Api-Key": self.api_key}

    @staticmethod
    def _obfuscate_api_key(secret):
        num_chars_to_mask = int(len(secret) * 0.3)
        mask_indices = random.sample(range(len(secret)), num_chars_to_mask)

        obfuscated_secret = list(secret)
        for i in mask_indices:
            obfuscated_secret[i] = "*"

        return "".join(obfuscated_secret)

    def _get_mask_replacements(self):
        return {self.api_key: EverhourAPI._obfuscate_api_key(self.api_key)}

    @property
    def _obfuscated_headers(self):
        replacements = self._get_mask_replacements()
        replaced = str(self._header)
        for k in replacements:
            replaced = replaced.replace(k, replacements[k])
        return replaced

    def query_everhour(self, query):
        # Everhour connection params

        url = f"{self.base_url}{query}"

        try:
            response = requests.get(url, headers=self._header)

            # Log the HTTP status code
            log.info(f"HTTP Status Code: {response.status_code}")
            # Raise an HTTPError if the response code was not 2XX
            response.raise_for_status()

            return response.text
        except requests.exceptions.RequestException as e:
            # Log any exceptions
            log.exception(
                f"API call to {url} with {self._obfuscated_headers} failed:", exc_info=e
            )
            raise e

    def get_time_entries(self, start_date: datetime, end_date: datetime):
        return self.query_everhour(
            "/team/time?from="
            + start_date.strftime("%Y-%m-%d")
            + "&to="
            + end_date.strftime("%Y-%m-%d")
        )

    def get_projects(self):
        return self.query_everhour("/projects")

    def get_users(self):
        # load up all users frm everhour
        return self.query_everhour("/team/users")
    
    def get_user(self):
        # load up all users frm everhour
        return self.query_everhour("/users/me")

    def get_schedule_assignments(self):
        # load up schedule assignments from everhour
        return self.query_everhour("/resource-planner/assignments")
