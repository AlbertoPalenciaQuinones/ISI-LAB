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
    """ Busca hasta 5 artistas en Last.fm """
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "artist.search",
        "artist": busqueda,
        "api_key": API_KEY,
        "format": "json",
        "limit": 5  # 🔹 Last.fm permite limitar con este parámetro
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        resultados = response.json().get("results", {}).get("artistmatches", {}).get("artist", [])[:5]  # 🔹 Limitar a 5
        artistas = [{"nombre": artista["name"]} for artista in resultados]
        return artistas

    return []

