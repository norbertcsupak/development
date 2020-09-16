import boto3
import click
import os
import sys
import json


with open('credentials.json', 'r') as fd:
    credentials = json.loads(fd.read())


s3 = boto3.resource('s3',
     endpoint_url=credentials['endpoint_url'],
     aws_access_key_id=credentials['access_key'],
     aws_secret_access_key=credentials['secret_key'])

#session = boto3.Session(profile_name='shotty')
#ec2 = session.resource('ec2')



@click.group()
def cli():

    """Shotty manages S3 """

@cli.group('bucket')
def bucket():
    """ commands  for buckets """

@bucket.command('list')
#@click.option('--project',default=None, help="only instances for projects eg: tag Project:<name>")
def list_buckets():
    "List all S3 buckets "

    response = s3.list_buckets()
    for item in response['Buckets']:
        print(item['CreationDate'], item['Name'])
        
    return


@bucket.command('create')
@click.option('--bucket-name',default=None, help="name of the  bucket to create")
def create_bucket(bucket_name):
    "Create S3 bucket"

    bucket = s3.Bucket(bucket_name)
    bucket.create()

    return

@bucket.command('delete')
@click.option('--bucket-name',default=None, help="name of the  bucket to delete")
def create_bucket(bucket_name):
    "Delete S3 bucket"

    bucket = s3.Bucket(bucket_name)
    bucket.delte()

    return




@cli.group('object')
def object():
    """ commands  for objects """

@object.command('list')
@click.option('--bucket-name',default=None, help="name of the  bucket to  list")
def list_snapshot(bucket_name):
    "List S3 bucket objects"

    response = s3.list_objects_v2(Bucket=bucket_name)
    for item in response['Contents']:
        print(item['Key'])

    return


@cli.group('instances')
def instances():
    """ Commands for instances """

@instances.command('list')
@click.option('--project',default=None, help="only instances for projects eg: tag Project:<name>")
def list_instances(project):
    "List all the instances depends on options "

    instances = filter_instances(project)

    for i in  instances:
        tags = { t['Key']:t['Value'] for t in i.tags or []}
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project','<no  project>')
            )))
    return


if __name__ == '__main__':
    cli()
