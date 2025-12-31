from amazon import update_amazon_pin
import pyotp
import time
from py2n import Py2NDevice, Py2NConnectionData
import aiohttp
import asyncio
import os.path
import os
import sys

from settings_template import settings as settings_template
settingsfile=os.path.dirname(os.path.realpath(__file__))+"/settings.py"
if os.path.exists(settingsfile):
  from settings import settings as file_settings
else:
  file_settings = {}

def read_settings():
  settings = {}
  settings_complete=True

  for key in settings_template:
    env_key = key.upper()
    if env_key in os.environ:
      settings[key] = os.environ[env_key]
    elif key in file_settings:
      settings[key] = file_settings[key]
    else:
      print("Setting "+key+" missing.")
      settings_complete=False

  if not settings_complete:
    print("Settings incomplete. Aborting")
    sys.exit(1)

  return settings

async def main():
  settings = read_settings()

  door_totp = pyotp.TOTP(settings['door_totp_secret'])

  #generate daily OTP
  new_door_otp = door_totp.now()
  print("new OTP:"+new_door_otp)

  async with aiohttp.ClientSession() as aiohttp_session:
    connection_data = Py2NConnectionData(host=settings['klingel_host'], username=settings['klingel_account'], password=settings['klingel_pwd'], unprivileged=True)
    device = await Py2NDevice.create(aiohttp_session, connection_data)
    users = await device.query_dir()
    update = []
    for user in users:
        if user['name'] in settings['klingel_users']:
            update.append({'uuid': user['uuid'], 'access': { 'code': ["","","", new_door_otp] }})
    updated_users = await device.update_dir(update)
    await aiohttp_session.put(settings['hass_webhook_uri'],json={'value':new_door_otp})

  update_amazon_pin(settings['amazon_mail'], settings['amazon_pwd'], settings['amazon_totp_secret'], new_door_otp)

asyncio.run(main())
