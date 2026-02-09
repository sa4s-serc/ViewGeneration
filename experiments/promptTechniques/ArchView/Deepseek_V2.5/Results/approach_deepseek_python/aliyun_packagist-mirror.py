from diagrams import Diagram, Cluster
from diagrams.alibabacloud.storage import OSS
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.client import User
from diagrams.programming.language import Go
from diagrams.onprem.vcs import Github
from diagrams.alibabacloud.network import CloudEnterpriseNetwork as CDN

with Diagram("Alibaba Cloud Packagist Mirror Architecture", show=False, direction="TB"):
    user = User("Composer User")
    
    with Cluster("Alibaba Cloud Packagist Mirror"):
        main_app = Go("Main Application")
        
        with Cluster("Synchronization Services"):
            sync_providers = Go("Sync Providers")
            sync_packages_v1 = Go("Sync Packages V1")
            sync_packages_v2 = Go("Sync Packages V2")
            sync_dists = Go("Sync Distributions")
            sync_composer = Go("Sync Composer.phar")
        
        with Cluster("External Services"):
            packagist = Github("Packagist.org")
            github = Github("GitHub API")
        
        with Cluster("Storage & Cache"):
            oss = OSS("Object Storage\n(Packages & Metadata)")
            redis = Redis("Redis Cache\n(Queues & Status)")
        
        with Cluster("CDN Layer"):
            cdn = CDN("Alibaba Cloud CDN")
    
    user >> cdn
    cdn >> main_app
    
    main_app >> sync_providers
    main_app >> sync_packages_v1
    main_app >> sync_packages_v2
    main_app >> sync_dists
    main_app >> sync_composer
    
    sync_providers >> packagist
    sync_packages_v1 >> packagist
    sync_packages_v2 >> packagist
    sync_dists >> github
    sync_composer >> packagist
    
    sync_providers >> redis
    sync_packages_v1 >> redis
    sync_packages_v2 >> redis
    sync_dists >> redis
    sync_composer >> redis
    
    sync_providers >> oss
    sync_packages_v1 >> oss
    sync_packages_v2 >> oss
    sync_dists >> oss
    sync_composer >> oss
    
    redis >> main_app
    oss >> main_app