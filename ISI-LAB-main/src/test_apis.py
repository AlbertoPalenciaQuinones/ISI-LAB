import requests

# 🚀 Credenciales de Discogs
ACCESS_TOKEN = "GLSzIdaxEDVBQWczLGrFlZrSIrmnRMVtCyOAxlGW"
DISCOGS_URL = "https://api.discogs.com/database/search"

# 🚀 API Key de Last.fm
API_KEY = "fc59a90f65f0c9e4ede7546a7e9a10f7"
LASTFM_URL = "http://ws.audioscrobbler.com/2.0/"


# 🔹 Función para obtener artistas desde Discogs
def obtener_artistas_discogs(busqueda):
    params = {"q": busqueda, "type": "artist", "token": ACCESS_TOKEN, "per_page": 5}
    response = requests.get(DISCOGS_URL, params=params)

    if response.status_code == 200:
        resultados = response.json().get("results", [])[:5]

        artistas = []
        for artista in resultados:
            artistas.append({
                "nombre": artista.get("title", "Desconocido"),
                "imagen": artista.get("cover_image", ""),
                "url": artista.get("resource_url", "#"),
                "tags": "No disponible",  # Discogs no siempre tiene géneros en la búsqueda
                "listeners": "N/A",
                "plays": "N/A"
            })
        return artistas

    print(f"❌ Error en Discogs: {response.status_code} - {response.text}")
    return []


# 🔹 Función para obtener artistas desde Last.fm
def obtener_artistas_lastfm(busqueda):
    params = {
        "method": "artist.getinfo",
        "artist": busqueda,
        "api_key": API_KEY,
        "format": "json"
    }
    response = requests.get(LASTFM_URL, params=params)

    if response.status_code == 200:
        datos = response.json().get("artist", {})

        if datos:
            return [{
                "nombre": datos.get("name", "Desconocido"),
                "imagen": datos["image"][-1]["#text"] if datos.get("image") else "",
                "url": datos.get("url", "#"),
                "tags": ", ".join([tag["name"] for tag in datos.get("tags", {}).get("tag", [])]) if "tags" in datos else "No especificado",
                "listeners": datos.get("stats", {}).get("listeners", "0"),
                "plays": datos.get("stats", {}).get("playcount", "0")
            }]

    print(f"❌ Error en Last.fm: {response.status_code} - {response.text}")
    return []


# 🔥 Prueba de APIs
if __name__ == "__main__":
    busqueda = input("🔍 Introduce el nombre del artista: ").strip()

    print("\n🎵 Buscando en Discogs...")
    artistas_discogs = obtener_artistas_discogs(busqueda)
    if artistas_discogs:
        for artista in artistas_discogs:
            print(f"\n✅ {artista['nombre']}")
            print(f"🖼 Imagen: {artista['imagen']}")
            print(f"🔗 URL: {artista['url']}")
            print(f"🎼 Géneros: {artista['tags']}")
            print(f"👥 Seguidores: {artista['listeners']}")
            print(f"▶️ Reproducciones: {artista['plays']}")
    else:
        print("⚠️ No se encontraron artistas en Discogs.")

    print("\n🎶 Buscando en Last.fm...")
    artistas_lastfm = obtener_artistas_lastfm(busqueda)
    if artistas_lastfm:
        for artista in artistas_lastfm:
            print(f"\n✅ {artista['nombre']}")
            print(f"🖼 Imagen: {artista['imagen']}")
            print(f"🔗 URL: {artista['url']}")
            print(f"🎼 Géneros: {artista['tags']}")
            print(f"👥 Seguidores: {artista['listeners']}")
            print(f"▶️ Reproducciones: {artista['plays']}")
    else:
        print("⚠️ No se encontraron artistas en Last.fm.")

    if not artistas_discogs and not artistas_lastfm:
        print("\n⚠️ No se encontraron resultados en ninguna API.")
