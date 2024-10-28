import boto3

db = boto3.client('dynamodb')

response = db.create_backup(
    TableName = 'Employee',
    BackupName = 'EmployeeBackup'
)

print(response)