from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.queue import Kafka
from diagrams.k8s.compute import Pod
from diagrams.k8s.controlplane import API, APIServer
from diagrams.k8s.network import Service
from diagrams.aws.ml import Sagemaker
from diagrams.onprem.iac import Terraform
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.monitoring import Grafana

with Diagram("Benchmark AI System Overview", show=False, direction="TB"):

    with Cluster("Microservices Architecture"):
        bff = Pod("bai-bff")
        executor = Pod("executor")
        watcher = Pod("watcher")
        sm_executor = Sagemaker("sm-executor")
        fetcher = Pod("fetcher")
        fetcher_dispatcher = Service("fetcher-dispatcher")
        cloudwatch = Prometheus("cloudwatch-exporter")

    with Cluster("Metrics Components"):
        pusher = Pod("metrics-pusher")
        extractor = Pod("metrics-extractor")
        client_lib = Docker("client-lib")

    with Cluster("Infrastructure and Deployment"):
        baictl = Terraform("baictl")
        kubernetes_api = APIServer("Kubernetes API")

    with Cluster("CI/CD Pipeline"):
        codepipeline = API("AWS CodePipeline")

    metrics_flow = Edge(label="metrics flow", style="dashed")

    bff >> Edge(label="submit job") >> executor
    executor >> Edge(label="execute on") >> kubernetes_api
    executor >> Edge(label="execute on") >> sm_executor
    watcher >> Edge(label="monitor jobs") >> executor
    sm_executor >> Edge(label="manage SageMaker lifecycle") >> bff
    fetcher_dispatcher >> Edge(label="dispatch fetcher jobs") >> fetcher
    cloudwatch >> Edge(label="export metrics") >> pusher
    pusher >> metrics_flow >> Kafka("Kafka")
    extractor >> metrics_flow >> Kafka("Kafka")
    client_lib >> metrics_flow >> Kafka("Kafka")
    codepipeline >> Edge(label="trigger deployment") >> baictl
    baictl >> Edge(label="manage infrastructure") >> kubernetes_api
    Grafana("User Dashboard") << Edge(label="visualize metrics") << cloudwatch