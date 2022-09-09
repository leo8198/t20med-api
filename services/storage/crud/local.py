import os
import base64 

class LocalStorage():

    def save_file(
        self,
        local_file_path: str,
        local_file_name: str,
        file_data: bytes
    ):
        '''
        Save the file in the local storage.
        '''
        # Get the file from the storage
        path = local_file_path + local_file_name

        # Save the file in the storage
        with open(path, 'wb') as f:
            f.write(file_data)

        return True


    def get_file(
        self,
        local_file_path: str,
        local_file_name: str):
        '''
        Get the file from the local storage.

        Return the file data in base64 format.
        '''
        # Get the file from the storage
        path = local_file_path + local_file_name

        # Check if the file exists
        if not os.path.exists(path):
            return None

        # Save the file in the storage
        with open(path, 'rb') as pdf:
            return base64.b64encode(pdf.read())


    def delete_file(
        self,
        local_file_path: str,
        local_file_name: str
    ):
        '''
        Delete the file from the local storage
        '''
        
        # Get the file from the storage
        path = local_file_path + local_file_name

        # Check if the file exists
        if not os.path.exists(path):
            return True

        # Delete the file
        os.remove(path)

        return True