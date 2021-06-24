import json
import boto3
import os

REGION = os.environ['AWS_REGION']

print('Loading function')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    
    client = boto3.client('lambda', region_name=REGION)
    ec2 = boto3.client('ec2', region_name=REGION)
    rds = boto3.client('rds', region_name=REGION)

    # EC2 Shutdown
    resEc2Describe = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )['Reservations']

    ec2_list = list()

    for ins in resEc2Describe:
        for instance in ins.get('Instances', []):
            ec2_id = instance.get('InstanceId')

            input_event = { "message": ec2_id }
            Ec2Payload = json.dumps(input_event)

            ec2response = client.invoke(
                FunctionName='AWSCostSaver-Ec2Shutdown',
                InvocationType='Event', 
                Payload=Ec2Payload
            )


    # RDS Shutdown
    resRdsInstance = rds.describe_db_instances()
    v_readReplica=[]
    for i in resRdsInstance['DBInstances']:
        readReplica=i['ReadReplicaDBInstanceIdentifiers']
        v_readReplica.extend(readReplica)

    for db in resRdsInstance['DBInstances']:
        if db['Engine'] not in ['aurora-mysql','aurora-postgresql']:
            if db['DBInstanceIdentifier'] not in v_readReplica and len(db['ReadReplicaDBInstanceIdentifiers']) == 0:
                if db['DBInstanceStatus'] == 'available':
                    rds_id = db['DBInstanceIdentifier']
                    engine = db['Engine']

                    input_event = { "Engine": engine, "message": rds_id }
                    RdsPayload = json.dumps(input_event)

                    rdsresponse = client.invoke(
                        FunctionName='AWSCostSaver-RdsShutdown',
                        InvocationType='Event', 
                        Payload=RdsPayload
                    )

    resRdsCluster = rds.describe_db_clusters()
    for clu in resRdsCluster['DBClusters']:
        if clu['Status'] == 'available':
            rds_id = clu['DBClusterIdentifier']
            engine = clu['Engine']

            input_event = { "Engine": engine, "message": rds_id }
            RdsPayload = json.dumps(input_event)

            rdsresponse = client.invoke(
                FunctionName='AWSCostSaver-RdsShutdown',
                InvocationType='Event', 
                Payload=RdsPayload
            )


    