from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Nomad
from diagrams.onprem.network import Consul
from diagrams.onprem.database import Hive
from diagrams.onprem.analytics import Presto
from diagrams.onprem.iac import Ansible, Terraform
from diagrams.onprem.ci import GithubActions
from diagrams.generic.os import Vagrant
from diagrams.aws.storage import S3

with Diagram("Data Mesh Architecture", show=False, direction="TB"):
    with Cluster("Development Environment"):
        vagrant = Vagrant("Vagrant")
        ansible = Ansible("Ansible")
        terraform = Terraform("Terraform")
        github_actions = GithubActions("GitHub Actions")
    
    with Cluster("Orchestration & Service Mesh"):
        nomad = Nomad("Nomad")
        consul = Consul("Consul")
    
    with Cluster("Data Services"):
        minio = S3("MinIO")
        hive = Hive("Hive Metastore")
        presto = Presto("Presto")
        sqlpad = Presto("SQLPad")
    
    vagrant >> ansible
    ansible >> terraform
    terraform >> nomad
    nomad >> consul
    consul >> [minio, hive, presto, sqlpad]
    minio >> hive
    hive >> presto
    presto >> sqlpad
    github_actions >> vagrant