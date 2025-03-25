import requests

# 🚀 API Key de Last.fm (Reemplázala con la tuya)
API_KEY = "fc59a90f65f0c9e4ede7546a7e9a10f7"
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

def obtener_info_album_lastfm(artista, album):
    """ Obtiene información de un álbum en Last.fm """
    params = {
        "method": "album.getinfo",
        "artist": artista,
        "album": album,
        "api_key": API_KEY,
        "format": "json"
    }
    
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        datos = response.json()

        if "album" in datos:
            album_data = datos["album"]

            # 🔹 Manejo seguro de valores
            lastfm_listeners = int(album_data.get("listeners", 0))
            lastfm_plays = int(album_data.get("playcount", 0))
            lastfm_url = album_data.get("url", "")
            lastfm_image = album_data["image"][-1]["#text"] if album_data.get("image") else ""

            # 🚀 🔥 Verificar si "tags" es un diccionario antes de acceder
            tags_data = album_data.get("tags")
            lastfm_tags = ", ".join([tag["name"] for tag in tags_data["tag"]]) if isinstance(tags_data, dict) and "tag" in tags_data else ""

            return {
                "listeners": lastfm_listeners,
                "plays": lastfm_plays,
                "url": lastfm_url,
                "image": lastfm_image,
                "tags": lastfm_tags
            }
    
    print(f"⚠️ No se encontró información de '{album}' de {artista} en Last.fm.")
    return None

def obtener_artistas_lastfm(busqueda):
    """ Busca artistas en Last.fm cuyo nombre coincida exactamente con el término buscado """
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "artist.search",
        "artist": busqueda,
        "api_key": API_KEY,
        "format": "json",
        "limit": 10  # Consultamos más y filtramos luego
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        resultados = response.json().get("results", {}).get("artistmatches", {}).get("artist", [])

        busqueda_normalizada = busqueda.strip().lower()
        artistas = []

        for artista in resultados:
            nombre = artista.get("name", "").strip()
            if nombre.lower() == busqueda_normalizada:
                artistas.append({
                    "nombre": nombre,
                    "url": artista.get("url", "#"),
                    "imagen": artista.get("image", [{}])[-1].get("#text", ""),
                    "listeners": int(artista.get("listeners", 0)),
                    "plays": 0,  # Este valor no viene en la búsqueda, solo en getinfo
                    "tags": "No disponible"
                })

        return artistas

    return []


def obtener_info_artista_lastfm(nombre):
    """ Recupera información completa de un artista desde Last.fm (getinfo) """
    params = {
        "method": "artist.getinfo",
        "artist": nombre,
        "api_key": API_KEY,
        "format": "json"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        artista = data.get("artist", {})

        return {
            "biografia": artista.get("bio", {}).get("summary", "No disponible"),
            "imagen": artista.get("image", [{}])[-1].get("#text", ""),
            "url_lastfm": artista.get("url", "#"),
            "listeners": int(artista.get("stats", {}).get("listeners", 0)),
            "plays": int(artista.get("stats", {}).get("playcount", 0)),
            "tags": ", ".join([tag["name"] for tag in artista.get("tags", {}).get("tag", [])]) if artista.get("tags") else "No especificado"
        }

    print(f"❌ Error recuperando info de Last.fm para {nombre}")
    return {}

