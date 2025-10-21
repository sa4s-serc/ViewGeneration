from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.ml import Rekognition
from diagrams.programming.language import Python
from diagrams.aws.integration import SNS
from diagrams.aws.general import User as AWSUser
from diagrams.aws.iot import IotCamera

with Diagram("JavaWatch Architecture", show=False, direction="TB"):
    user = AWSUser("User")

    with Cluster("JavaWatch System"):
        raspberry_pi = IotCamera("Raspberry Pi with Camera")
        s3_bucket = S3("Image Bucket")

        with Cluster("Serverless Functions"):
            lambda_check_image = Lambda("checkImage.py")
            lambda_label_check = Lambda("labelCheck.js")

        rekognition = Rekognition("Amazon Rekognition")
        drs_service = AWSUser("Amazon DRS")
        website = Python("JavaWatch Website")

    user >> website >> raspberry_pi
    raspberry_pi >> s3_bucket
    s3_bucket >> SNS("S3 Event") >> lambda_check_image
    lambda_check_image >> rekognition
    rekognition >> lambda_label_check
    lambda_label_check >> drs_service