import boto3

s3 = boto3.resource('s3')

destination = 'first-bucket43'
source = {
    'Bucket':'example-bucket9432',
    'Key':'aws.png'
}

s3.meta.client.copy(source, destination, 'copy.png')

