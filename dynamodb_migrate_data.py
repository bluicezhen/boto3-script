import boto3


def export_data(table_name, dynamodb_src, dynamodb_des):
    source_table = dynamodb_src.Table(table_name)
    response = source_table.scan()
    data_to_migrate = response['Items']
    while 'LastEvaluatedKey' in response:
        response = source_table.scan(
            ExclusiveStartKey=response['LastEvaluatedKey'])
        data_to_migrate.extend(response['Items'])
    print(f'Total items to migrate: {response["ScannedCount"]}')

    destination_table = dynamodb_des.Table(table_name)
    i = 1
    for item in data_to_migrate:
        print(f'Migrating item {i}/{response["ScannedCount"]}')
        destination_table.put_item(Item=item)
        i += 1


if __name__ == "__main__":
    session_src = boto3.Session(region_name='us-east-1')
    session_des = boto3.Session(profile_name='test_1', region_name='us-east-1')

    dynamodb_src = session_src.resource('dynamodb')
    dynamodb_des = session_des.resource('dynamodb')

    export_data('DeviceSecretKeyTable', dynamodb_src, dynamodb_des)
