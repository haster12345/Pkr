import boto3
from botocore.exceptions import NoCredentialsError

# Connect to DynamoDB Local
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000', 
    region_name='eu-west-2', 
    aws_access_key_id='anything',  
    aws_secret_access_key='anything'
)


table_name = 'TableInfo'
table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': 'hand_number',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'ID',
            'AttributeType': 'N'
        },
        {
            
        }
    ]
)

# Wait until the table exists
table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

# Perform operations
try:
    # Put an item
    table.put_item(Item={'ID': 1, 'Name': 'John'})

    # Get an item
    response = table.get_item(Key={'ID': 1})
    print(response['Item'])

    # Delete the table (cleanup)
    table.delete()
except NoCredentialsError:
    print('Unable to connect to DynamoDB Local. Please make sure it is running and credentials are provided.')
