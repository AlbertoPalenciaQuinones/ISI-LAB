import pymysql
from config import config

# 🚀 Conectar a la Base de Datos MySQL
def conectar():
    try:
        conexion = pymysql.connect(
            host=config['development'].MYSQL_HOST,
            user=config['development'].MYSQL_USER,
            password=config['development'].MYSQL_PASSWORD,
            database=config['development'].MYSQL_DB,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conexion
    except pymysql.MySQLError as e:
        print(f"❌ Error al conectar con MySQL: {e}")
        return None

# 🚀 Guardar un álbum en la base de datos evitando duplicados
def guardar_album(id_album, nombre, artista, year, formato, url, sello_discografico, rating, 
                  lastfm_listeners, lastfm_plays, lastfm_url, lastfm_image, lastfm_tags, discogs_availability):

    conexion = conectar()
    
    if not conexion:
        print("❌ No se pudo conectar a la base de datos.")
        return

    try:
        with conexion.cursor() as cursor:
            sql = """INSERT INTO albumes (id_album, nombre, artista, year, formato, url, sello_discografico, rating, 
                                          lastfm_listeners, lastfm_plays, lastfm_url, lastfm_image, lastfm_tags, discogs_availability)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                     ON DUPLICATE KEY UPDATE 
                     nombre=VALUES(nombre), artista=VALUES(artista), year=VALUES(year), formato=VALUES(formato),
                     url=VALUES(url), sello_discografico=VALUES(sello_discografico), rating=VALUES(rating), 
                     lastfm_listeners=VALUES(lastfm_listeners), lastfm_plays=VALUES(lastfm_plays), lastfm_url=VALUES(lastfm_url), 
                     lastfm_image=VALUES(lastfm_image), lastfm_tags=VALUES(lastfm_tags), discogs_availability=VALUES(discogs_availability)"""
            
            cursor.execute(sql, (id_album, nombre, artista, year, formato, url, sello_discografico, rating,
                                 lastfm_listeners, lastfm_plays, lastfm_url, lastfm_image, lastfm_tags, discogs_availability))
        
        conexion.commit()
        print(f"✅ Álbum '{nombre}' de {artista} guardado correctamente en MySQL.")
    
    except pymysql.MySQLError as e:
        print(f"❌ Error al guardar el álbum en MySQL: {e}")
    
    finally:
        conexion.close()


def guardar_artista(id_artista, nombre, biografia, imagen, url_discogs, url_lastfm, listeners, plays, tags):
    """ Guarda un artista en MySQL o actualiza si ya existe """
    conexion = pymysql.connect(
        host=config['development'].MYSQL_HOST,
        user=config['development'].MYSQL_USER,
        password=config['development'].MYSQL_PASSWORD,
        database=config['development'].MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conexion.cursor() as cursor:
            sql = """
                INSERT INTO artistas (id_artista, nombre, biografia, imagen, url_discogs, url_lastfm, listeners, plays, tags)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                biografia=VALUES(biografia), imagen=VALUES(imagen), url_discogs=VALUES(url_discogs), 
                url_lastfm=VALUES(url_lastfm), listeners=VALUES(listeners), plays=VALUES(plays), tags=VALUES(tags)
            """
            cursor.execute(sql, (id_artista, nombre, biografia, imagen, url_discogs, url_lastfm, listeners, plays, tags))
        
        conexion.commit()
        print(f"✅ Artista '{nombre}' guardado en MySQL.")
    
    except pymysql.MySQLError as e:
        print(f"❌ Error al guardar el artista en MySQL: {e}")
    
    finally:
        conexion.close()
