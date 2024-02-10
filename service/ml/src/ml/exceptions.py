from fastapi import HTTPException
from starlette import status


class JWTException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


class JWTTimeOutError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="JWT Token time out exception. Sign in.",
        )


class UserNotFound(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
