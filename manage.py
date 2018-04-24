# -*-  coding:utf-8  -*-
from config.routes import urls
from config.conf import settings
from sqlalchemy.orm import scoped_session, sessionmaker
from libs.database import engine
import redis
from libs import database
from libs.connector import Connection
from tornado.options import define, options
import tornado.ioloop
import tornado.web
import sys
import MySQLdb
from auth import *
from config import *
from handlers import *
from utils import *

define("port", default=8081, help="Run server on a specific port", type=int)

class Index(tornado.web.RequestHandler) :
    def get(self) :
        return self.write('hello index')

def cache_manager_init():
    pool = redis.ConnectionPool(host=settings['redis_host'], port=settings['redis_port'], password=settings['redis_pass'],db=0)
    # c = tornadoredis.Client(host=settings['redis_host'], port=settings['redis_port'], password=settings['redis_pass'], connection_pool=CONNECTION_POOL)
    r = redis.Redis(connection_pool=pool)
    return r

class MyApplication(tornado.web.Application) :
    def __init__(self, handlers, **settings) :
        # self.conf = get_settings()
        sdb = database.DB_Session()
        sdb.close()

        # 创建redis连接池
        # self.redis = cache_manager_init()
        super(MyApplication, self).__init__(handlers, **settings)

def make_app():
    return MyApplication(urls, **settings)

def main():
    options.parse_command_line()
    app = make_app()
    server = tornado.httpserver.HTTPServer(app, xheaders = True)
    server.listen(options.port)
    print 'port=', options.port         # debug
    tornado.ioloop.IOLoop.current().start()

def create_database() :
    import libs.model
    import hashlib
    libs.model.init_db()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == 'create_database' :
            create_database()
        elif sys.argv[1] == 'runserver' :
            main()
        elif sys.argv[1] == 'initdata' :
            init_database()
        else :
            main()
    else :
        main()
