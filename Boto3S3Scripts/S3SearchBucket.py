import boto3

s3 = boto3.resource('s3')
bucket_name = "example-bucket9432"
bucket = s3.Bucket(bucket_name)
found = False
for object in bucket.objects.filter(Prefix = "aws"):
    print(object.key)
    found = True

if found == False:
    print('No objects found')