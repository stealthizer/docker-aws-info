#!/usr/bin/env python3
from flask import Flask
import boto3
import requests


app = Flask(__name__)

def describe_instances(instance_id):
    client = boto3.client('ec2', region_name='eu-west-1')
    try:
        instances = client.describe_instances(InstanceIds=[instance_id])
        return instances
    except Exception as e:
        return e

def get_instance_id():
    response = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
    data = response.text
    print(data)
    return data

@app.route('/')
def aws_info():
    instance_id = get_instance_id()
    instance_data = describe_instances(instance_id)['Reservations'][0]['Instances'][0]
    instanceType = instance_data['InstanceType']
    instanceLifecycle = instance_data['InstanceLifecycle']
    html_code = '<table><td><tr>' + instance_id + '<br>' + instanceType + '<br>' + instanceLifecycle + '</tr></td></table>'
    return html_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
