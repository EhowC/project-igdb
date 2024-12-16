import json
import boto3
import urllib3
import datetime

## Firehose name, client ID and, secret key need to be filled in.
FIREHOSE_NAME = <<firehose name>>

def lambda_handler(event, context):
    http = urllib3.PoolManager()
    r = http.request('POST', 'https://api.igdb.com/v4/games',
                     body='fields id,name,first_release_date,total_rating,total_rating_count; where total_rating_count >= 50 & release_dates.platform = (4,18,19,20,21,37,130,137,159,416); sort first_release_date asc; limit 500;',
                     headers={'Client-ID': <<client id>>,'Authorization': 'Bearer <<secret key>>'})
    
    r_dict = json.loads(r.data.decode(encoding='utf-8', errors='strict'))
    
    processed_dict = {}
    records_to_push = []

    # Since the data is saved as a long array of JSONs, we need to process the file based on the length of the array.
    for i in range(len(r_dict)):
        processed_dict['id'] = r_dict[i]['id']
        processed_dict['name'] = r_dict[i]['name']
        processed_dict['first_release_date'] = datetime.datetime.utcfromtimestamp(r_dict[i]['first_release_date']).strftime('%Y-%m-%d %H:%M:%S')
        processed_dict['total_rating'] = r_dict[i]['total_rating']
        processed_dict['total_rating_count'] = r_dict[i]['total_rating_count']
        processed_dict['last_updated'] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        msg = str(processed_dict) + '\n'
        records_to_push.append({'Data': msg})

    msg = str(processed_dict) + '\n'
    fh = boto3.client('firehose')
    reply = fh.put_record_batch(
        DeliveryStreamName=FIREHOSE_NAME,
        Records = records_to_push
    )

    return reply
