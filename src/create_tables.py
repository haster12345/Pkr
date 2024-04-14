from local_db import dynamodb

def create_hand_info_table():
    """
    All the stages of a hand are identified with a hand number we just create a table 
    with hand number as a partition key and hand as sort key.

    Possible Sort Keys:
    hand#action
    hand#pre_flop#flop
    hand

    Maybe all of this can be done when building inserting rules

    Main query patterns:
    - for a hand what was the given action?
    - What hands did we have for these actions?

    """
    table = dynamodb.create_table(

        AttributeDefinitions=[
            { 
                'AttributeName': 'hand_number',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'hand',
                'AttributeType': 'S'
            }
            ],
        TableName='hand_info',
        KeySchema=[
            {
                    'AttributeName': 'hand_number',
                    'KeyType': 'HASH' 
            },
            {
                    'AttributeName': 'hand',
                    'KeyType': 'RANGE' 
            }
            ],
        BillingMode='PAY_PER_REQUEST'
    )

    table.wait_until_exists()

    return

