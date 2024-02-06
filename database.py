import boto3
from botocore.exceptions import NoCredentialsError
from acesskey import aws_access_key_id
from acesskey import aws_secret_access_key

# Connect to DynamoDB Local
dynamodb = boto3.resource(
    'dynamodb',  # Local DynamoDB endpoint
    region_name='eu-west-2',  # Specify any region (required by Boto3)
    aws_access_key_id= aws_access_key_id,  # Dummy credentials
    aws_secret_access_key= aws_secret_access_key  # Dummy credentials
)

print(dynamodb)

# Define table schema
table_name = 'TestTable'
print(1)
table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': 'ID',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'ID',
            'AttributeType': 'N'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# print(table)
# Wait until the table exists
table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

# Perform operations
try:
    # Put an item
    table.put_item(Item={'ID': 1, 'Name': 'John'})

    # Get an item
    response = table.get_item(Key={'ID': 1})
    print(1)
    print(response['Item'])

    # Delete the table (cleanup)
    table.delete()
except NoCredentialsError:
    print('Unable to connect to DynamoDB Local. Please make sure it is running and credentials are provided.')
