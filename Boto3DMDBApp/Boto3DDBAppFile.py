import boto3
import json
import pprint
from decimal import Decimal
from botocore.exceptions import ClientError

class DynamoDBTable:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = table_name
        self.table = self.dynamodb.Table(table_name)
        self.key_name = None
        self.key_type = None

    def load_table(self):
        """Load the table if it exists, handle table not found exception."""
        try:
            self.table.load()
            print(f"Table '{self.table_name}' loaded successfully.")
        except ClientError as e:
            print(e.response['Error']['Code'])
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                entry = input(f"The table '{self.table_name}' cannot be found. \nCreate a new table? (y/n): ")
                if entry.lower() == 'y':
                    self.create_table()
                else:
                    quit()

    def create_table(self):
        """Create a new DynamoDB table with user input."""
        key_name = input('Enter a name for the key: ')
        key_type = input('Enter a datatype for the key: ')
        read_cap = int(input('Enter the read capacity for the table: '))
        write_cap = int(input('Enter the write capacity for the table: '))
        
        self.table = self.dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {
                    'AttributeName': key_name,
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': key_name,
                    'AttributeType': key_type
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': read_cap,
                'WriteCapacityUnits': write_cap
            }
        )
        print('Creating Table...')
        self.table.wait_until_exists()
        print(f"Table '{self.table_name}' created successfully.")

    def fetch_key_info(self):
        """Fetch and store the key name and type from the table."""
        try:
            response = self.table.meta.client.describe_table(TableName=self.table_name)
            key_schema = response['Table']['KeySchema']
            attribute_definitions = response['Table']['AttributeDefinitions']
            
            for key in key_schema:
                if key['KeyType'] == 'HASH':
                    self.key_name = key['AttributeName']
            
            for attribute in attribute_definitions:
                if attribute['AttributeName'] == self.key_name:
                    self.key_type = attribute['AttributeType']
            print(f"Key Name: {self.key_name}")
            print(f"Key Type: {self.key_type}")
        except ClientError as e:
            print(f"Unable to fetch key info: {e.response['Error']['Message']}")

    def print_menu(self):
        print("MENU\n1 - Insert Record\n2 - Insert JSON File\n3 - Update Record\n4 - Delete Record\n5 - Fetch Record\n6 - Fetch Entire Database\n7 - Backup Table\n8 - Open New Table\n9 - Delete Table\n0 - Close Application")

    def core_loop(self):
        entry = True
        self.fetch_key_info()

        while entry != 0:
            self.print_menu()
            entry = int(input("\n\nEntry: "))
            match entry:
                case 1:
                    print("Insert a Record")
                    self.insert_record()
                case 2:
                    print("Insert a JSON File")
                    self.insert_json()
                case 3:
                    print("Update a Record")
                    self.update_record()
                case 4:
                    print("Delete a Record")
                    self.delete_record()
                case 5:
                    print("Fetch a Record")
                    self.fetch_record()
                case 6:
                    print("Fetch Whole Database")
                    self.fetch_database()
                case 7:
                    print("Backup Table")
                    self.backup_table()
                case 8:
                    print("Open New Table")
                    self.open_new_table()
                case 9:
                    print("Delete Table")
                    self.delete_table()
                case 0:
                    print("Close Application")
                    exit()
                case _:
                    print("Entry must be 0-9")
            

    def insert_record(self):
        key_value = input("Key Value: ")
        try:
            response = self.table.get_item(
                Key={
                    self.key_name: key_value
                }
            )
            if 'Item' in response:
                print(f"Record with {self.key_name} = {key_value} exists.")
                return
        except ClientError as e:
            print(f"Error checking record: {e.response['Error']['Message']}")
            return False


        if self.key_type == 'i':
            key_value = int(key_value)

        attribute_name = input("Attribute Name: ")
        data_value = input("Attribute Value: ")
        data_type = input("String or Integer? (s/i): ")

        while data_type not in ['s', 'i']:
            data_type = input("Attributes must be either an Integer or a String. (s/i): ")

        if data_type == 'i':
            data_value = int(data_value)

        
        item = {
            self.key_name: key_value,
            attribute_name: data_value
        }

        entry = input("Would you like to add more attributes? (y/n): ")
        if entry.lower() == 'y':
            self.add_attributes(item)

        
    
    def insert_json(self):
        file_name = input("Enter the name of the JSON file (with extention): ")
        with open(file_name) as json_file:
            data_list = json.load(json_file, parse_float=Decimal)
            for item in data_list:
                self.table.put_item(Item=item)
                try:
                    print(f"Inserted item: {item}")
                except ClientError as e:
                    print(f"Error inserting item: {e.response['Error']['Message']}")


    def update_record(self):
        attr_name = input("Enter the name of the attribute to change: ")
        attr_val = input(f"Enter the new value for {attr_name}: ")
        key_value = input("Enter the key for the record: ")

        try:
            response = self.table.update_item(
                Key={
                    self.key_name: key_value
                },
                UpdateExpression=f"set {attr_name} = :val",
                ExpressionAttributeValues={
                    ':val': attr_val
                },
                ReturnValues="UPDATED_NEW"
            )
            print(f"Record updated successfully: {response['Attributes']}")
        except ClientError as e:
            print(f"Error updating the record: {e.response['Error']['Message']}")

        
        

    def add_attributes(self, item):
        entry = 'y'
        while entry.lower() == 'y':

            new_attr_name = input("Enter new attribute name: ")
            new_attr_value = input(f"Enter value for '{new_attr_name}': ")
            new_attr_type = input("String or Integer? (s/i): ")

            while new_attr_type not in ['s', 'i']:
                new_attr_type = input("Attribute must be either an Integer or a String. (s/i): ")

            if new_attr_type == 'i':
                new_attr_value = int(new_attr_value)

            
            item[new_attr_name] = new_attr_value

            entry = input("Would you like to add more attributes? (y/n): ")
           
        self.table.put_item(Item=item)

    def delete_record(self):
        key_value = input("Enter the key for the record to be deleted: ")
        try:
            response = self.table.delete_item(
                Key={
                    self.key_name: key_value
                }
            )
            print(f"Record with {self.key_name} = {key_value} deleted successfully.")
            print("Response:", response)
        except ClientError as e:
            print(f"Error deleting record: {e.response['Error']['Message']}")
    
    def fetch_record(self):
        key_value = input("Enter the key for the record to be fetched: ")
        response = self.table.get_item(
            Key = {
                self.key_name: key_value
            }
        )
        print(response)

    def open_new_table(self):
        try:
            self.table_name = input("Enter the name of the new table: ")
            self.table = self.dynamodb.Table(self.table_name)
            # table.load is run to throw an error if the table does not exist
            self.table.load()
            print(f"Successfully opened table '{self.table_name}'.")

        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            print(f"Error: The table '{self.table_name}' does not exist.")
        except ClientError as e:
            print(f"ClientError: {e.response['Error']['Message']}")
    
    def fetch_database(self):
        try:
            response = self.dynamodb.describe_table(
                TableName = self.table_name
            )
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            print(f"Error: The table '{self.table_name}' does not exist.")
        pprint(response)

    def backup_table(self):
        backup_name = input("Enter the name for the backup table: ")
        response = self.dynamodb.create_backup(
            TableName = self.table_name,
            BackupName = backup_name
        )
        print(response)

    def delete_table(self):
        entry = input(f"Type 'delete' to delete {self.table_name}")
        if entry == 'delete':
            try:
                response = self.table.delete()
                print(f"Table '{self.table_name}' deleted successfully.")
            except ClientError as e:
                print(f"Error deleting table: {e.response['Error']['Message']}")
            exit()



def main():
    table_name = input("Enter a table to open or create: ")
    dynamo_table = DynamoDBTable(table_name)
    dynamo_table.load_table()
    dynamo_table.core_loop()


if __name__ == '__main__':
    main()
