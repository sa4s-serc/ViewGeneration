from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.iac import Terraform
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Git

with Diagram("OpenPSD Model Bank Architecture", show=False, direction="LR"):
    user = User("Client")

    with Cluster("Clean Architecture Layers"):
        with Cluster("Entities"):
            ledger = PostgreSQL("Ledger")
            account = PostgreSQL("Account")
            payment = PostgreSQL("Payment")

        with Cluster("Use Cases"):
            use_case = Server("ModelBank UseCase")

        with Cluster("Providers (Infrastructure)"):
            db_provider = Server("DB Provider")
            grpc_server = Server("gRPC Server")
            mq = RabbitMQ("Message Queue")

        with Cluster("Presentation Layer"):
            controller = Server("ModelBank Controller")
            grpc = Server("gRPC Service")

    user >> Edge(label="uses") >> controller
    controller >> Edge(label="invokes") >> use_case
    use_case >> Edge(label="processes") >> ledger
    use_case >> Edge(label="manages") >> account
    use_case >> Edge(label="handles") >> payment
    controller >> Edge(label="requests") >> grpc
    controller >> Edge(label="connects") >> grpc_server
    grpc_server >> Edge(label="interacts") >> mq
    grpc_server >> Edge(label="accesses") >> db_provider
    db_provider >> Edge(label="CRUD") >> ledger

    with Cluster("Development and Deployment Tools"):
        ci_cd = Jenkins("CI/CD")
        version_control = Git("Version Control")
        infra_automation = Terraform("Infrastructure as Code")

    version_control >> Edge(label="code") >> ci_cd
    ci_cd >> Edge(label="deploys") >> infra_automation
    infra_automation >> Edge(label="provisions") >> [controller, grpc_server, db_provider]