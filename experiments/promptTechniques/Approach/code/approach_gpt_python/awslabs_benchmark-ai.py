from plantuml import PlantUML

# Create a PlantUML diagram for the AWSLabs Benchmark AI system
uml_code = """
@startuml

title Benchmark AI System Architecture

package "Benchmark AI Microservices" {
    [bai-bff] <<Microservice>> #LightBlue
    [executor] <<Microservice>> #LightBlue
    [watcher] <<Microservice>> #LightBlue
    [sm-executor] <<Microservice>> #LightBlue
    [fetcher] <<Microservice>> #LightBlue
    [fetcher-dispatcher] <<Microservice>> #LightBlue
    [cloudwatch-exporter] <<Microservice>> #LightBlue
}

package "Metrics Components" {
    [metrics-pusher] <<Sidecar>> #LightGreen
    [metrics-extractor] <<Sidecar>> #LightGreen
    [client-lib] <<Library>> #LightGreen
}

package "Infrastructure and Deployment" {
    [baictl] <<Tool>> #Orange
    [Terraform] <<Tool>> #Orange
    [Kubernetes] <<Platform>> #Orange
    [Kafka] <<Messaging>> #Orange
    [ZooKeeper] <<Service Coordination>> #Orange
}

node "AWS Cloud" {
    [EKS Cluster] <<Kubernetes>> #LightYellow
    [MSK Cluster] <<Kafka Cluster>> #LightYellow
    [SageMaker] <<ML Platform>> #LightYellow
    [S3] <<Storage>> #LightYellow
    [DynamoDB] <<Database>> #LightYellow
}

[bai-bff] --> [executor] : Submits Jobs
[executor] --> [watcher] : Job Status
[watcher] --> [bai-bff] : Status Updates

[fetcher-dispatcher] --> [fetcher] : Create Fetcher Jobs
[fetcher] --> [S3] : Fetch Data
[fetcher] --> [DynamoDB] : Metadata

[sm-executor] --> [SageMaker] : Execute Jobs
[cloudwatch-exporter] --> [AWS CloudWatch] : Export Metrics

[metrics-pusher] --> [Kafka] : Push Metrics
[metrics-extractor] --> [Kafka] : Extract Metrics
[client-lib] --> [metrics-pusher] : Emit Metrics

[baictl] --> [Terraform] : Manage Infrastructure
[Terraform] --> [AWS Cloud] : Provision Resources
[Kubernetes] --> [EKS Cluster] : Manage Pods
[ZooKeeper] --> [fetcher-dispatcher] : Service Coordination

@enduml
"""

# Create a PlantUML client
server = PlantUML(url='http://www.plantuml.com/plantuml/uml/')

# Generate and save the diagram
server.processes(uml_code)