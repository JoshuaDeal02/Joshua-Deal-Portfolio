import boto3

db = boto3.resource('dynamodb')
table = db.Table('Employee')

with table.batch_writer() as batch:
    batch.put_item(
        Item = {
            'emp_id':'3',
            'name':'testname'
        }
    )
    batch.put_item(
        Item = {
            'emp_id':'4',
            'name':'testUserAlso'
        }
    )