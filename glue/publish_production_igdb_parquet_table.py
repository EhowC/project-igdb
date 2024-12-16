import sys
import boto3
from datetime import datetime

QUERY_RESULTS_BUCKET = '<S3 bucket for Athan query results>'
MY_DATABASE = '<Athena database name>'
SOURCE_PARQUET_TABLE_NAME = '<parquet table to copy>'
NEW_PROD_PARQUET_TABLE_NAME = '<production table name>'
NEW_PROD_PARQUET_TABLE_S3_BUCKET = '<S3 bucket for production table>'

client = boto3.client('athena')

# Refresh the table
queryStart = client.start_query_execution(
    QueryString = f"""
    CREATE TABLE {NEW_PROD_PARQUET_TABLE_NAME} WITH
    (external_location='{NEW_PROD_PARQUET_TABLE_S3_BUCKET}/',
    format='PARQUET',
    write_compression='SNAPPY',
    partitioned_by = ARRAY['release_year'])
    AS
    SELECT
        *
    FROM "{MY_DATABASE}"."{SOURCE_PARQUET_TABLE_NAME}"
    ;
    """,
    QueryExecutionContext = {
        'Database': f'{MY_DATABASE}'
    }, 
    ResultConfiguration = { 'OutputLocation': f'{QUERY_RESULTS_BUCKET}'}
)

# list of responses
resp = ["FAILED", "SUCCEEDED", "CANCELLED"]

# get the response
response = client.get_query_execution(QueryExecutionId=queryStart["QueryExecutionId"])

# wait until query finishes
while response["QueryExecution"]["Status"]["State"] not in resp:
    response = client.get_query_execution(QueryExecutionId=queryStart["QueryExecutionId"])
    
# if it fails, exit and give the Athena error message in the logs
if response["QueryExecution"]["Status"]["State"] == 'FAILED':
    sys.exit(response["QueryExecution"]["Status"]["StateChangeReason"])

