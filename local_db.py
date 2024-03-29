import boto3
from botocore.exceptions import NoCredentialsError

# Connect to DynamoDB Local
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000', 
    region_name='asdf', 
    aws_access_key_id='asdf',  
    aws_secret_access_key='asdf'
)

table = dynamodb.create_table(
        AttributeDefinitions=[
            { 
            'AttributeName': 'hand_number',
            'AttributeType': 'N'
            },
        ],
        TableName='table_info',
        KeySchema=[
            {
                'AttributeName': 'hand_number',
                'KeyType': 'HASH' 
            },
        ],    
        ProvisionedThroughput={
        'ReadCapacityUnits': 123,
        'WriteCapacityUnits': 123
    }
)


table.wait_until_exists()
print(table.item_count)
