import os 
import base64
import requests
import boto3
from config import settings
from services.storage.crud.local import LocalStorage

class RemoteStorage():

    def aws_instance(self):
        return boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            )
    
    # Save the file in the storage
    def save_file(
        self,
        local_file_name: str,
        file_data: bytes ,
        aws_file_path: str,
        aws_file_name: str= None,
        local_file_path: str=None,
        delete_after_upload: bool=False
        ) -> bool:

        '''
        Save the file in the S3 bucket

        
        '''
        
        # Save the file in the storage

        # If the file isn't created in the local storage
        if file_data:

            # Create a file in the local storage
            with open(local_file_path + '/' + local_file_name, 'wb') as f:
                f.write(file_data)

        s3_client = self.aws_instance()

        bucket = settings.aws_bucket_name

        try:
            # If the custom file name is provided, use it
            if not aws_file_name:
                aws_file_name = local_file_name
            s3_client.upload_file(local_file_path + local_file_name, bucket,aws_file_path+aws_file_name)
            
        except Exception as e:
            print(e)
            return False

        # Delete the file in the local storage  
        if delete_after_upload:
            self.delete_local(local_file_path+local_file_name)
        
        return True

    # Get the file from the storage
    def get_file(
        self,
        aws_file_name: str,
        aws_file_path: str,
        local_file_name: str=None,
        local_file_path: str=None,
        return_blob: bool=False
        ):

        # Get the file from S3 bucker
        s3_client = self.aws_instance()

        if local_file_name is None:
            local_file_name = aws_file_name

        bucket = settings.aws_bucket_name
        with open(local_file_path + local_file_name, 'wb') as f:
            s3_client.download_fileobj(bucket, aws_file_path + aws_file_name, f)

        # Return the file bytes
        if return_blob:
            return LocalStorage().get_file(local_file_path,local_file_name)
        
        
        return True