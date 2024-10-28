import boto3

s3 = boto3.resource('s3')
bucket_name = 'example-bucket9432'
object = s3.Object(bucket_name, 'aws.png')

object.download_file('example2.png')
