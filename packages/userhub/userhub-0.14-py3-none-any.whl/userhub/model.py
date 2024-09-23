from libdev.cfg import cfg
from libdev.req import fetch
from libdev.log import log
from consys import Attribute  # make_base
from consys.handlers import (
    default_login,
    check_login_uniq,
    check_password,
    process_password,
    pre_process_name,
    check_name,
    check_phone_uniq,
    pre_process_phone,
    check_mail_uniq,
    process_title,
    process_lower,
    default_status,
    default_title,
)


LINK = "https://chill.services/api/"


# Base = make_base(
#     host=cfg("mongo.host") or "db",
#     name=cfg("PROJECT_NAME"),
#     login=cfg("mongo.user"),
#     password=cfg("mongo.pass"),
# )


class BaseUser:  # User(Base)
    _name = "users"
    _token = None

    # status:
    # 0 - deleted
    # 1 - blocked
    # 2 - unauthorized
    # 3 - authorized
    # 4 - has access to platform resources
    # 5 - supervisor
    # 6 - moderator
    # 7 - admin
    # 8 - owner

    login = Attribute(
        types=str,
        default=default_login,
        checking=check_login_uniq,
        pre_processing=process_lower,
    )
    password = Attribute(
        types=str,
        checking=check_password,
        processing=process_password,
    )
    # Personal
    name = Attribute(
        types=str,
        pre_processing=pre_process_name,
        checking=check_name,
        processing=process_title,
    )
    surname = Attribute(
        types=str,
        pre_processing=pre_process_name,
        checking=check_name,
        processing=process_title,
    )
    title = Attribute(
        types=str,
        default=default_title,
    )
    birth = Attribute(types=int)  # TODO: datetime
    sex = Attribute(types=str)  # TODO: enum: male / female
    # Contacts
    phone = Attribute(
        types=int,
        checking=check_phone_uniq,
        pre_processing=pre_process_phone,
    )
    phone_verified = Attribute(types=bool, default=True)
    mail = Attribute(
        types=str,
        checking=check_mail_uniq,
        pre_processing=process_lower,
    )
    mail_verified = Attribute(types=bool, default=True)
    social = Attribute(types=list)  # TODO: list[{}] # TODO: checking
    #
    description = Attribute(types=str)
    status = Attribute(types=int, default=default_status)
    rating = Attribute(types=float)
    # global_channel = Attribute(types=int, default=1)
    # channels = Attribute(types=list)
    discount = Attribute(types=float)
    balance = Attribute(types=int, default=0)
    subscription = Attribute(types=int, default=0)
    utm = Attribute(types=str)  # Source
    pay = Attribute(types=list)  # Saved data for payment
    # Permissions
    mailing = Attribute(types=dict)
    # Cache
    last_online = Attribute(types=int)

    # TODO: UTM / promo
    # TODO: referal_parent
    # TODO: referal_code
    # TODO: attempts (password)
    # TODO: middle name

    # TODO: del Base.user

    def get_social(self, social):
        """Get user social info by social ID"""
        for i in self.social:
            if i["id"] == social:
                return {
                    "id": i["user"],
                    "login": i.get("login"),
                    "locale": i.get("locale") or cfg("locale", "en"),
                }
        return None

    def __init__(self, token=None, **kwargs):
        self._token = token
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self

    @classmethod
    async def get(
        cls,
        token: str,
        **kwargs,
    ):
        code, res = await fetch(LINK + "users/get/", {"token": token, **kwargs})

        if code != 200 or not isinstance(res, dict) or "users" not in res:
            log.error(f"{code}: {res}")
            return str(res)
        users = res["users"]

        if isinstance(users, dict):
            return cls(token, **users)
        return [cls(token, **user) for user in users]

    @classmethod
    async def complex(
        cls,
        token: str,
        **kwargs,
    ):
        code, res = await fetch(LINK + "users/get/", {"token": token, **kwargs})

        if code != 200 or not isinstance(res, dict) or "users" not in res:
            log.error(f"{code}: {res}")
            return str(res)
        users = res["users"]
        return users
