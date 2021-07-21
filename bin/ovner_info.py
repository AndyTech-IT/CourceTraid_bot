from admin.bot_admin import BotAdmin
from user.bot_user import BotUser

_ovner_id = environ['OVNER_ID'] 

Ovner_Admin = BotAdmin(id=_ovner_id)
Ovner_User = BotUser(id=_ovner_id)
