import sys
import boto3

client = boto3.client('athena')

# Database, table names, and S3 buckets need to be added in
SOURCE_TABLE_NAME = '<source table>'
NEW_TABLE_NAME = '<parquet table name'
NEW_TABLE_S3_BUCKET = '<parquet S3 bucket>'
MY_DATABASE = '<database name>'
QUERY_RESULTS_S3_BUCKET = '<Athena results S3 bucket>'

# Refresh the table
queryStart = client.start_query_execution(
    QueryString = f"""
    CREATE TABLE {NEW_TABLE_NAME} WITH
    (external_location='{NEW_TABLE_S3_BUCKET}',
    format='PARQUET',
    write_compression='SNAPPY',
    partitioned_by = ARRAY['release_year'])
    AS
    SELECT
        id
      , first_release_date
      , name
      , total_rating
      , total_rating_count
      , last_updated
      , SUBSTRING(cast(first_release_date as varchar(8)), 1, 4) 
          AS release_year
    FROM(
        SELECT
            *
          , row_number() over (partition by id order by last_updated desc) = 1 
              as most_recent_entry
        FROM "{MY_DATABASE}"."{SOURCE_TABLE_NAME}"
        )
    where most_recent_entry
    ;
    """,
    QueryExecutionContext = {
        'Database': f'{MY_DATABASE}'
    }, 
    ResultConfiguration = { 'OutputLocation': f'{QUERY_RESULTS_S3_BUCKET}'}
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
