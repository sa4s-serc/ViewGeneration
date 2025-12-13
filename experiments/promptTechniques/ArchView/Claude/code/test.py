import boto3
import json
from botocore.exceptions import ClientError
# Create a Bedrock Runtime client in the AWS Region of your choice.
# client = boto3.client(service_name='bedrock-runtime',region_name='us-west-2',endpoint_url='https://bedrock.us-west-2.amazonaws.com')
client = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-west-2',
    aws_access_key_id='ASIA4N3EOZMEQIZ4SX2R',
    aws_secret_access_key='ebWTOvbUX7gj47al5NXqd/rkudcH2Fnhs2jUuv/r',
    aws_session_token="IQoJb3JpZ2luX2VjEJ3//////////wEaCXVzLWVhc3QtMSJIMEYCIQDTMpch/vAA4Yl207iec/Mg4tT6WYitLQJtNhsyIzi6SQIhAInRbdm+xNJTF6/w4sEw3pjrFE5QPLD52TZY3FSkA+utKpIDCGYQABoMODU0MzcyMzA1NjczIgxH4kBuCuXKDLaosA8q7wIA1rXRZUzLC4cpJJlP0c+v1Zd17jgj1uxoo14blHqeuQyKy9q61qDBIOAOoCTsvWS2IzhuIiOu+EMfWsdsxFD7zWWXH3K+WeBqmSnCG4OePPfMZZg6YDs/NIHhLI+RMIA6xSdodBkE91y8bOvezKaBQI0UaGnQ2PH5GquBtKwFCDokIiQE1SEvWju0uoknwt4jtdV6MzGy5e+yuiVhOxOumQ2RnXnRToMCUhcSSZia89VK3iQZBd3RAkhAO4k8n+c+CELU7uwzVBhYUiGHIdk5vlE5y6dhipmsv8e0sKwVL47kvbc1C8da+fapNI+r5MPwDS72kvdIcnvJDgR7hVK287Y4Y9sITboF+PD/nE/Afx2OAu3ZsLPwhi/gf/yRxSwIYCt92uKgLzmHwC5ISu9Iafdi175Ab3zl4tnTdDJh+uhLEfX9kwLq2bcvZ9qrfqBhGLSw9gZqFGIW2PtVdlKsIwd56BUG5AEfCjBGqXuzMOnD3MgGOqMBSA9EPSA6e787Cf2O1XcQSYE16D2TRcBUPHP7I2quOBPuw81h1ABnq6X9f6/iR8eFkI14CpPGALdRLgQkDi0lncpgJsVcyIs9BX7Nb71w4B7u8EM3lJIbMjq3XbjNYoaXLgvj6y6gTskOJ/0cZgE7BMV1AlML/TDAhUlnXOqNmDlUV256X/Tnt8jp3duCA/sCN64levQVgxlVTUhdZOw5YFNYpw=="
)
model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
prompt = "Hi AI"
# Format the request payload using the model's native structure.
native_request = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 512,
    "temperature": 0.5,
    "messages": [
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}],
        }
    ],
}
# Convert the native request to JSON.
request = json.dumps(native_request)
try:
    # Invoke the model with the request.
    response = client.invoke_model(modelId=model_id, body=request)
except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)
response = client.invoke_model(modelId=model_id, body=request)
# Parse the response
model_response = json.loads(response["body"].read())
# Extract the response text
response_text = model_response["content"][0]["text"]
print(response_text)









# export AWS_ACCESS_KEY_ID="ASIA4N3EOZME7FRCLX2I"
# export AWS_SECRET_ACCESS_KEY="TJ+FplUv5pebxSGT4GXfKKBFuIN0760RQaTVmJqo"
# export AWS_SESSION_TOKEN="IQoJb3JpZ2luX2VjEOT//////////wEaCXVzLWVhc3QtMSJHMEUCIQCciTd9MxOToMqkJLTwcLGaiInKeFqld+edOiTi6PWKaAIgd2urcmLxqyxioOOEbIDjNqN3vbMZN2g2EuA4ZfhuGyUqmwMIrf//////////ARAAGgw4NTQzNzIzMDU2NzMiDBQMIbroWxR6+p1HXSrvAvuZ0WOIRvEnxHdLTM4MeDuRHRklZIDWfrdJ79UMdBc4+/vHFcGD61X0n0ou8YHDI07GpZv4kW96G1vnhG/QnWtyWY1B7Uem6UsFuabZvsSzaNqtPjS6qX38HeqFNr/aiUQKLpLCc2NrCyq06sPUZ8ag3F4KR1kQq6FhHt1TzuKSSDxqYfFloq8XAOUZWb7IDPvo98XT1SfCuCZ/NHBXI99dgwbA/srrQNp/moQyk4JHvEiSVxmKNckIoYNGGme4CsBhcfvcG41U10aXlhcqzuynpzlTfRyFblZlRvzXgJQrvCOeJTThme0LMQ27puEdSjnzoK1zpR1QybPGcK6cOZxU1JP3vZjMs2uG1p2YQBwUjKLDTin+Qb5+obv0pc/l/yzxpWFGYbW1FCJAYNSL3jl9Am5hXV88ZSsjGJC7lwS50d4Q8uaRMoJ1uWUL+dO99l441/4zwTvUDEboVPHnkmMpDwfBU+oVwmIC924tPjMw6pHsyAY6pAFDZG7UTRMwSGfRNi+JL/Vv8Yd9KS+67JbESgFWYe9zIlZIDeRf7llcCHDki0VOF6e4sBai0tJw5OAA16IzC1KuOaN4hHW2tDi5zU4YkMVRU3cjb9N/czqSejrD+3nOrP1ioph03ShF04w+oSB9sqqY1KwsBhZQIKDh2qF6NC/Ox9bHeULdvLrf5d3GbWJypJTRcFHfikyRK63gaHVZXWeVsdHS5g=="