class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '123456789'
    MYSQL_DB = 'musicfinder'


config = {
    'development': DevelopmentConfig
}