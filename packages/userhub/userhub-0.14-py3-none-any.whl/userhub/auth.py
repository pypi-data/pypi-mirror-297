"""
Functionality of authorization
"""

import re

from libdev.cfg import cfg
from libdev.req import fetch
from libdev.log import log


LINK = "https://chill.services/api/"


def check_phone(cont):
    """Phone checking"""
    return 11 <= len(str(cont)) <= 18


def pre_process_phone(cont):
    """Phone number pre-processing"""

    if not cont:
        return 0

    cont = str(cont)

    if cont[0] == "8":
        cont = "7" + cont[1:]

    cont = re.sub(r"[^0-9]", "", cont)

    if not cont:
        return 0

    return int(cont)


def check_mail(cont):
    """Mail checking"""
    return re.match(r".+@.+\..+", cont) is not None


def detect_type(login):
    """Detect the type of authorization"""

    if check_phone(pre_process_phone(login)):
        return "phone"

    if check_mail(login):
        return "mail"

    return "login"


async def auth(
    project: str,
    by: str,
    token: str,
    network: int = 0,
    ip: str = None,
    locale: str = cfg("locale", "en"),
    login: str = None,
    social: int = None,
    user: str = None,
    password: str = None,
    name: str = None,
    surname: str = None,
    image: str = None,
    mail: str = None,
    utm: str = None,
    online: bool = False,
    check_password: bool = False,
):
    """Auth"""

    req = {
        "by": by,
        "token": token,
        "network": network,
        "ip": ip,
        "locale": locale,
        "project": project,
        "login": login,
        "social": social,
        "user": user,
        "password": password,
        "name": name,
        "surname": surname,
        "image": image,
        "mail": mail,
        "utm": utm,
        "online": online,
        "check_password": check_password,
    }

    code, res = await fetch(LINK + "account/proj/", req)
    if code != 200:
        log.error(f"{code}: {res}")
        return 0, token, False
    return res["user"], res["token"], res["new"]


async def token(
    project: str,
    token: str,
    network: int = 0,
    utm: str = None,
    extra: dict = None,
    ip: str = None,
    locale: str = cfg("locale", "en"),
    user_agent: str = None,
):
    """Save token"""

    if extra is None:
        extra = {}

    req = {
        "token": token,
        "network": network,
        "utm": utm,
        "extra": extra,
        "ip": ip,
        "locale": locale,
        "user_agent": user_agent,
        "project": project,
    }

    code, res = await fetch(LINK + "account/proj_token/", req)
    if code != 200:
        log.error(f"{code}: {res}")
        return None, 0, 2
    return res["token"], res["user"], res["status"]
