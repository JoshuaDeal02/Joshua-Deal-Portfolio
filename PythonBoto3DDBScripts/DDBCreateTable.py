import boto3

def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName = 'newTableName',
        KeySchema = [
            {
                'AttributeName':'emp_id',
                'KeyType':'HASH'
            }
        ],
        AttributeDefinitions = [
            {
                'AttributeName':'emp_id',
                'AttributeType':'S'
            }
        ],
        ProvisionedThroughput =
            {
                'ReadCapacityUnits':1,
                'WriteCapacityUnits':1
            }

    )
    return table


if __name__ == '__main__':
    table = create_table()
    print(table.table_status)
