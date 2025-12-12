from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Database
from diagrams.aws.mobile import APIGateway
from diagrams.aws.integration import SimpleNotificationServiceSns

with Diagram("Retweet Leaderboard Architecture", show=False):
    with Cluster("AWS Cloud"):
        api = APIGateway("API Gateway")
        
        with Cluster("Serverless Components"):
            tweet_processor = Lambda("Tweet Processor")
            get_leaderboard = Lambda("Get Leaderboard")
            
        db = Database("Leaderboard Table")
        
        sns = SimpleNotificationServiceSns("Twitter Event Source")
        
        # Flow
        sns >> tweet_processor
        tweet_processor >> db
        api >> get_leaderboard
        get_leaderboard >> db