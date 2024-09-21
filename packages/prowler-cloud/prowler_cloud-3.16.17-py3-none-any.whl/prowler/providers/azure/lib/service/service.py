from typing import Any

from prowler.lib.logger import logger
from prowler.providers.azure.lib.audit_info.models import Azure_Audit_Info


class AzureService:
    def __init__(
        self,
        service: Any,
        audit_info: Azure_Audit_Info,
    ):
        self.clients = self.__set_clients__(
            audit_info.identity,
            audit_info.credentials,
            service,
            audit_info.azure_region_config,
        )

        self.subscriptions = audit_info.identity.subscriptions
        self.locations = audit_info.locations

        self.audit_config = audit_info.audit_config

    def __set_clients__(self, identity, credentials, service, region_config):
        clients = {}
        try:
            if "GraphServiceClient" in str(service):
                clients.update({identity.domain: service(credentials=credentials)})
            else:
                for display_name, id in identity.subscriptions.items():
                    clients.update(
                        {
                            display_name: service(
                                credential=credentials,
                                subscription_id=id,
                                base_url=region_config.base_url,
                                credential_scopes=region_config.credential_scopes,
                            )
                        }
                    )
        except Exception as error:
            logger.error(
                f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}]: {error}"
            )
        else:
            return clients
