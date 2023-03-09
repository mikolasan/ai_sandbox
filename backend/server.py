from aiohttp import web
from ..ann.navigation import Navigation

def json_response(handler):
  async def wrapper(*args):
    this = args[0]
    try:
      data = await handler(*args)
    except Exception as e:
      # logger.error(traceback.format_exc())
      # if this.comments_writer.get_error_status() == Status.OK:
      #   this.comments_writer.set_error_status(Status.SYSTEM_ERROR)
      data = None
      return web.json_response(this.create_response(data))
  return wrapper


class Server:
  def __init__(self):
    self.app = web.Application()
    self.app.router.add_route('POST', "/models/navigation/predict", self.model_predict)
  
  def run(self):
    # ssl_context = ssl.create_default_context(
    #     purpose=ssl.Purpose.CLIENT_AUTH,
    #     cafile=path.join('keys', 'ca.pem'))
    # # ssl_context.verify_mode = ssl.CERT_REQUIRED 
    # ssl_context.load_cert_chain(path.join('keys', 'server.crt'), path.join('keys', 'server.key'))
    web.run_app(self.app,
                host='0.0.0.0',
                port=8080)
                # access_log=logger,
                # ssl_context=ssl_context)
  
  def create_response(self, data=None):
    return data
  
  @json_response
  async def model_predict(self, request):
    request_data = await request.json()
    # logger.info(f'{request.path} <-- {request_data}')
    direction = "left"
    return {
      'direction': direction,
    }


if __name__ == '__main__':
  server = Server()
  server.run()