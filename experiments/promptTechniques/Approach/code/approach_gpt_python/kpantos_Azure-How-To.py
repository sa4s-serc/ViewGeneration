from diagrams import Diagram, Cluster
from diagrams.azure.network import ApplicationGateway
from diagrams.azure.security import ApplicationSecurityGroup
from diagrams.azure.identity import ActiveDirectoryConnect
from diagrams.azure.compute import AppServices
from diagrams.azure.integration import APIManagement
from diagrams.custom import Custom
from diagrams.onprem.network import Internet

with Diagram("Azure How-To Architecture", show=False, direction="TB"):
    
    web_user = Internet("User")
    
    with Cluster("Secure Bot Exposure with WAF"):
        with Cluster("Azure Environment"):
            bot_service = AppServices("Bot Application")
            app_gateway = ApplicationGateway("Azure Application Gateway")
            waf = ApplicationSecurityGroup("Web Application Firewall")
            lets_encrypt = Custom("Let's Encrypt", "./icons/letsencrypt.png")
        
        web_user >> waf >> app_gateway >> bot_service
        app_gateway << lets_encrypt

    with Cluster("Kerberos Secured On-Prem API Exposure with APIM"):
        with Cluster("On-Premises Environment"):
            onprem_api = Custom("On-Premises API", "./icons/api.png")
        
        with Cluster("Azure Environment"):
            ad_proxy = Custom("Azure AD Application Proxy", "./icons/adproxy.png")
            apim = APIManagement("Azure API Management")
            ad_connect = ActiveDirectoryConnect("Azure AD Connect")
            spn = Custom("Service Principal Name (SPN)", "./icons/spn.png")
        
        web_user >> ad_proxy >> onprem_api
        onprem_api >> apim
        apim >> ad_connect
        ad_connect >> spn