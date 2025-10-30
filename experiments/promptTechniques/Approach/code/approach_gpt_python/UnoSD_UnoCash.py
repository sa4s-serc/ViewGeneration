from diagrams import Diagram
from diagrams.azure.identity import ADB2C, ADIdentityProtection
from diagrams.azure.compute import ACR, FunctionApps, KubernetesServices
from diagrams.azure.integration import APIManagement
from diagrams.azure.storage import BlobStorage, ArchiveStorage
from diagrams.onprem.iac import Pulumi

with Diagram("UnoCash Application Architecture", show=False):
    api_mgmt = APIManagement("API Management")
    blazor_frontend = KubernetesServices("Blazor Frontend")
    azure_function = FunctionApps("Azure Functions")
    identity_protection = ADIdentityProtection("AD Protection")
    b2c = ADB2C("B2C")
    blob_storage = BlobStorage("Blob Storage")
    archive_storage = ArchiveStorage("Archive Storage")
    pulumi = Pulumi("Pulumi")

    blazor_frontend >> api_mgmt >> azure_function
    azure_function >> [blob_storage, archive_storage]
    blazor_frontend >> identity_protection >> b2c
    pulumi >> [blazor_frontend, azure_function, api_mgmt]