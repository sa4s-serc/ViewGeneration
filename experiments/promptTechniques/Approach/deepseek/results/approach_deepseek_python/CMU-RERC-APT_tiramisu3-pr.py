from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import Dynamodb, RDS
from diagrams.aws.integration import SQS
from diagrams.aws.mobile import Mobile
from diagrams.onprem.database import Postgresql
from diagrams.programming.framework import Angular
from diagrams.programming.language import Python, Java
from diagrams.generic.os import Android, IOS

with Diagram("Tiramisu3-PR Architecture", show=False, direction="TB"):
    mobile_client = Mobile("Mobile Client\n(Ionic/Angular)")
    
    with Cluster("Frontend Layer"):
        frontend = Java("Java Frontend\n(Servlets)")
        frontend_components = [
            "SchedulesForLocationServlet",
            "WriteFavRouteServlet",
            "ReadFavRouteServlet",
            "StatusLogServlet",
            "ButtonLogServlet",
            "FocusLogServlet"
        ]
    
    with Cluster("Backend Layer"):
        with Cluster("Data Processing"):
            feed_grabber_paac = EC2("FeedGrabberPAAC")
            feed_grabber_mta = EC2("FeedGrabberMTA")
            observation_processor = EC2("ObservationProcessor")
            dynamo_cleaner = EC2("DynamoCleaner")
        
        with Cluster("Alarm System"):
            alarm_processor = EC2("AlarmProcessor")
            aws_send_email = EC2("AWSSendEmail")
    
    with Cluster("Prediction Layer"):
        predictor = Python("Route Predictor\n(Random Forest)")
    
    with Cluster("Data Storage"):
        dynamodb = Dynamodb("DynamoDB\n(Real-time Data)")
        postgres = Postgresql("PostgreSQL\n(User Logging)")
    
    with Cluster("External Services"):
        onebusaway = EC2("OneBusAway")
        transportation_agencies = EC2("Transportation\nAgencies")
    
    mobile_client >> frontend
    frontend >> onebusaway
    frontend >> dynamodb
    frontend >> postgres
    
    transportation_agencies >> feed_grabber_paac
    transportation_agencies >> feed_grabber_mta
    
    feed_grabber_paac >> SQS("SQS Queue")
    feed_grabber_mta >> SQS("SQS Queue")
    SQS("SQS Queue") >> observation_processor
    
    observation_processor >> dynamodb
    dynamo_cleaner >> dynamodb
    
    alarm_processor >> aws_send_email
    aws_send_email >> mobile_client
    
    predictor >> dynamodb
    predictor >> postgres