from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.onprem.network import Nginx
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Github
from diagrams.onprem.client import Users

with Diagram("Aliyun Packagist Mirror Architecture", show=False, direction="LR"):
    users = Users("Composer Users")
    
    with Cluster("Aliyun Packagist Mirror"):
        main_service = Custom("Main Service", "./icons/go.png")
        config = Custom("Configuration (packagist.yml)", "./icons/config.png")

        with Cluster("Synchronization Tasks"):
            sync_providers = Custom("Sync Providers", "./icons/goroutine.png")
            sync_packages_v1 = Custom("Sync Packages V1", "./icons/goroutine.png")
            sync_packages_v2 = Custom("Sync Packages V2", "./icons/goroutine.png")
            sync_distributions = Custom("Sync Distributions", "./icons/goroutine.png")
            sync_composer_phar = Custom("Sync Composer Phar", "./icons/goroutine.png")

        with Cluster("Data Storage"):
            oss = Custom("Alibaba Cloud OSS", "./icons/oss.png")
            redis = Redis("Redis Cache")

        with Cluster("External Services"):
            packagist = Custom("Packagist API", "./icons/api.png")
            github_api = Github("GitHub API")

        cdn = Custom("Alibaba Cloud CDN", "./icons/cdn.png")
        status_monitor = Custom("Status Monitoring", "./icons/status.png")

    users >> main_service
    main_service >> config
    main_service >> [sync_providers, sync_packages_v1, sync_packages_v2, sync_distributions, sync_composer_phar]
    sync_providers >> oss
    sync_packages_v1 >> oss
    sync_packages_v2 >> oss
    sync_distributions >> oss
    sync_composer_phar >> oss
    sync_providers >> redis
    sync_packages_v1 >> redis
    sync_packages_v2 >> redis
    sync_distributions >> redis
    sync_composer_phar >> redis
    sync_providers >> packagist
    sync_packages_v1 >> packagist
    sync_packages_v2 >> packagist
    sync_distributions >> github_api
    sync_composer_phar >> github_api
    main_service >> cdn
    main_service >> status_monitor