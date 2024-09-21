import requests
import json
import random
import logging

from python_asana import config

log = logging.getLogger(__name__)

class AsanaAPI:
    base_url = config.base_url
    api_key: str

    def __init__(self, api_key: str):
        self.api_key = api_key

    @property
    def _headers(self):
        return {"Authorization": f"Bearer {self.api_key}"}

    @staticmethod
    def _obfuscate_api_key(secret):
        num_chars_to_mask = max(1, int(len(secret) * 0.3))
        mask_indices = random.sample(range(len(secret)), num_chars_to_mask)

        obfuscated_secret = list(secret)
        for i in mask_indices:
            obfuscated_secret[i] = "*"

        return "".join(obfuscated_secret)

    def _get_mask_replacements(self):
        return {self.api_key: self._obfuscate_api_key(self.api_key)}

    @property
    def _obfuscated_headers(self):
        replacements = self._get_mask_replacements()
        replaced = str(self._headers)
        for k, v in replacements.items():
            replaced = replaced.replace(k, v)
        return replaced

    def query_asana(self, query):
        url = f"{self.base_url}{query}"

        try:
            response = requests.get(url, headers=self._headers)
            log.info(f"HTTP Status Code: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            result = data["data"]

            while data.get("next_page") and data["next_page"]:
                next_page = data["next_page"]["uri"]
                response = requests.get(next_page, headers=self._headers)
                log.info(f"HTTP Status Code: {response.status_code}")
                response.raise_for_status()
                data = response.json()
                result += data["data"]

            return json.dumps(result)
        except requests.exceptions.RequestException as e:
            log.exception(
                f"API call to {url} with headers {self._obfuscated_headers} failed:", exc_info=e
            )
            raise e