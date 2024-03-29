from local_db import dynamodb

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
