from fastapi import HTTPException, status

# Custom error templates
class CustomError:

    def error_400(self, description: str):
        '''
        Custom HTTP 400 error message
        '''
        return HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "status": "Error",
                            "status_code": 1,
                            "description":description
                        }
                    )

    def error_500(self, description: str):
        '''
        Custom HTTP 500 error message
        '''
        raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                        detail={
                        "status": "Error",
                        "status_code": 1,
                        "description":description}) 

    def error_401(self, description: str):
        '''
        Custom HTTP 401 error message
        '''
        raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail={
                        "status": "Error",
                        "status_code": 3,
                        "description":description}) 

    def error_404(self, description: str):
        '''
        Custom HTTP 404 error message
        '''
        raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, 
                        detail={
                        "status": "Error",
                        "status_code": 4,
                        "description":description})

    def error_403(self, description: str):
        '''
        Custom HTTP 403 error message
        '''
        raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, 
                        detail={
                        "status": "Error",
                        "status_code": 3,
                        "description":description})
