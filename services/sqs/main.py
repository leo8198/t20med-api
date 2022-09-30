import random
import string
import boto3
from config import settings
import json

class SQSConnector():

    def __init__(self, queue: str) -> None:
        self.sqs_client = self._aws_instance()
        self.queue = queue

    def _aws_instance(self):
        return boto3.client(
            'sqs',
            region_name="us-east-1",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            )

    def _get_queue_url(self):
        
        response = self.sqs_client.get_queue_url(
            QueueName=self.queue,
        )
        return response["QueueUrl"]
    
    def send_message(self,message: dict, message_group_id: str):
        

        response = self.sqs_client.send_message(
            QueueUrl=self._get_queue_url(),
            MessageBody=json.dumps(message),
            MessageGroupId=message_group_id,
            MessageDeduplicationId=self._generate_id()
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return response 
        else:
            raise Exception('Error sending message to SQS')

    def receive_message(
        self,
        max_number_of_messages: int=1,
        wait_time_seconds: int=10):
        
        
        response = self.sqs_client.receive_message(
            QueueUrl=self._get_queue_url(),
            MaxNumberOfMessages=max_number_of_messages,
            WaitTimeSeconds=wait_time_seconds,
        )

        print(f"Number of messages received: {len(response.get('Messages', []))}")

        return response.get("Messages", [])

    def delete_message(self,receipt_handle):
        
        response = self.sqs_client.delete_message(
            QueueUrl=self._get_queue_url(),
            ReceiptHandle=receipt_handle,
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return None 
        else:
            raise Exception('Failed to delete SQS message')    

    def _generate_id(self):
        length = 8
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str