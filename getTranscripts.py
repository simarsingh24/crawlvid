import json
import boto3


def utf8len(s):
    return len(s.encode('utf-8'))
    
def truncateUTF8length(unicodeStr, maxsize):
    return str(unicodeStr.encode("utf-8")[:maxsize], "utf-8", errors="ignore")


def lambda_handler(event, context):
    ACCESS_KEY_ID = 'AKIAIP7E6DYJUA6FZXEQ'
    ACCESS_SECRET_KEY = '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'
    BUCKET_NAME = 'seektube'
    
    s3 = boto3.client("s3",aws_access_key_id=ACCESS_KEY_ID,aws_secret_access_key=ACCESS_SECRET_KEY)
    comprehend  = boto3.client('comprehend',aws_access_key_id=ACCESS_KEY_ID,aws_secret_access_key=ACCESS_SECRET_KEY,region_name='us-east-1')
    json_name=event["queryStringParameters"]['id'] +'.json'
    json_object=s3.get_object(Bucket=BUCKET_NAME,Key= json_name)
    
    json_reader=json_object['Body'].read()
    json_data=json.loads(json_reader)
    final_json=json_data["results"]["items"]
    transcript=json_data["results"]["transcripts"][0]['transcript']
    
    transcript_length = utf8len(transcript);
    
    if (transcript_length > 5000):
        transcript = truncateUTF8length(transcript, 5000)
    
    sentiment = comprehend.detect_sentiment(Text=transcript, LanguageCode='en')
    message = {
        "json": final_json,
        "transcript": transcript,
        "sentiment": sentiment
    }
    
    
    return {
        'statusCode': 200,
        'body': json.dumps({"status":message}),
         "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        }
    }
