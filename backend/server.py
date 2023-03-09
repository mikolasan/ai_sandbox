from json import JSONDecodeError
from aiohttp import web
import aiohttp_cors
import logging
import logging.config
import numpy as np
import traceback

from ann.navigation import Navigation

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("server")
nav = Navigation()
nav.load('ann/navigation.1.model')


def json_response(handler):
  async def wrapper(*args):
    this = args[0]
    try:
      data = await handler(*args)
    except Exception as e:
      print(traceback.format_exc())
      # logger.error(traceback.format_exc())
      # if this.comments_writer.get_error_status() == Status.OK:
      #   this.comments_writer.set_error_status(Status.SYSTEM_ERROR)
      data = None
      return web.json_response(this.create_response(data))
  return wrapper


class Server:
  def __init__(self):
    self.app = web.Application()
    self.app.router.add_route('POST', '/models/{model}/predict', self.model_predict)
    # Configure default CORS settings.
    self.cors = aiohttp_cors.setup(self.app, defaults={
      "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
          )
    })
    # Configure CORS on all routes.
    for route in list(self.app.router.routes()):
      self.cors.add(route)
  
  def run(self):
    # ssl_context = ssl.create_default_context(
    #     purpose=ssl.Purpose.CLIENT_AUTH,
    #     cafile=path.join('keys', 'ca.pem'))
    # # ssl_context.verify_mode = ssl.CERT_REQUIRED 
    # ssl_context.load_cert_chain(path.join('keys', 'server.crt'), path.join('keys', 'server.key'))
    web.run_app(self.app,
                host='0.0.0.0',
                port=8080,
                access_log=logger)
                # ssl_context=ssl_context)
  
  def create_response(self, data=None):
    if not data:
      return {}
    return data
  
  async def model_predict(self, request):
    name = request.match_info.get('model', 'navigation')
    try:
      request_data = await request.json()
    except JSONDecodeError:
      return web.Response(status=400, text='your json is bad :o')
    # logger.info(f'{request.path} <-- {request_data}')
    if name == 'navigation':
      try:
        angle = request_data['angle'] % 360
        distance = request_data['distance']
        x = [angle, distance]
        X = np.array([x])
        category = nav.predict(X)
        category_map = {
          0: 'up',
          1: 'left',
          2: 'down',
          3: 'right'
        }
        direction = category_map[category.item()]
        prediction = {
          'direction': direction,
        }
      except Exception as e:
        print(traceback.format_exc())
    else:
      return web.Response(status=400, text='this is not the model you are looking for')
    
    return web.json_response(prediction)


if __name__ == '__main__':
  server = Server()
  server.run()