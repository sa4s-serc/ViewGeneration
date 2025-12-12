from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.analytics import Glue
from diagrams.aws.analytics import Athena
from diagrams.aws.analytics import EMR
from diagrams.aws.database import RDS
from diagrams.aws.network import CloudFront
from diagrams.aws.mobile import Amplify
from diagrams.onprem.client import Client
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.analytics import Spark
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import React
from diagrams.gcp.analytics import BigQuery
from diagrams.gcp.storage import GCS
from diagrams.azure.database import CosmosDb
from diagrams.azure.compute import ContainerInstances
from diagrams.azure.network import CDNProfiles
from diagrams.generic.database import SQL
from diagrams.generic.storage import Storage
from diagrams.generic.network import Firewall
from diagrams.generic.os import LinuxGeneral
from diagrams.generic.device import Mobile
from diagrams.custom import Custom

with Diagram("Justice40 Tool Architecture", show=False, direction="TB"):
    with Cluster("Data Sources"):
        census = Custom("Census Data", "./icons/census.png")
        fema = Custom("FEMA Data", "./icons/fema.png")
        epa = Custom("EPA Data", "./icons/epa.png")
        first_street = Custom("First Street Foundation", "./icons/first_street.png")
        data_sources = [census, fema, epa, first_street]

    with Cluster("ETL Pipeline"):
        with Cluster("Extract"):
            datasource = Custom("DataSource", "./icons/datasource.png")
        
        with Cluster("Transform"):
            etl_base = Custom("ETL Base", "./icons/etl_base.png")
            etl_runner = Custom("ETL Runner", "./icons/runner.png")
        
        with Cluster("Load"):
            s3_data_lake = S3("S3 Data Lake")
    
    with Cluster("Scoring Engine"):
        score_runner = Custom("Score Runner", "./icons/score_runner.png")
        score_a = Custom("Score A", "./icons/score_a.png")
        score_b = Custom("Score B", "./icons/score_b.png")
        score_n = Custom("Score N", "./icons/score_n.png")
        score_f = Custom("Score F", "./icons/score_f.png")
    
    with Cluster("Map Generation"):
        generate_tiles = Custom("Generate Tiles", "./icons/generate.png")
        tippecanoe = Custom("Tippecanoe", "./icons/tippecanoe.png")
    
    with Cluster("Client Application"):
        with Cluster("Frontend"):
            react_app = React("React App")
            gatsby = Custom("Gatsby", "./icons/gatsby.png")
            maplibre = Custom("Maplibre GL", "./icons/maplibre.png")
            uswds = Custom("USWDS", "./icons/uswds.png")
        
        with Cluster("Features"):
            map_component = Custom("J40 Map", "./icons/map.png")
            info_panel = Custom("Map Info Panel", "./icons/info_panel.png")
            area_detail = Custom("Area Detail", "./icons/area_detail.png")
            download = Custom("Data Download", "./icons/download.png")
    
    with Cluster("Comparison Tool"):
        comparator = Custom("Comparator", "./icons/comparator.png")
    
    with Cluster("Validation"):
        data_validation = Custom("Data Validation", "./icons/validation.png")
    
    with Cluster("Infrastructure"):
        docker = Custom("Docker", "./icons/docker.png")
        github_actions = Custom("GitHub Actions", "./icons/github_actions.png")
    
    data_sources >> datasource
    datasource >> etl_base
    etl_base >> etl_runner
    etl_runner >> s3_data_lake
    s3_data_lake >> score_runner
    score_runner >> score_a
    score_runner >> score_b
    score_runner >> score_n
    score_runner >> score_f
    score_a >> generate_tiles
    score_b >> generate_tiles
    score_n >> generate_tiles
    score_f >> generate_tiles
    generate_tiles >> tippecanoe
    tippecanoe >> map_component
    s3_data_lake >> data_validation
    s3_data_lake >> comparator
    react_app >> map_component
    react_app >> info_panel
   