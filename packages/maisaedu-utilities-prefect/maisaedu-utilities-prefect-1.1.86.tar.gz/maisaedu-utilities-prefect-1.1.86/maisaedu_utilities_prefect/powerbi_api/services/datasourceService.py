import requests

from requests.exceptions import HTTPError
from ..models.datasourceModel import datasource


class DatasourceService:
    gateways_snippet = "gateways"
    datasource_snippet = "datasources"

    def __init__(self, client, gateway_id):
        self.client = client
        self.gateway_id = gateway_id
        self.base_url = f"{self.client.api_url}/{self.client.api_version_snippet}/{self.client.api_myorg_snippet}"

    def get_datasourses(self):
        url = (
            self.base_url
            + f"/{self.gateways_snippet}/{self.gateway_id}/{self.datasource_snippet}"
        )
        headers = self.client.auth_header
        
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPError(
                response,
                f"Get datasources returned http error: {response.json()}",
            )

        response = response.json()['value']

        datasources = []
        for entry in response:
            datasources.append(datasource.from_dict(entry))

        return datasources