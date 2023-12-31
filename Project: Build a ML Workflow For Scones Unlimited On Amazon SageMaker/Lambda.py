import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = ## TODO: fill in
    bucket = ## TODO: fill in
    
    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }


# serializeImageData Function

import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    key = event['s3_key']  
    bucket = event['s3_bucket']  

    s3.download_file(bucket, key, '/tmp/image.png')

    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

# dataClassifier function

import json
import boto3
import base64

ENDPOINT = "image-classification-2023-12-28-20-51-08-699"  

def lambda_handler(event, context):

    print("Received Event:", json.dumps(event))
    print("Event keys:", event.keys())
    
    image = base64.b64decode(event['body']["image_data"])
    
    endpoint = ENDPOINT
    runtime = boto3.Session().client('sagemaker-runtime')
    response = runtime.invoke_endpoint(EndpointName=endpoint, ContentType = 'image/png',Body = image)
    predictions = json.loads(response['Body'].read().decode())
    event["inferences"] = predictions
    
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }



# outlierFilter function
import json

THRESHOLD = 0.93  # Adjust this threshold as needed (between 1.00 and 0.000)

def lambda_handler(event, context):
    try:
        inferences = json.loads(event["inferences"])

        meets_threshold = any(value >= THRESHOLD for value in inferences)

        if meets_threshold:
            return {
                'statusCode': 200,
                'body': json.dumps(event)
            }
        else:
            raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")
    except Exception as e:
        return {
            'statusCode': 500,  
            'body': str(e)  
        }