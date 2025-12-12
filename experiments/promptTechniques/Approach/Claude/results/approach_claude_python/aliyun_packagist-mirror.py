from diagrams import Diagram, Cluster
from diagrams.alibabacloud.storage import OSS
from diagrams.onprem.inmemory import Redis
from diagrams.programming.language import Go
from diagrams.onprem.vcs import Github
from diagrams.generic.network import Subnet

with Diagram("Aliyun Packagist Mirror Architecture", show=False, direction="TB"):

    with Cluster("Aliyun Packagist Mirror"):
        api = Go("Mirror API")

        with Cluster("Storage"):
            oss = OSS("Alibaba Cloud OSS")
            redis = Redis("Redis Cache")

        with Cluster("External Services"):
            packagist = Subnet("Packagist.org")
            github = Github("GitHub")

        # Connect components
        packagist >> api
        api >> oss
        api >> redis
        api >> github

        # Add bidirectional connections for sync
        api << oss
        api << redis