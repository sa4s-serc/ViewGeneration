from diagrams import Diagram, Cluster
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.container import Docker
from diagrams.onprem.analytics import Spark
from diagrams.onprem.database import Postgresql
from diagrams.onprem.queue import Kafka
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.ci import Jenkins

with Diagram("Apache Spark Integration Architecture", show=False, direction="TB"):
    with Cluster("Orchestration Layer"):
        airflow = Airflow("Airflow DAGs")
    
    with Cluster("Container Platform"):
        with Cluster("Kubernetes Cluster"):
            docker = Docker("Docker Containers")
            spark_apps = Spark("Spark Applications")
    
    with Cluster("Data Sources"):
        kafka = Kafka("Kafka Streams")
        postgresql = Postgresql("PostgreSQL")
    
    with Cluster("Processing Layer"):
        with Cluster("Spark Core"):
            spark_core = Spark("Spark Core")
        
        with Cluster("Spark Libraries"):
            spark_sql = Spark("Spark SQL")
            spark_ml = Spark("MLlib")
            spark_streaming = Spark("Spark Streaming")
            graphx = Spark("GraphX")
    
    with Cluster("Storage Layer"):
        hdfs = Server("HDFS")
        redis = Redis("Redis Cache")
    
    with Cluster("Monitoring"):
        grafana = Grafana("Grafana")
        nginx = Nginx("Nginx")
    
    with Cluster("CI/CD"):
        jenkins = Jenkins("Jenkins")
    
    # Data flow connections
    airflow >> docker
    docker >> spark_apps
    kafka >> spark_streaming
    postgresql >> spark_sql
    spark_apps >> spark_core
    spark_core >> [spark_sql, spark_ml, spark_streaming, graphx]
    spark_sql >> hdfs
    spark_ml >> redis
    spark_streaming >> kafka
    graphx >> hdfs
    [spark_core, spark_sql, spark_ml, spark_streaming, graphx] >> grafana
    nginx >> grafana
    jenkins >> docker