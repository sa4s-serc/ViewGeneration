from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Database
from diagrams.aws.integration import Appsync
from diagrams.aws.mobile import APIGateway
from diagrams.aws.integration import SNS
from diagrams.aws.ml import Translate
from diagrams.aws.general import Client, Users
from diagrams.programming.framework import Nextjs

with Diagram("Reinvent2022 Vote App Architecture", show=False):
    with Cluster("Frontend"):
        client = Users("Users")
        next = Nextjs("Next.js App")

    with Cluster("API Layer"):
        appsync = Appsync("AppSync API")
        
    with Cluster("Backend Services"):
        dynamo = Database("Vote Storage")
        sns = SNS("Vote Events")
        translate = Translate("Message Translation")
        
        funcs = [
            Lambda("Save to DynamoDB"),
            Lambda("Publish to SNS"),
            Lambda("Translate Message")
        ]

    # Frontend connections
    client >> next
    next >> appsync

    # Backend connections 
    appsync >> funcs[0]
    appsync >> funcs[1] 
    appsync >> funcs[2]

    funcs[0] >> dynamo
    funcs[1] >> sns
    funcs[2] >> translate