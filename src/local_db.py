import boto3

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://dynamodb-local:8000', 
    region_name='asdf', 
    aws_access_key_id='asdf',  
    aws_secret_access_key='asdf'
)

