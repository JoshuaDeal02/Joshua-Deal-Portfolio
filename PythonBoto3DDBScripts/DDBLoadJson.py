import boto3
import json
from decimal import Decimal

def load_json(filesData, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('newTableName')

    for fileData in filesData:
        year = str(fileData['emp_id'])
        title = fileData['title']
        print("Adding Data: ", year, title)
        table.put_item(Item = fileData)

if __name__ == '__main__':
    with open('data.json') as json_file:
        data_list = json.load(json_file, parse_float=Decimal)

    load_json(data_list)