
import boto3

class Athena:
    def __init__(self, database, s3_output):
        self.client = boto3.client('athena')
        self.database = database
        self.s3_output = s3_output
        
    def query(self, query, s3_output=None):
        if not s3_output:
            s3_output = self.s3_output
        
        response = self.client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': self.database
            },
            ResultConfiguration={
                'OutputLocation': s3_output,
            }
        )
        
        query_execution_id = response['QueryExecutionId']
        print(f"Query '{query_execution_id}' started...")
        
        return query_execution_id

