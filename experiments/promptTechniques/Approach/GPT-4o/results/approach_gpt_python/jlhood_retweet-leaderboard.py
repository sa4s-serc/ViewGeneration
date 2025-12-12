from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import APIGateway
from diagrams.aws.general import User

with Diagram("Retweet Leaderboard Architecture", show=False):
    user = User("Client")

    with Cluster("Serverless Application"):
        tweet_processor_lambda = Lambda("TweetProcessor")
        leaderboard_lambda = Lambda("GetLeaderboard")
        api_gateway = APIGateway("API Gateway")
        dynamodb_table = Dynamodb("Leaderboard")

    user >> api_gateway >> leaderboard_lambda
    tweet_processor_lambda >> dynamodb_table
    leaderboard_lambda >> dynamodb_table