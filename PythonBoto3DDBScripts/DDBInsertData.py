import boto3

db = boto3.resource('dynamodb')
table = db.Table('Employee')

table.put_item(
    Item = {
        "emp_id":'2',
        "name":'testName'
    }
)

