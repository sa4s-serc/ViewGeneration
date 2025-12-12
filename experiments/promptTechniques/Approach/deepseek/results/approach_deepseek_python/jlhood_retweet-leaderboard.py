from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import APIGateway
from diagrams.aws.integration import Eventbridge
from diagrams.onprem.client import User

with Diagram("jlhood_retweet-leaderboard Architecture", show=False, direction="LR"):
    twitter_source = User("Twitter Event Source")
    
    tweet_processor = Lambda("TweetProcessor")
    get_leaderboard = Lambda("GetLeaderboard")
    
    dynamodb = Dynamodb("Leaderboard Table")
    api_gateway = APIGateway("API Gateway")
    
    web_client = User("Web Client")
    
    twitter_source >> tweet_processor
    tweet_processor >> dynamodb
    api_gateway >> get_leaderboard
    get_leaderboard >> dynamodb
    api_gateway >> web_client