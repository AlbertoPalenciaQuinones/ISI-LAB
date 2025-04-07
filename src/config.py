class DevelopmentConfig:
    DEBUG = True
    MYSQL_HOST = 'localhost'  # Cambia esto si usas un servidor remoto
    MYSQL_USER = 'root'  # Tu usuario de MySQL
    MYSQL_PASSWORD = '123456789'  # Tu contraseña de MySQL
    MYSQL_DB = 'musicfinder'
    MYSQL_CURSORCLASS = 'DictCursor'

config = {
    'development': DevelopmentConfig
}
