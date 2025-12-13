from diagrams import Diagram, Cluster
from diagrams.onprem.cd import Tekton
from diagrams.onprem.client import Client
from diagrams.saas.alerting import Pagerduty
from diagrams.aws.management import SystemsManager
from diagrams.aws.compute import EC2
from diagrams.k8s.compute import Pod
from diagrams.aws.network import Route53
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3

with Diagram("OpenShift Configuration Anomaly Detection System", show=False, direction="TB"):
    pagerduty = Pagerduty("PagerDuty Alerts")
    
    with Cluster("CAD System"):
        interceptor = Tekton("Tekton Interceptor")
        cadctl = Client("cadctl CLI Tool")
        
        with Cluster("Tekton Pipeline"):
            pipeline = Tekton("PipelineRun")
            investigation = Pod("Investigation Pod")
        
        with Cluster("Investigation Framework"):
            with Cluster("Ready Made Investigations"):
                chgm = Pod("chgm")
                apierror = Pod("apierrorbudgetburn")
                insights = Pod("insightsoperatordown")
                ccam = Pod("ccam")
                upgrade = Pod("upgradeconfigsync")
                cpd = Pod("cpd")
                cluster = Pod("clustermonitoring")
                mhc = Pod("machinehealthcheck")
        
        with Cluster("External Integrations"):
            ocm = SystemsManager("OpenShift Cluster Manager")
            aws = EC2("AWS Services")
            k8s = Pod("Kubernetes API")
            network_verifier = Route53("Network Verifier")
    
    pagerduty >> interceptor
    interceptor >> pipeline
    pipeline >> cadctl
    cadctl >> investigation
    
    investigation >> chgm
    investigation >> apierror
    investigation >> insights
    investigation >> ccam
    investigation >> upgrade
    investigation >> cpd
    investigation >> cluster
    investigation >> mhc
    
    investigation >> ocm
    investigation >> aws
    investigation >> k8s
    investigation >> network_verifier