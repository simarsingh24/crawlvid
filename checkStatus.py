import json
import boto3

BUCKET = 'seektube'

def lambda_handler(event, context):
    
    transcribe = boto3.client("transcribe",aws_access_key_id=ACCESS_KEY_ID,aws_secret_access_key=ACCESS_SECRET_KEY,
        region_name='us-east-1')
    
    job_name=event["queryStringParameters"]['id']
    
    try:
        response = transcribe.get_transcription_job(TranscriptionJobName = job_name)
        message = response["TranscriptionJob"]["TranscriptionJobStatus"]
    except:
        message='Job Not exsist'

    return {
        "statusCode": 200,
        "body": json.dumps({"status": message}),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        }
    }
