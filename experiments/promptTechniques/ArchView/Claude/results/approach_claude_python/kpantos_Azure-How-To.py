from diagrams import Diagram, Cluster
from diagrams.azure.network import ApplicationGateway, Firewall
from diagrams.azure.web import AppServices
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.integration import APIManagement
from diagrams.azure.network import VirtualNetworks

with Diagram("Azure Secure Bot and Kerberos API Architecture", show=False):
    with Cluster("External Access Layer"):
        appgw = ApplicationGateway("Application Gateway")
        waf = Firewall("WAF")

    with Cluster("Application Layer"):
        bot = AppServices("Bot Service")
        apim = APIManagement("API Management")

    with Cluster("Identity & Security"):
        aad = ActiveDirectory("Azure AD")
        adconnect = ActiveDirectory("AD Connect")

    with Cluster("On-Premises"):
        with Cluster("Network"):
            vnet = VirtualNetworks("Virtual Network")
            api = AppServices("Kerberos API")

    # External Access Flow
    appgw >> waf >> bot
    appgw >> waf >> apim

    # API Management Flow
    apim >> api

    # Identity Flow
    aad >> adconnect
    adconnect >> api
    api >> vnet