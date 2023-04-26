
# Import necessary libraries
import boto3
from botocore.exceptions import ClientError

# Define global variables
QUICKSIGHT_REGION = 'us-east-1'
QUICKSIGHT_ACCOUNT_ID = '123456789012'
QUICKSIGHT_DATA_SOURCE_NAME = 'ecommerce_transactions'
QUICKSIGHT_DATA_SET_NAME = 'ecommerce_transactions'
QUICKSIGHT_GROUP_NAME = 'ecommerce_users'

# Create a QuickSight client
quicksight = boto3.client('quicksight', region_name=QUICKSIGHT_REGION)

# Create a data source using Amazon S3
def create_data_source(bucket_name, object_key):
    try:
        response = quicksight.create_data_source(
            AwsAccountId=QUICKSIGHT_ACCOUNT_ID,
            DataSourceId=QUICKSIGHT_DATA_SOURCE_NAME,
            Name=QUICKSIGHT_DATA_SOURCE_NAME,
            Type='S3',
            DataSourceParameters={
                'S3Parameters': {
                    'ManifestFileLocation': {
                        'Bucket': bucket_name,
                        'Key': object_key
                    }
                }
            },
            Permissions=[
                {
                    'Principal': 'arn:aws:quicksight:us-east-1:123456789012:group/' + QUICKSIGHT_GROUP_NAME,
                    'Actions': [
                        'quicksight:DescribeDataSource',
                        'quicksight:DescribeDataSourcePermissions',
                        'quicksight:PassDataSource',
                        'quicksight:UpdateDataSource',
                        'quicksight:DeleteDataSource'
                    ]
                }
            ],
            SslProperties={
                'DisableSsl': False
            },
            Tags=[
                {
                    'Key': 'Source',
                    'Value': 'e-commerce transactions'
                }
            ]
        )
        return response['Arn']
    except ClientError as e:
        return e.response['Error']['Message']

# Create a data set using the QuickSight data source
def create_data_set():
    try:
        response = quicksight.create_data_set(
            AwsAccountId=QUICKSIGHT_ACCOUNT_ID,
            DataSetId=QUICKSIGHT_DATA_SET_NAME,
            Name=QUICKSIGHT_DATA_SET_NAME,
            PhysicalTableMap={
                "TransactionTable": {
                    "CustomSql": {
                        "DataSourceArn": "arn:aws:quicksight:us-east-1:123456789012:datasource/" + QUICKSIGHT_DATA_SOURCE_NAME,
                        "Name": "TransactionTable",
                        "SqlQuery": "SELECT * FROM transactions"
                    }
                }
            },
            Permissions=[
                {
                    'Principal': 'arn:aws:quicksight:us-east-1:123456789012:group/' + QUICKSIGHT_GROUP_NAME,
                    'Actions': [
                        'quicksight:DescribeDataSet',
                        'quicksight:DescribeDataSetPermissions',
                        'quicksight:PassDataSet',
                        'quicksight:UpdateDataSet',
                        'quicksight:DeleteDataSet',
                        'quicksight:UpdateDataSetPermissions',
                        'quicksight:CreateIngestion',
                        'quicksight:GetIngestion',
                        'quicksight:CancelIngestion',
                        'quicksight:ListIngestions'
                    ]
                }
            ],
            Tags=[
                {
                    'Key': 'Source',
                    'Value': 'e-commerce transactions'
                }
            ]
        )
        return response['Arn']
    except ClientError as e:
        return e.response['Error']['Message']

# Create a dashboard using the QuickSight data set
def create_dashboard():
    try:
        response = quicksight.create_dashboard(
            AwsAccountId=QUICKSIGHT_ACCOUNT_ID,
            DashboardId=QUICKSIGHT_DATA_SOURCE_NAME,
            Name=QUICKSIGHT_DATA_SOURCE_NAME,
            Permissions=[
                {
                    'Principal': 'arn:aws:quicksight:us-east-1:123456789012:group/' + QUICKSIGHT_GROUP_NAME,
                    'Actions': [
                        'quicksight:DescribeDashboard',
                        'quicksight:DescribeDashboardPermissions',
                        'quicksight:PassDashboard',
                        'quicksight:UpdateDashboard',
                        'quicksight:DeleteDashboard',
                        'quicksight:UpdateDashboardPermissions',
                        'quicksight:QueryDashboard'
                    ]
                }
            ],
            SourceEntity={
                'SourceTemplate': {
                    'DataSetReferences': [
                        {
                            'DataSetArn': 'arn:aws:quicksight:us-east-1:123456789012:dataset/' + QUICKSIGHT_DATA_SET_NAME,
                            'DataSetPlaceholder': 'transactions',
                            'Arn': 'arn:aws:quicksight:us-east-1:123456789012:template/e-commerce'
                        }
                    ]
                }
            },
            Tags=[
                {
                    'Key': 'Source',
                    'Value': 'e-commerce transactions'
                }
            ]
        )
        return response['DashboardId']
    except ClientError as e:
        return e.response['Error']['Message']

# Main function
def main():
    s3_bucket_name = 'ecommerce-transactions-bucket'
    s3_object_key = 'transactions.csv'
    data_source_arn = create_data_source(s3_bucket_name, s3_object_key)
    data_set_arn = create_data_set()
    dashboard_id = create_dashboard()
    print('QuickSight Dashboard created with ID:', dashboard_id)

# Call the main function
if __name__ == "__main__":
    main()
