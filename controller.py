import boto3
import json
import csv

config ={
    'AWS_ACCESS_KEY_ID': 'AKIAZFM3KGDWAVOEDUOU', 
    'AWS_SECRET_ACCESS_KEY': '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' 
}
session = boto3.Session(
    region_name="us-east-1",
    aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"]
)

lambda_client = session.client('lambda')
sqs_client = session.client('sqs')
output_bucket = "himaliaoutputbucket"
s3 = session.client('s3')

def purge_message_from_queue(queue_url, receipt_handle):
    response = sqs_client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    # print(f'\n\nMessage deleted from queue {queue_url}')

def invoke_lambda(lambda_function, key):
    # Set the input parameters for the Lambda function
    payload = {
        "key1": key
    }
    # Convert the input parameters to a JSON string
    payload_json = json.dumps(payload)
    image_name = key['Records'][0]['s3']['object']['key'] 
    print("Invoking lambda function for the image - " + image_name)

    # Invoke the Lambda function
    response = lambda_client.invoke(
        FunctionName=lambda_function,
        InvocationType='Event',
        Payload=payload_json
    )

    # Print the response from the Lambda function
    # print(response)
    return response

def download_from_s3(key):
	with open('tmp/'+key, 'wb') as f:
		s3.download_fileobj(output_bucket, key, f)
                
def receive_message_from_queue(queue_url):
    # Receive a message from the SQS queue
    message = sqs_client.receive_message(QueueUrl=queue_url, MessageAttributeNames=['All'])
   
    # Print the received message, if any
    if 'Messages' in message:
        message_body = message["Messages"][0]["Body"]
        # print(message_body)
        # convert string to dict
        message_body_dt = json.loads(message_body)
        key = message_body_dt['Records'][0]['s3']["object"]["key"]
        # trigger lambda
        receipt_handle = message["Messages"][0]["ReceiptHandle"]
        purge_message_from_queue(queue_url, receipt_handle)
        return message_body_dt

    return None

while 1:
    lambda_function = 'face_recoginition'
    msg = receive_message_from_queue('s3_input_notification_queue')
    if msg:
        res = invoke_lambda(lambda_function, msg)
    
    output_msg = receive_message_from_queue('s3_output_notification_queue')
    # get key from the output msg
   
    if output_msg:
        key = output_msg['Records'][0]['s3']['object']['key']
        print("Key from output notification", key)
        download_from_s3(key)
        # print it
        with open('tmp/'+key, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                print(row)
            print()
