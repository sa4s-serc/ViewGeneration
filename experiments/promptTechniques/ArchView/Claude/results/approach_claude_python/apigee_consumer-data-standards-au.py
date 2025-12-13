from diagrams import Diagram, Cluster
from diagrams.aws.security import IAM
from diagrams.aws.network import APIGateway
from diagrams.aws.compute import Lambda
from diagrams.generic.storage import Storage
from diagrams.programming.language import Python
from diagrams.onprem.monitoring import Prometheus
from diagrams.gcp.analytics import Pubsub
from diagrams.aws.security import Cognito
from diagrams.aws.integration import SQS

with Diagram("CDS Reference Implementation Architecture", show=False, direction="TB"):
    with Cluster("API Layer"):
        api = APIGateway("CDS Banking API Proxies")
        auth = Cognito("Authentication & Authorization")
        consent = Lambda("Consent Management")

    with Cluster("Core Services"):
        shared_flows = Python("Reusable Shared Flows")
        mock_provider = Lambda("Mock OIDC Provider")
        consent_store = Storage("Consent Storage (KVM)")
        metrics = Prometheus("Metrics Service")

    with Cluster("Event Processing"):
        event_bus = Pubsub("Event Processing")
        queue = SQS("Message Queue")

    with Cluster("Security"):
        iam = IAM("Access Management")

    # Connect components
    api >> auth >> consent
    api >> shared_flows
    auth >> mock_provider
    consent >> consent_store
    api >> metrics
    metrics >> event_bus
    event_bus >> queue
    iam >> [api, auth, mock_provider]