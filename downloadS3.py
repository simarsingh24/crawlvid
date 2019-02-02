import json
import boto3
from pytube import YouTube
import botocore.vendored.requests.packages.urllib3 as urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def lambda_handler(event, context):
    ACCESS_KEY_ID = 'AKIAIP7E6DYJUA6FZXEQ'
    ACCESS_SECRET_KEY = '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'
    BUCKET_NAME = 'seektube'
    

    yt_id=event["queryStringParameters"]['id']
    yt_url = "https://www.youtube.com/watch?v=" + yt_id
    yt = YouTube(yt_url)
    stream = yt.streams.filter(progressive=True, file_extension="mp4").all()[-1]
    key = yt_id + '.mp4'
    s3 = boto3.client("s3",aws_access_key_id=ACCESS_KEY_ID,aws_secret_access_key=ACCESS_SECRET_KEY)
    http = urllib3.PoolManager()
    s3.upload_fileobj(http.request("GET", stream.url, preload_content = False), BUCKET_NAME, key)
    
    message = {
        "id": yt_id,
        "title": yt.title,
        "resolution": stream.resolution,
        "mime_type": stream.mime_type
    }
    return {
        "statusCode": 200,
        "body": json.dumps(message),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        }
    }