from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka

with Diagram("Xen Performance Analysis Tool Architecture", show=False, direction="TB"):
    with Cluster("Data Capture Layer"):
        xentrace = Server("xentrace")
    
    with Cluster("Core Processing"):
        with Cluster("Event Processing"):
            reader = Server("Reader")
            event_handler = Server("EventHandler")
            events = Server("Event")
        
        with Cluster("Analysis Tools"):
            cpu_analysis = Server("CPU Analysis")
            io_analysis = Server("I/O Analysis")
            xen_stats = Server("Xen Stats")
    
    with Cluster("Data Storage"):
        trace_data = PostgreSQL("Trace Data")
        results_db = PostgreSQL("Results")
    
    xentrace >> reader
    reader >> event_handler
    event_handler >> events
    event_handler >> cpu_analysis
    event_handler >> io_analysis
    event_handler >> xen_stats
    reader >> trace_data
    cpu_analysis >> results_db
    io_analysis >> results_db
    xen_stats >> results_db