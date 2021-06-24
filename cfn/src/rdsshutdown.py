import json
import boto3
import os

REGION = os.environ['AWS_REGION']

print('Loading function')

rds = boto3.client('rds', region_name=REGION)

def cluster_shutdown(event):
    #clusterid = event['message']

    rds.stop_db_cluster(DBClusterIdentifier = event['message'])
    print('stopped your DB Cluster: ' + str(event['message']))

def instance_shutdown(event):
    rds.stop_db_instance(DBInstanceIdentifier = event['message'])
    print('stopped your DB Instace: ' + str(event['message']))

def lambda_handler(event, context):
    if event['Engine'] not in ['aurora-mysql','aurora-postgresql']:
        instance_shutdown(event)
    elif event['Engine'] in ['aurora-mysql','aurora-postgresql']:
        cluster_shutdown(event)
    else:
        print('Unknow Engine Type')

