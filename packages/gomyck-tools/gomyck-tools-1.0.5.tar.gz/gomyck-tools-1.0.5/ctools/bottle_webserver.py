from bottle import ServerAdapter, Bottle, template
from socketserver import ThreadingMixIn
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server

"""
app = init_app('/doc_download')

@app.get('/queryList')
@mvc.parameter_handler()
@rule('DOC:DOWNLOAD')
def query_list(params, pageInfo):
"""

"""
module_names = list(globals().keys())
def get_modules():
  mods = []
  for modname in module_names:
    if modname == 'base' or modname == 'online' or modname.startswith('__') or modname == 'importlib': continue
    module = globals()[modname]
    mods.append(module)
  return mods

def get_ws_modules():
  from . import websocket
  return [websocket]
"""

"""
http_app = Bottle()
for module in controller.get_modules():
  log.debug('正在挂载http路由: {}'.format(module.app.context_path))
  http_app.mount(module.app.context_path, module.app)
http_server = bottle_server.WSGIRefServer(port=application.Server.port)
http_app.run(server=http_server, quiet=True)
"""

class CBottle:

  def __init__(self, bottle: Bottle, port=8888, quiet=False):
    self.port = port
    self.quiet = quiet
    self.bottle = bottle

  def run(self):
    http_server = WSGIRefServer(port=self.port)
    self.bottle.run(server=http_server, quiet=self.quiet)

  def set_index(self, path, **kwargs):
    @self.bottle.route(['/', '/index'])
    def index():
      return template(path, kwargs)

  def mount(self, context_path, app):
    self.bottle.mount(context_path, app)

def init_bottle(port=8888, quiet=False) -> CBottle:
  bottle = Bottle()
  return CBottle(bottle, port, quiet)

class ThreadedWSGIServer(ThreadingMixIn, WSGIServer): pass

class CustomWSGIHandler(WSGIRequestHandler):
  def log_request(*args, **kw): pass

class WSGIRefServer(ServerAdapter):

  def __init__(self, host='0.0.0.0', port=8010):
    super().__init__(host, port)
    self.server = None

  def run(self, handler):
    req_handler = WSGIRequestHandler
    if self.quiet: req_handler = CustomWSGIHandler
    self.server = make_server(self.host, self.port, handler, server_class=ThreadedWSGIServer, handler_class=req_handler)
    self.server.serve_forever()

  def stop(self):
    self.server.shutdown()
