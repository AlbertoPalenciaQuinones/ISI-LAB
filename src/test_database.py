from flask import json, request
from discogs_api import obtener_info_discogs, obtener_info_artista_discogs
from lastfm_api import obtener_info_artista_lastfm, obtener_info_album_lastfm
import pymysql # type: ignore
from config import config

# 🚀 Lista de artistas a buscar en Discogs y Last.fm
ARTISTAS_A_BUSCAR = [
    "Oscar Mulero", "Reeko", "Christian Wünsch", "Exium", "Lewis Fautzi",
    "Jeff Mills", "Robert Hood", "Surgeon", "Ben Klock", "DVS1",
    "Regis", "Speedy J"
]

# 🚀 Lista de álbumes a buscar en Discogs y Last.fm
ALBUMS_A_BUSCAR = [
    # Oscar Mulero
    ("Oscar Mulero", "Muscle and Mind"),
    ("Oscar Mulero", "Perfect Peace"),
    ("Oscar Mulero", "Black Propaganda"),
    ("Oscar Mulero", "Acceptance"),
    ("Oscar Mulero", "Monochrome"),
    ("Oscar Mulero", "Grey Fades to Green"),

    # Reeko
    ("Reeko", "Finding the New Matter"),
    ("Reeko", "Between Desires and Delusions"),
    ("Reeko", "Bad Mood"),
    ("Reeko", "Empty Streets"),
    ("Reeko", "Industrial Complex"),
    ("Reeko", "Mechanics of Joy"),

    # Christian Wünsch
    ("Christian Wünsch", "Internal Conversion"),
    ("Christian Wünsch", "Sacrifice"),
    ("Christian Wünsch", "Structure"),
    ("Christian Wünsch", "Mutations"),
    ("Christian Wünsch", "Paranormal Activities"),
    ("Christian Wünsch", "Through the Ages"),

    # Exium
    ("Exium", "Roots of Time"),
    ("Exium", "A Sensible Alternative to Emotion"),
    ("Exium", "Reference"),
    ("Exium", "Caronte"),
    ("Exium", "XV"),
    ("Exium", "Neural Structure"),

    # Lewis Fautzi
    ("Lewis Fautzi", "The Gare Album"),
    ("Lewis Fautzi", "Space Exploration"),
    ("Lewis Fautzi", "Twilight"),
    ("Lewis Fautzi", "Deep Illusion"),
    ("Lewis Fautzi", "Straight Line"),
    ("Lewis Fautzi", "Control Room"),

    # Otros artistas legendarios del Techno
    ("Jeff Mills", "Waveform Transmission Vol. 1"),
    ("Jeff Mills", "The Bells"),
    ("Jeff Mills", "Axis Classics"),
    ("Robert Hood", "Minimal Nation"),
    ("Robert Hood", "Internal Empire"),
    ("Surgeon", "Force + Form"),
    ("Surgeon", "Balance"),
    ("Ben Klock", "One"),
    ("DVS1", "Beta Sensory Motor Rhythm"),
    ("Regis", "Penetration"),
    ("Speedy J", "Loudboxer"),
]


def verificar_datos():
    """ Verifica si hay datos en la base de datos después de la importación """
    conexion = pymysql.connect(
        host=config['development'].MYSQL_HOST,
        user=config['development'].MYSQL_USER,
        password=config['development'].MYSQL_PASSWORD,
        database=config['development'].MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conexion.cursor() as cursor:
            # ✅ Verificar artistas en la base de datos
            cursor.execute("SELECT COUNT(*) as total FROM artistas;")
            total_artistas = cursor.fetchone()["total"]
            
            # ✅ Verificar álbumes en la base de datos
            cursor.execute("SELECT COUNT(*) as total FROM albumes;")
            total_albumes = cursor.fetchone()["total"]

            print("\n🔹 Verificación de la base de datos:")
            print(f"   🎶 Artistas almacenados: {total_artistas}")
            print(f"   📀 Álbumes almacenados: {total_albumes}")

            if total_artistas == 0:
                print("⚠️ No se encontraron artistas en la base de datos.")
            if total_albumes == 0:
                print("⚠️ No se encontraron álbumes en la base de datos.")

    except pymysql.MySQLError as e:
        print(f"❌ Error al consultar la base de datos: {e}")
    
    finally:
        conexion.close()


def poblar_base_de_datos():
    """ Recupera datos de Discogs y Last.fm y los almacena en MySQL """
    print("🔹 Iniciando proceso de importación de datos...\n")

    # 🔹 Buscar y almacenar ARTISTAS
    for artista in ARTISTAS_A_BUSCAR:
        print(f"🔍 Buscando información de '{artista}' en Discogs y Last.fm...")
        resultado = obtener_info_artista_discogs(artista)

        if resultado:
            print(f"✅ Artista '{artista}' guardado en la base de datos.\n")
        else:
            print(f"⚠️ No se pudo encontrar información de '{artista}' en las APIs.\n")

    # 🔹 Buscar y almacenar ÁLBUMES
    for artista, album in ALBUMS_A_BUSCAR:
        print(f"🔍 Buscando '{album}' de {artista} en Discogs y Last.fm...")
        resultado = obtener_info_artista_lastfm(artista, album)

        if resultado:
            print(f"✅ Álbum '{album}' de {artista} guardado en la base de datos.\n")
        else:
            print(f"⚠️ No se pudo encontrar '{album}' de {artista} en las APIs.\n")

    # ✅ Verificar que los datos fueron almacenados correctamente
    verificar_datos()

def buscar_artista():
    """ Solicita el nombre del artista por consola y busca su información en Discogs y Last.fm """

    nombre_artista = input("🎤 Introduce el nombre del artista: ")

    # 🔹 Obtener datos desde Discogs
    artista_discogs = obtener_info_artista_discogs(nombre_artista)

    # 🔹 Obtener datos desde Last.fm
    artista_lastfm = obtener_info_artista_lastfm(nombre_artista)

    # 🔹 Combinar datos de ambas APIs
    artista_completo = {
        "id_artista": artista_discogs["id_artista"] if artista_discogs else None,
        "nombre": artista_discogs["nombre"] if artista_discogs else artista_lastfm["nombre"],
        "biografia": artista_discogs["biografia"] if artista_discogs else None,
        "imagen": artista_discogs["imagen"] if artista_discogs else artista_lastfm["imagen"],
        "url_discogs": artista_discogs["url_discogs"] if artista_discogs else None,
        "url_lastfm": artista_lastfm["url_lastfm"] if artista_lastfm else None,
        "listeners": artista_lastfm["listeners"] if artista_lastfm else None,
        "plays": artista_lastfm["plays"] if artista_lastfm else None,
        "tags": artista_lastfm["tags"] if artista_lastfm else None,
        "urls_extras": artista_discogs["urls_extras"] if artista_discogs else []
    }

    # 🔹 Mostrar la información del artista en la terminal
    print("\n🎶 Información del Artista:")
    print(json.dumps(artista_completo, indent=4, ensure_ascii=False))

    return artista_completo

if __name__ == "__main__":
    artista_info = buscar_artista()
