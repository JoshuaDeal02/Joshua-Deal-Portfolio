import boto3

s3 = boto3.resource('s3')
bucket_name = "example-bucket9432"
bucket = s3.Bucket(bucket_name)

for object in bucket.objects.all():
    print(object.key)