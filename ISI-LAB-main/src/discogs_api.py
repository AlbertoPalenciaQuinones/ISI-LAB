import requests

# 🚀 Credenciales de Discogs (Reemplázalas con las tuyas)
CONSUMER_KEY = "UHBryCkmHEadIhxTorBF"
CONSUMER_SECRET = "rGOkabkyiIgixBGJMBZeUSurjdxkwZmG"
ACCESS_TOKEN = "GLSzIdaxEDVBQWczLGrFlZrSIrmnRMVtCyOAxlGW"

# 🔹 URL de la API de Discogs
BASE_URL = "https://api.discogs.com"

# 🔹 ✅ Función para buscar información de un artista en Discogs
def obtener_artistas_discogs(busqueda):
    """ Busca artistas en Discogs cuyo nombre coincida exactamente con el término buscado """
    url = "https://api.discogs.com/database/search"
    params = {"q": busqueda, "type": "artist", "token": ACCESS_TOKEN, "per_page": 10}  # Se puede pedir más para filtrar luego

    response = requests.get(url, params=params)

    if response.status_code == 200:
        resultados = response.json().get("results", [])

        # Normalizar la búsqueda para comparación exacta (ignorando mayúsculas/minúsculas)
        busqueda_normalizada = busqueda.strip().lower()

        artistas = []
        for artista in resultados:
            nombre = artista.get("title", "").strip()
            if nombre.lower() == busqueda_normalizada:
                artistas.append({
                    "nombre": nombre,
                    "imagen": artista.get("cover_image", ""),
                    "url": artista.get("resource_url", "#")
                })

        return artistas

    return []


# 🔹 ✅ Función para buscar un álbum en Discogs
def obtener_info_discogs(artista, album):
    """ Busca un álbum en Discogs y devuelve sus detalles """
    url = f"{BASE_URL}/database/search"
    params = {"q": f"{artista} {album}", "type": "release", "token": ACCESS_TOKEN}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        resultados = response.json().get("results", [])

        if resultados:
            album_data = resultados[0]  # Tomamos el primer resultado
            id_album = str(album_data["id"])
            nombre = album_data["title"]
            formato = ", ".join(album_data.get("format", ["Desconocido"]))
            year = album_data.get("year", None)
            url_discogs = album_data["resource_url"]
            sello_discografico = ", ".join(album_data.get("label", ["Desconocido"]))
            rating = album_data.get("community", {}).get("rating", {}).get("average", None)

            print(f"✅ Álbum encontrado: {nombre} de {artista} ({year})")
            return {
                "id_album": id_album,
                "nombre": nombre,
                "artista": artista,
                "year": year,
                "formato": formato,
                "url_discogs": url_discogs,
                "sello_discografico": sello_discografico,
                "rating": rating
            }

        else:
            print(f"⚠️ No se encontró '{album}' de {artista} en Discogs.")

    else:
        print(f"❌ Error en la solicitud a Discogs: {response.status_code} - {response.text}")

    return None

