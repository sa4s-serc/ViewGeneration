from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.onprem.client import User
from diagrams.onprem.network import Internet
from diagrams.programming.language import Python

with Diagram("Webex Teams Chatbot Architecture", show=False):
    client = User("User")

    with Cluster("AWS Cloud"):
        api_gateway = APIGateway("API Gateway")
        lambda_function = Lambda("Lambda Function")
        
        api_gateway >> Edge(label="Invoke") >> lambda_function

    with Cluster("External Services"):
        joke_api = Internet("icanhazdadjoke.com")
        webex_api = Internet("Webex Teams API")

        lambda_function >> Edge(label="GET Joke") >> joke_api
        lambda_function >> Edge(label="POST Joke") >> webex_api

    client >> Edge(label="Mention Bot") >> webex_api
    webex_api >> Edge(label="Webhook Trigger") >> api_gateway