from diagrams import Diagram, Cluster
from diagrams.azure.web import AppServices
from diagrams.azure.network import ApplicationGateway, Firewall
from diagrams.onprem.certificates import LetsEncrypt
from diagrams.azure.integration import APIManagement
from diagrams.azure.identity import ActiveDirectory, ADDomainServices
from diagrams.azure.identity import ADIdentityProtection
from diagrams.onprem.queue import ActiveMQ

with Diagram("Azure-How-To Architecture", show=False):

    with Cluster("Secure Bot Exposure with WAF"):
        bot_app = AppServices("Bot Application")
        app_gateway = ApplicationGateway("Azure Application Gateway")
        waf = Firewall("Web Application Firewall")
        lets_encrypt = LetsEncrypt("Let's Encrypt")

        bot_app >> waf >> app_gateway
        app_gateway << lets_encrypt

    with Cluster("Kerberos Secured On-Prem API Exposure with APIM"):
        on_prem_api = AppServices("On-Premises API")
        ad_proxy = ActiveDirectory("Azure AD Application Proxy")
        apim = APIManagement("Azure API Management")
        ad_connect = ADDomainServices("Azure AD Connect")
        spn = ADIdentityProtection("Service Principal Name")

        on_prem_api >> ad_proxy >> apim
        ad_connect >> spn

    # Legend
    ActiveMQ("Legend: Secure Bot with WAF") >> ActiveMQ("Legend: Kerberos Secured On-Prem API")