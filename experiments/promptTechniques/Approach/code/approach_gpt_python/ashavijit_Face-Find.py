from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.onprem.client import User
from diagrams.onprem.network import Internet

with Diagram("Face-Find Architecture", show=False, direction="LR"):
    user = User("User")
    
    with Cluster("Front-End"):
        bootstrap_css = Custom("Bootstrap CSS", "./bootstrap-icon.png")
        rtl_css = Custom("RTL CSS", "./rtl-icon.png")
        scss_components = [
            Custom("Grid", "./grid-icon.png"),
            Custom("Forms", "./forms-icon.png"),
            Custom("Buttons", "./buttons-icon.png"),
            Custom("Nav", "./nav-icon.png"),
            Custom("Card", "./card-icon.png")
        ]

    with Cluster("Django Backend"):
        with Cluster("Models"):
            missing_person_model = Custom("MissingPerson", "./model-icon.png")
            reported_person_model = Custom("ReportedPerson", "./model-icon.png")
        
        with Cluster("Views"):
            list_view = Custom("ListView", "./view-icon.png")
            create_view = Custom("CreateView", "./view-icon.png")
            update_view = Custom("UpdateView", "./view-icon.png")
            delete_view = Custom("DeleteView", "./view-icon.png")
        
        with Cluster("Forms"):
            missing_person_form = Custom("MissingPersonForm", "./form-icon.png")
            reported_person_form = Custom("ReportedPersonForm", "./form-icon.png")
        
        azure_face_api = Custom("Azure Face API", "./api-icon.png")
        email_service = Custom("Email Notification", "./email-icon.png")

    with Cluster("Database"):
        db = RDS("PostgreSQL")

    user >> Internet("Browser") >> bootstrap_css
    user >> Internet("Browser") >> rtl_css
    user >> Internet("Browser") >> scss_components

    bootstrap_css >> list_view
    rtl_css >> list_view
    for component in scss_components:
        component >> list_view

    list_view >> missing_person_model
    list_view >> reported_person_model

    create_view >> missing_person_model
    update_view >> missing_person_model
    delete_view >> missing_person_model

    create_view >> reported_person_model
    update_view >> reported_person_model
    delete_view >> reported_person_model

    missing_person_form >> create_view
    reported_person_form >> create_view

    list_view >> azure_face_api
    list_view >> email_service

    missing_person_model >> db
    reported_person_model >> db