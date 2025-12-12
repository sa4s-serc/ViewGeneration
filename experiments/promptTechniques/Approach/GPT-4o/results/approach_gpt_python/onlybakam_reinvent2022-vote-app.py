from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SNS
from diagrams.aws.mobile import Appsync
from diagrams.aws.ml import Translate
from diagrams.programming.framework import Nextjs

with Diagram("Reinvent2022 Vote App Architecture", show=False, direction="TB"):
    user = Nextjs("User")

    with Cluster("AWS"):
        appsync = Appsync("AppSync API")
        
        with Cluster("Data Storage"):
            dynamodb = Dynamodb("DynamoDB Table")
        
        sns = SNS("SNS Topic")
        translate = Translate("AWS Translate Service")
        
        with Cluster("Lambda Functions"):
            publish_to_sns = Lambda("publishToSNS")
            save_to_dynamodb = Lambda("saveToDynamoDB")
            translate_message = Lambda("translateMessage")
        
        appsync - Edge(label="invoke") - publish_to_sns
        appsync - Edge(label="invoke") - save_to_dynamodb
        appsync - Edge(label="invoke") - translate_message
        
        publish_to_sns >> Edge(label="publish") >> sns
        save_to_dynamodb >> Edge(label="store") >> dynamodb
        translate_message >> Edge(label="translate") >> translate

    user >> Edge(label="vote") >> appsync
    appsync << Edge(label="real-time updates") << user