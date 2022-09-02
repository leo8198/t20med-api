from pydantic import BaseModel

# Class to reset user password
class UserReset(BaseModel):
    password: str