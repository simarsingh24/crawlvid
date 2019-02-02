import json
import boto3

BUCKET = 'seektube'

def lambda_handler(event, context):

    
    transcribe = boto3.client("transcribe",aws_access_key_id=ACCESS_KEY_ID,aws_secret_access_key=ACCESS_SECRET_KEY,
        region_name='us-east-1')
    
    v_name = event["queryStringParameters"]['id']
    
    response = transcribe.start_transcription_job(
        TranscriptionJobName = v_name,
        LanguageCode = "en-US",
        MediaFormat = "mp4",
        Media={
            
            "MediaFileUri": "https://s3.amazonaws.com/" + BUCKET + "/" + v_name + ".mp4"
        },
        OutputBucketName = BUCKET,
    )
    message = {"name": v_name}


  
    return {
        "statusCode": 200,
        "body": json.dumps(message),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        }
    }
