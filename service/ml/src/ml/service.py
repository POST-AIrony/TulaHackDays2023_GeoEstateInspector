import httpx
from core import settings
from ml import exceptions, schemas


class MLService:
    @staticmethod
    async def get_user(token: str) -> schemas.UserModel | list:
        print("GOGOGGO")
        async with httpx.AsyncClient() as client:
            res = await client.post(
                url="http://" + settings.USER_SERVICE + "/api/user/me",
                json={"token": token},
            )
            print(res.status_code)
            print(res.content)
            match res.status_code:
                case 403:
                    if res.json().get("detail") != None:
                        match res.json().get("detail"):
                            case "Could not validate credentials":
                                return [
                                    False,
                                    "Could not validate credentials",
                                ]
                            case "JWT Token time out exception. Sign in.":
                                return [
                                    False,
                                    "JWT Token time out exception. Sign in.",
                                ]
                            case _:
                                return [
                                    False,
                                    "JWT Token time out exception. Sign in.",
                                ]
                case 404:
                    return [
                        False,
                        "User not found",
                    ]
                case 200:
                    return schemas.UserModel(**res.json())

                case _:
                    # TODO: Log this
                    print("ALERTTTTTTTTTTTTT")
