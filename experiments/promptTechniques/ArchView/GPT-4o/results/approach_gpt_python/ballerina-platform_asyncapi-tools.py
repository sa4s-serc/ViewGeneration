from diagrams import Diagram
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Gitlab
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Grafana
from diagrams.aws.analytics import Glue
from diagrams.aws.compute import LambdaFunction
from diagrams.aws.database import Dynamodb

with Diagram("Ballerina AsyncAPI Tools Architecture", show=False):
    gitlab = Gitlab("Gitlab CI")
    jenkins = Jenkins("Jenkins")
    docker = Docker("Docker")
    grafana = Grafana("Monitoring")
    glue = Glue("Data Processing")
    lambda_func = LambdaFunction("Lambda")
    dynamodb = Dynamodb("Database")

    gitlab >> jenkins >> docker
    docker >> lambda_func >> dynamodb
    lambda_func >> glue
    glue >> grafana