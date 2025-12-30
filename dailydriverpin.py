from amazon import update_amazon_pin
import pyotp
import time
from py2n import Py2NDevice, Py2NConnectionData
import aiohttp
import asyncio

from settings import door_totp_secret, amazon_mail, amazon_pwd, amazon_totp_secret, klingel_host, klingel_account, klingel_pwd, klingel_users
async def main():
  door_totp = pyotp.TOTP(door_totp_secret)

  #generate daily OTP
  new_door_otp = door_totp.now()
  print("new OTP:"+new_door_otp)

  async with aiohttp.ClientSession() as aiohttp_session:
    connection_data = Py2NConnectionData(host=klingel_host, username=klingel_account, password=klingel_pwd, unprivileged=True)
    device = await Py2NDevice.create(aiohttp_session, connection_data)
    users = await device.query_dir()
    update = []
    for user in users:
        if user['name'] in klingel_users:
            update.append({'uuid': user['uuid'], 'access': { 'pin': new_door_otp }})
    updated_users = await device.update_dir(update)

  update_amazon_pin(amazon_mail, amazon_pwd, amazon_totp_secret, new_door_otp)

asyncio.run(main())
