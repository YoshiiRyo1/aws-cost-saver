import json
import boto3
import os

REGION = os.environ['AWS_REGION']

print('Loading function')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    instanceid = event['message']

    ec2 = boto3.client('ec2', region_name=REGION)
    ec2.stop_instances(InstanceIds=[instanceid])
    print('stopped your instance: ' + str(instanceid))


