from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb, DynamodbStreams
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.aws.security import Cognito
from diagrams.aws.mobile import Amplify
from diagrams.aws.storage import S3
from diagrams.elastic.elasticsearch import Kibana
from diagrams.onprem.client import Users
from diagrams.programming.framework import React

with Diagram("Comprehensive Platform Architecture", show=False):
    user_auth = Cognito("User Auth")
    user = Users("End User")

    frontend = React("React PWA")
    amplify = Amplify("AWS Amplify")
    user >> user_auth >> frontend >> amplify

    backend = Lambda("Data Aggregation")
    es_hasher = Lambda("ES Hasher")
    stream_handler = Lambda("Stream Handler")
    get_es_documents = Lambda("Get ES Documents")

    frontend >> backend >> [Dynamodb("DynamoDB"), Elasticsearch("Elasticsearch")]
    backend >> es_hasher >> Elasticsearch("Elasticsearch")
    backend >> stream_handler >> DynamodbStreams("DynamoDB Streams")
    backend >> get_es_documents >> Elasticsearch("Elasticsearch")

    s3_bucket = S3("S3 Data Lake")
    frontend >> s3_bucket

    kibana = Kibana("Kibana Admin Console")
    Elasticsearch("Elasticsearch") >> kibana