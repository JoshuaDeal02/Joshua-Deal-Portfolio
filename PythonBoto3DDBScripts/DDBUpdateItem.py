import boto3
from pprint import pprint
from decimal import Decimal

def update_item(emp_id, rating, plot, dynamodb=None):
    """
    Args:
        emp_id (str): The ID of the employee (or other entity) to update in the table.
        rating (Decimal): The rating to be applied to the entity. (Not currently used in the update).
        plot (str): A plot or description associated with the entity. (Not currently used in the update).
        dynamodb (boto3.resource, optional): A DynamoDB resource. If not provided, a new resource is created.

    Returns:
        dict: The response from DynamoDB's `update_item` operation, containing updated item attributes.

    Example:
        >>> update_response = update_item("Sherlock Holmes", Decimal(4.5), "Example Updated")
        >>> pprint(update_response)

    Note:
        This function updates the `title` attribute of the item. Modify the `UpdateExpression` and 
        `ExpressionAttributeValues` for more complex updates.
    """
    dynamodb = boto3.resource('dynamodb')
    print(type(dynamodb))
    table = dynamodb.Table('newTableName')

    response = table.update_item(
        Key={
            'emp_id': emp_id
        },
        UpdateExpression="set info.genres =:r",
        ExpressionAttributeValues={
            ':r': 'Example'
        },
        ReturnValues='UPDATED_NEW'
    )

    return response

if __name__ == '__main__':
    update_response = update_item("2005", Decimal(4.5), "Example Updated")
    pprint(update_response)
