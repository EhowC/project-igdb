import sys
import awswrangler as wr

#TO-DO: Figure out how to embed variables in the SQL.
MY_DATABASE = 'igdb'
MY_TABLE_NAME = 'nintendo_games_parquet_tbl'

# if any rows are duplicate, the check returns a number > 0
# need to fill in database & table
DUPLICATE_DQ_CHECK = f"""
    SELECT
        count(1) as duplicates
    FROM(
        SELECT 
            id
          , count(1)
              as entries
        FROM <database>.<table_name>
        group by
            id
        )
    where entries > 1
    ;
    """

# run the quality check
df = wr.athena.read_sql_query(sql=DUPLICATE_DQ_CHECK, database="igdb")

# exit if we get a result > 0
# else, the check was successful
if df['duplicates'][0] > 0:
    sys.exit('Results returned. Quality check failed.')
else:
    print('Quality check passed.')

