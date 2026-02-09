from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.saas.chat import Teams
from diagrams.programming.framework import Flask
from diagrams.aws.integration import Eventbridge

with Diagram("Webex Teams Chatbot Architecture", show=False):
    with Cluster("AWS Cloud"):
        api = APIGateway("API Gateway")
        lambda_fn = Lambda("Joke Bot\nLambda")
        events = Eventbridge("Events")

    with Cluster("External Services"):
        webex = Teams("Webex Teams")
        jokes = Flask("icanhazdadjoke\nAPI")

    webex >> api >> lambda_fn
    lambda_fn >> jokes
    lambda_fn >> webex
    events >> lambda_fn