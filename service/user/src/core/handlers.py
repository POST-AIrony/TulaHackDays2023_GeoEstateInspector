from jose.exceptions import JWTError
from user import exceptions, models, repository, schemas, utils


async def token_decode_handler(token: str):
    try:
        token_data = await utils.decode_token(token)
    except JWTError:
        raise exceptions.JWTError
    except TimeoutError:
        raise exceptions.JWTTimeOutError
    return token_data
