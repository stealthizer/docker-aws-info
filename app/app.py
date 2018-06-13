#!/usr/bin/env python3
from flask import Flask, render_template
import boto3
import requests


app = Flask(__name__)

def describe_instances(instanceId):
    client = boto3.client('ec2', region_name='eu-west-1')
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
        response = requests.get('http://169.254.169.254/latest/meta-data/spot/termination-time')
        if response.status_code == 404:
            terminationNotice = 'no termination notice'
            status = None
        else:
            terminationNotice = response.text
            status = 'terminate'
    print(status)
    print(terminationNotice)
    return render_template('instance_template.html', instanceId=instanceId, instanceType=instanceType,
                           instanceLifecycle=instanceLifecycle, terminationNotice=terminationNotice, status=status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
