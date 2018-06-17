#!/usr/bin/env python3
from flask import Flask, render_template
import boto3
import requests


app = Flask(__name__)
region = 'eu-west-1'

def get_termination_time_demo():
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table('terminateDB')
    try:
        response = table.scan(Limit=1)
        return response['Items'][0]['termination']
    except Exception as e:
        print(e)
        return None

def get_termination_notice_metadata():
    response = requests.get('http://169.254.169.254/latest/meta-data/spot/termination-time')
    if response.status_code == 404:
        return None
    else:
        return response.text

def get_termination_notice():
    terminationNotice_metadata = get_termination_notice_metadata()
    terminationNotice_demo = get_termination_time_demo()
    if terminationNotice_demo is not None or terminationNotice_metadata is not None:
        if terminationNotice_metadata is not None:
            return terminationNotice_metadata
        else:
            return terminationNotice_demo
    else:
        return None

def describe_instances(instanceId):
    client = boto3.client('ec2', region_name=region)
    try:
        instances = client.describe_instances(InstanceIds=[instanceId])
        return instances
    except Exception as e:
        return e

def get_instance_id():
    response = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
    data = response.text
    return data

@app.route('/')
def aws_info():
    instanceId = get_instance_id()
    instance_data = describe_instances(instanceId)['Reservations'][0]['Instances'][0]
    instanceType = instance_data['InstanceType']
    terminationNotice = ''
    status = ''
    try:
        instanceLifecycle = instance_data['InstanceLifecycle']
    except:
        instanceLifecycle = 'normal'
    else:
        result = get_termination_notice()
        if result is None:
            terminationNotice = 'No termination notice'
            status = None
        else:
            terminationNotice = result
            status = "terminate"

    print(status)
    print(terminationNotice)
    return render_template('instance_template.html', instanceId=instanceId, instanceType=instanceType,
                           instanceLifecycle=instanceLifecycle, terminationNotice=terminationNotice, status=status)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)