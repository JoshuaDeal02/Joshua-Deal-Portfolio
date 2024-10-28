import boto3

s3 = boto3.resource("s3")
bucket_name = "example-bucket9432"
object_name = "aws.png"
object_summary = s3.ObjectSummary(bucket_name, object_name)

print(object_summary.bucket_name)
print(object_summary.key)