from bot_admin import BotAdmin
from bot_user import BotUser
from os import environ

_ovner_id = int(environ['OVNER_ID']) 

Ovner_Admin = BotAdmin(id=_ovner_id)
Ovner_User = BotUser(id=_ovner_id)
