from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.container import Docker
from diagrams.onprem.queue import Celery
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import Postgresql
from diagrams.onprem.monitoring import Grafana, Kibana
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.client import User
from diagrams.onprem.logging import Logstash
from diagrams.onprem.network import Internet
from diagrams.k8s.compute import Pod
from diagrams.onprem.storage import HDFS
from diagrams.onprem.monitoring import Influxdb

with Diagram("Apache Airflow Learning Repository Architecture", show=False, direction="TB"):
    user = User("Data Engineer")

    with Cluster("Docker-Based Deployment"):
        docker = Docker("Docker")
        airflow = Airflow("Apache Airflow")
        postgres = Postgresql("Postgres")
        redis = Redis("Redis")
        celery = Celery("CeleryExecutor")

        with Cluster("Airflow Components"):
            webserver = Server("Web Server")
            scheduler = Server("Scheduler")
            worker = Server("Worker")

        docker >> [webserver, scheduler, worker, postgres, redis, celery]

    with Cluster("Data Pipeline Orchestration"):
        with Cluster("Forex Data Pipeline"):
            http_sensor = Internet("HttpSensor")
            file_sensor = Server("FileSensor")
            python_operator = Server("PythonOperator")
            bash_operator = Server("BashOperator")
            hive_operator = Server("HiveOperator")
            spark_submit_operator = Spark("SparkSubmitOperator")
            email_operator = Server("EmailOperator")
            slack_webhook_operator = Server("SlackWebhookOperator")

        hdfs = HDFS("HDFS")
        http_sensor >> file_sensor >> python_operator >> bash_operator >> hive_operator >> spark_submit_operator >> hdfs
        email_operator >> user
        slack_webhook_operator >> user

    with Cluster("Hadoop Integration"):
        namenode = Server("Namenode")
        datanode = Server("Datanode")
        hive = Server("Hive")
        spark = Spark("Spark")
        livy = Server("Livy")

        namenode >> datanode >> hive >> spark >> livy

    with Cluster("Monitoring & Logging"):
        influxdb = Influxdb("InfluxDB")
        grafana = Grafana("Grafana")
        logstash = Logstash("Logstash")
        kibana = Kibana("Kibana")

        influxdb >> grafana
        logstash >> kibana

    with Cluster("Kubernetes Deployment"):
        k8s_pod = Pod("Airflow Pod")

        k8s_pod - Edge(style="dashed") - docker