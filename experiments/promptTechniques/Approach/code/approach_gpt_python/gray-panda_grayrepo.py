from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import ELB
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.aws.general import Users
from diagrams.onprem.network import Internet

with Diagram("Flare-On CTF Challenges Architecture", show=False):
    internet = Internet("Internet")

    with Cluster("Malware Analysis"):
        client = Users("User")

        with Cluster("Malware System"):
            elb = ELB("Load Balancer")
            ec2 = EC2("Malware EC2")
            rds = RDS("Malware RDS")
            
            elb >> Edge(label="UDP, IRC") >> ec2
            ec2 >> Edge(label="encrypted data") >> rds

        client >> Edge(label="access") >> elb
        internet >> Edge(label="C2 communication") >> ec2

    with Cluster("SSHD Exploitation"):
        sshd = EC2("SSHD Vulnerable Server")
        core_dump = S3("Core Dump Storage")
        
        sshd >> Edge(label="write core dump") >> core_dump

    with Cluster("Mobile App Reverse Engineering"):
        android_app = EC2("Android App Server")
        windows_mobile = EC2("Windows Mobile Server")
        
        android_app >> Edge(label="gesture data") >> windows_mobile

    internet >> Edge(label="user access") >> client