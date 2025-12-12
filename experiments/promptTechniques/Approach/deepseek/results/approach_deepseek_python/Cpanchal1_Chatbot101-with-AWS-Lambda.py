from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.onprem.client import User
from diagrams.custom import Custom

with Diagram("Webex Teams Chatbot Architecture", show=False, direction="LR"):
    user = User("Webex Teams User")
    teams = Custom("Webex Teams", "./custom_icons/teams.png")
    api_gateway = APIGateway("API Gateway")
    lambda_func = Lambda("chatbot.py")
    joke_api = Custom("icanhazdadjoke.com", "./custom_icons/joke_api.png")
    
    user >> teams
    teams >> api_gateway
    api_gateway >> lambda_func
    lambda_func >> joke_api
    lambda_func >> teams