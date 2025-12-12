from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.ml import Rekognition
from diagrams.aws.engagement import SES
from diagrams.aws.general import User
from diagrams.generic.os import Raspbian
from diagrams.onprem.client import Client

with Diagram("JavaWatch Architecture", show=False, direction="LR"):
    user = User("User")
    raspberry_pi = Raspbian("Raspberry Pi")
    s3_bucket = S3("S3 Bucket")
    lambda_check_image = Lambda("checkImage.py")
    rekognition = Rekognition("Amazon Rekognition")
    lambda_label_check = Lambda("labelCheck.js")
    drs = SES("Amazon DRS")
    website = Client("Static Website")

    raspberry_pi >> s3_bucket
    s3_bucket >> lambda_check_image
    lambda_check_image >> rekognition
    rekognition >> lambda_label_check
    lambda_label_check >> drs
    user >> website
    website >> drs