from pydantic import BaseModel


class UserModel(BaseModel):
    email: str
    email_validated: bool
    username: str
    first_name: str
    last_name: str
    is_admin: bool
