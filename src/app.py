from flask import Flask, json, request, render_template, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from config import config
from discogs_api import obtener_artistas_discogs, obtener_info_discogs  # Importar funciones de la API de Discogs
from lastfm_api import  obtener_info_album_lastfm, obtener_artistas_lastfm, obtener_info_artista_lastfm, buscar_albumes_por_artista # Importar funciones de la API de last.fm
from database import guardar_artista

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Configuración de MySQL desde la clase DevelopmentConfig
app.config.from_object(config['development'])
conexion = MySQL(app)

@app.route('/')
def inicio():
    return render_template('inicio.html')  # Página de inicio con botones de login y registro.

@app.route('/iniciosesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT id_usuario, contraseña FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if usuario:
            usuario_id = usuario["id_usuario"]  # Accede al ID usando la clave del diccionario
            contraseña_hash = usuario["contraseña"]  # Accede a la contraseña usando la clave

            if check_password_hash(contraseña_hash, contraseña):
                session['usuario_id'] = usuario_id
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('dashboard'))

        flash('Correo o contraseña incorrectos', 'danger')

    return render_template('iniciosesion.html')

@app.route('/crearcuenta', methods=['GET', 'POST'])
def crear_cuenta():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT email FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            flash('El correo ya está registrado', 'danger')
        else:
            id_usuario = str(uuid.uuid4())
            contraseña_hash = generate_password_hash(contraseña)
            cursor.execute("INSERT INTO usuarios (id_usuario, nombre, email, contraseña) VALUES (%s, %s, %s, %s)", 
                           (id_usuario, nombre, email, contraseña_hash))
            conexion.connection.commit()
            flash('Cuenta creada exitosamente', 'success')
            return redirect(url_for('inicio_sesion'))
    
    return render_template('crearcuenta.html')


@app.route('/cerrarsesion')
def cerrar_sesion():
    session.pop('usuario_id', None)
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('inicio'))

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('inicio_sesion'))
    return render_template('dashboard.html')


# --------------------------------------------------------------------------------------------------------------------------------- #

# METODOS PARA BUSCAR ARTISTAS

def procesar_albumes_y_canciones(nombre_artista, cursor):
    """Busca álbumes y canciones de un artista y los guarda en la base de datos."""
    albumes_api = buscar_albumes_por_artista(nombre_artista)  # Llama a la función para obtener los álbumes del artista

    if albumes_api:
        for album in albumes_api:
            if "nombre" in album and album["nombre"]:
                # Obtener la información desde ambas APIs: Last.fm y Discogs
                info_album_lastfm = obtener_info_album_lastfm(nombre_artista, album["nombre"])
                info_album_discogs = obtener_info_discogs(nombre_artista, album["nombre"])

                if info_album_lastfm and info_album_discogs:
                    # Extraer datos de Discogs
                    year = info_album_discogs.get("year")
                    formato = info_album_discogs.get("formato", "Desconocido")
                    sello_discografico = info_album_discogs.get("sello_discografico", "Desconocido")
                    rating = info_album_discogs.get("rating", None)
                    url_discogs = info_album_discogs.get("url_discogs", "")

                    # Extraer datos de Last.fm
                    lastfm_url = info_album_lastfm.get("url")
                    lastfm_image = info_album_lastfm.get("image")
                    lastfm_tags = info_album_lastfm.get("tags", "")

                    # Insertar en la base de datos
                    cursor.execute("""
                        INSERT INTO albumes (nombre, artista, year, formato, url, lastfm_image, lastfm_url, sello_discografico, rating)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        album["nombre"],
                        nombre_artista,
                        year,
                        formato,
                        lastfm_url,
                        lastfm_image,
                        lastfm_url,
                        sello_discografico,
                        rating
                    ))
                    conexion.connection.commit()

                    # Guardar canciones del álbum
                    guardar_canciones_automatico(album["nombre"], nombre_artista, cursor)
    else:
        print(f"⚠️ No se encontraron álbumes para el artista '{nombre_artista}'.")

@app.route('/busqueda_artistas', methods=['GET', 'POST'])
def busqueda_artistas():
    artistas = []
    artistas_bd = []

    if request.method == 'POST':
        busqueda = request.form['busqueda'].strip()

        # Buscar en la base de datos
        cursor = conexion.connection.cursor()
        cursor.execute("""
            SELECT id_artista, nombre, biografia, imagen, url_discogs, url_lastfm, listeners, plays, tags
            FROM artistas
            WHERE LOWER(nombre) = LOWER(%s)
        """, (busqueda,))
        
        artistas_bd = [dict(fila) for fila in cursor.fetchall()]
        print("🎵 Artistas en BD:", artistas_bd)

        if not artistas_bd:  # Si no está en la BD, buscar en la API
            print("🔍 No encontrado en BD. Buscando en API...")
            artistas_api = obtener_info_artista_lastfm(busqueda)

            if isinstance(artistas_api, dict):
                artistas_api = [artistas_api]

            if isinstance(artistas_api, list) and all(isinstance(artista, dict) for artista in artistas_api):
                for artista in artistas_api:
                    guardar_artista(
                        nombre=artista.get("nombre", "Desconocido"),
                        biografia=artista.get("biografia", "No disponible"),
                        imagen=artista.get("imagen", ""),
                        url_discogs=artista.get("url_discogs", "#"),
                        url_lastfm=artista.get("url_lastfm", "#"),
                        listeners=artista.get("listeners", 0),
                        plays=artista.get("plays", 0),
                        tags=artista.get("tags", "No especificado")
                    )

                    # Procesar álbumes y canciones del artista
                    procesar_albumes_y_canciones(artista["nombre"], cursor)

                artistas = artistas_api
            else:
                print("⚠️ La API de Last.fm devolvió un formato inesperado.")
                flash("No se encontraron artistas con ese nombre. Intenta con otro término de búsqueda.", "warning")
        else:
            print("✅ Artista encontrado en BD.")
            artistas = artistas_bd

    return render_template('busqueda_artistas.html', artistas=artistas)
# --------------------------------------------------------------------------------------------------------------------------------- #

@app.route('/discografia/<nombre_artista>', methods=['GET', 'POST'])
def discografia_artista(nombre_artista):
    albumes = []  # Lista para almacenar los resultados finales
    mensaje_error = None  # Variable para almacenar el mensaje de error

    # Usar el nombre del artista como término de búsqueda
    busqueda = nombre_artista.strip()

    if busqueda:
        try:
            # Buscar en la base de datos por el nombre del artista
            cursor = conexion.connection.cursor()
            cursor.execute("""
                SELECT DISTINCT id_album, nombre, artista, year, formato, url, lastfm_image, lastfm_url
                FROM albumes
                WHERE LOWER(artista) = LOWER(%s)
            """, (busqueda,))

            albumes_bd = [{"id_album": fila["id_album"], "nombre": fila["nombre"], "artista": fila["artista"],
                           "year": fila["year"], "formato": fila["formato"], "url": fila["url"],
                           "imagen": fila["lastfm_image"], "lastfm_url": fila["lastfm_url"]} for fila in cursor.fetchall()]
            print("📀 Álbumes en BD:", albumes_bd)

            if not albumes_bd:  # Solo busca en API si no lo encuentra en la BD
                print("🔍 No encontrado en BD. Buscando en API...")
                albumes_api = obtener_info_album_lastfm(busqueda)  # Llama a la función de la API para buscar álbumes

                if albumes_api:
                    # Guardar en la BD los álbumes nuevos
                    for album in albumes_api:
                        cursor.execute("""
                            INSERT INTO albumes (nombre, artista, year, formato, url, lastfm_image, lastfm_url)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (album["nombre"], album["artista"], album["year"],
                              album["formato"], album["url"], album["imagen"], album["lastfm_url"]))
                        conexion.connection.commit()

                    albumes = albumes_api  # Mostrar los nuevos resultados de la API
                else:
                    mensaje_error = f"No se encontraron álbumes para el artista '{nombre_artista}'."
            else:
                print("✅ Álbum encontrado en BD.")
                albumes = albumes_bd  # Mostrar los resultados de la BD
        except Exception as e:
            print(f"⚠️ Error al buscar álbumes: {e}")
            mensaje_error = "No se han encontrado álbumes de este artista."
    else:
        mensaje_error = "Por favor, ingresa un término de búsqueda."

    return render_template('busqueda_albumes.html', albumes=albumes, nombre_artista=nombre_artista, mensaje_error=mensaje_error)


from lastfm_api import obtener_canciones_album_lastfm  # Importar el método creado



@app.route('/busqueda_albumes', methods=['GET', 'POST'])
def busqueda_albumes():
    albumes = []  # Lista para almacenar los resultados finales
    mensaje_error = None  # Variable para almacenar el mensaje de error

    # Capturar el contexto y el nombre del artista si se pasa como parámetro en la URL
    contexto = request.args.get('contexto', 'busqueda_album')  # Por defecto, es una búsqueda de álbumes
    nombre_artista = request.args.get('artista', '').strip()

    if request.method == 'POST':
        busqueda = request.form['busqueda'].strip()  # Eliminar espacios extra
    else:
        # Si se llega desde "Consultar Discografía", usar el nombre del artista como búsqueda inicial
        busqueda = nombre_artista if contexto == 'discografia' else ''

    if busqueda:
        try:
            # Buscar en la base de datos
            cursor = conexion.connection.cursor()
            if contexto == 'discografia':
                # Buscar álbumes por el nombre del artista
                cursor.execute(""" 
                    SELECT DISTINCT id_album, nombre, artista, year, formato, url, lastfm_image, lastfm_url
                    FROM albumes
                    WHERE LOWER(artista) = LOWER(%s)
                """, (busqueda,))
            else:
                # Buscar álbumes por el nombre del álbum o el artista
                cursor.execute(""" 
                    SELECT DISTINCT id_album, nombre, artista, year, formato, url, lastfm_image, lastfm_url
                    FROM albumes
                    WHERE LOWER(nombre) LIKE LOWER(%s) OR LOWER(artista) = LOWER(%s)
                """, ('%' + busqueda + '%', busqueda))

            albumes_bd = [{"id_album": fila["id_album"], "nombre": fila["nombre"], "artista": fila["artista"],
                           "year": fila["year"], "formato": fila["formato"], "url": fila["url"],
                           "imagen": fila["lastfm_image"], "lastfm_url": fila["lastfm_url"]} for fila in cursor.fetchall()]
            print("📀 Álbumes en BD:", albumes_bd)

            if not albumes_bd:  # Solo busca en API si no lo encuentra en la BD
                print("🔍 No encontrado en BD. Buscando en API...")

                # Llamamos a la función para obtener los álbumes desde Discogs
                albumes_api = buscar_albumes_por_artista(busqueda)  # Llama a la función para obtener los álbumes del artista

                if albumes_api:
                    # Guardar en la BD los álbumes nuevos
                    for album in albumes_api:
                        # Validar que el álbum tenga un nombre antes de llamar a obtener_info_album_lastfm
                        if "nombre" in album and album["nombre"]:
                            # Obtener la información desde ambas APIs: Last.fm y Discogs
                            info_album_lastfm = obtener_info_album_lastfm(busqueda, album["nombre"])  # Llama a la API con artista y álbum
                            info_album_discogs = obtener_info_discogs(busqueda, album["nombre"])  # Llamar a Discogs para obtener más info

                            if info_album_lastfm and info_album_discogs:
                                # Extraer datos de Discogs (aquí es donde obtenemos year y formato)
                                year = info_album_discogs.get("year")
                                formato = info_album_discogs.get("formato", "Desconocido")
                                sello_discografico = info_album_discogs.get("sello_discografico", "Desconocido")
                                rating = info_album_discogs.get("rating", None)
                                url_discogs = info_album_discogs.get("url_discogs", "")

                                # Extraer datos de Last.fm (aquí es donde obtenemos la imagen, el URL y las etiquetas)
                                lastfm_url = info_album_lastfm.get("url")
                                lastfm_image = info_album_lastfm.get("image")
                                lastfm_tags = info_album_lastfm.get("tags", "")

                                # Insertar en la base de datos
                                cursor.execute("""
                                    INSERT INTO albumes (nombre, artista, year, formato, url, lastfm_image, lastfm_url, sello_discografico, rating)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """, (
                                    album["nombre"],
                                    busqueda,  # Relacionar el álbum con el artista
                                    year,
                                    formato,
                                    lastfm_url,
                                    lastfm_image,
                                    lastfm_url,
                                    sello_discografico,
                                    rating
                                ))
                                conexion.connection.commit()

                                # Llamar al método para guardar canciones del álbum
                                guardar_canciones_automatico(album["nombre"], busqueda, cursor)

                    albumes = albumes_api  # Mostrar los nuevos resultados de la API
                else:
                    mensaje_error = "No se encontraron resultados."
            else:
                print("✅ Álbum encontrado en BD.")
                albumes = albumes_bd  # Mostrar los resultados de la BD
        except Exception as e:
            print(f"⚠️ Error al buscar álbumes: {e}")
            mensaje_error = "Ocurrió un error al realizar la búsqueda. Por favor, inténtalo de nuevo más tarde."
    else:
        mensaje_error = "Por favor, ingresa un término de búsqueda."

    return render_template('busqueda_albumes.html', albumes=albumes, nombre_artista=nombre_artista, contexto=contexto, mensaje_error=mensaje_error)


def guardar_canciones_automatico(nombre_album, nombre_artista, cursor):
    """Obtiene y guarda automáticamente las canciones de un álbum en la base de datos."""
    canciones = obtener_canciones_album_lastfm(nombre_artista, nombre_album)

    if not canciones:
        print(f"⚠️ No se encontraron canciones para el álbum '{nombre_album}' del artista '{nombre_artista}'.")
        return

    try:
        for cancion in canciones:
            cursor.execute("""
                INSERT INTO canciones (id_album, nombre, url)
                VALUES ((SELECT id_album FROM albumes WHERE nombre = %s AND artista = %s), %s, %s)
                ON DUPLICATE KEY UPDATE nombre = nombre
            """, (nombre_album, nombre_artista, cancion["nombre"], cancion["url"]))
        conexion.connection.commit()
        print(f"✅ Canciones del álbum '{nombre_album}' guardadas exitosamente.")
    except Exception as e:
        print(f"Error al guardar canciones del álbum '{nombre_album}': {e}")




@app.route('/ver_album/<id_album>')
def ver_album(id_album):
    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para ver los detalles del álbum.", "danger")
        return redirect(url_for('inicio_sesion'))

    usuario_id = session['usuario_id']
    cursor = conexion.connection.cursor()

    # Obtener los detalles del álbum
    cursor.execute("""
        SELECT id_album, nombre, artista, year, formato, url, lastfm_image, lastfm_url, sello_discografico, lastfm_tags, discogs_availability
        FROM albumes
        WHERE id_album = %s
    """, (id_album,))
    album = cursor.fetchone()

    if not album:
        flash("El álbum no existe o no está disponible.", "danger")
        return redirect(url_for('busqueda_albumes'))

    # Verificar si el álbum ya está en la wishlist
    cursor.execute("""
        SELECT 1 FROM wishlist
        WHERE id_usuario = %s AND id_album = %s
    """, (usuario_id, id_album))
    in_wishlist = cursor.fetchone() is not None

    # Obtener las canciones del álbum
    cursor.execute("""
        SELECT nombre, url
        FROM canciones
        WHERE id_album = %s
    """, (id_album,))
    canciones = [{"nombre": fila["nombre"], "url": fila["url"]} for fila in cursor.fetchall()]

    album_data = {
        "id_album": album["id_album"],
        "nombre": album["nombre"],
        "artista": album["artista"],
        "year": album["year"],
        "formato": album["formato"],
        "url": album["url"],
        "imagen": album["lastfm_image"],
        "lastfm_url": album["lastfm_url"],
        "sello": album["sello_discografico"],
        "tags": album["lastfm_tags"],
        "disponibilidad": "Disponible" if album["discogs_availability"] == 1 else "Agotado",
        "in_wishlist": in_wishlist  # Indica si el álbum está en la wishlist
    }

    # Capturar el parámetro 'from_page' para saber si viene de la wishlist
    from_page = request.args.get('from_page', 'busqueda_albumes')

    return render_template('visualizacionalbum.html', album=album_data, canciones=canciones, from_page=from_page)

@app.route('/add_to_wishlist/<id_album>', methods=['POST'])
def add_to_wishlist(id_album):
    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para añadir álbumes a tu wishlist.", "danger")
        return redirect(url_for('inicio_sesion'))

    usuario_id = session['usuario_id']
    id_wishlist = str(uuid.uuid4())  # Generar un identificador único para la wishlist
    cursor = conexion.connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO wishlist (id_wishlist, id_usuario, id_album)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE id_album = id_album
        """, (id_wishlist, usuario_id, id_album))
        conexion.connection.commit()

        # Obtener el nombre del álbum para la descripción
        cursor.execute("""
            SELECT nombre FROM albumes WHERE id_album = %s
        """, (id_album,))
        album = cursor.fetchone()
        descripcion = f"El álbum '{album['nombre']}' ha sido añadido a tu wishlist"

        # Insertar notificación con el nombre del álbum
        id_notificacion = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO notificaciones (id_notificacion, id_usuario, id_album, estado, descripcion)
            VALUES (%s, %s, %s, 'pendiente', %s)
        """, (id_notificacion, usuario_id, id_album, descripcion))
        conexion.connection.commit()

        flash("¡El álbum ha sido añadido a tu wishlist con éxito!", "success")
    except Exception as e:
        print(f"Error al añadir a la wishlist: {e}")
        flash("Ocurrió un error al intentar añadir el álbum a tu wishlist.", "danger")

    return redirect(url_for('ver_album', id_album=id_album))



@app.route('/remove_from_wishlist/<id_album>', methods=['POST'])
def remove_from_wishlist(id_album):
    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para eliminar álbumes de tu wishlist.", "danger")
        return redirect(url_for('inicio_sesion'))

    usuario_id = session['usuario_id']
    cursor = conexion.connection.cursor()
    try:
        cursor.execute("""
            DELETE FROM wishlist
            WHERE id_usuario = %s AND id_album = %s
        """, (usuario_id, id_album))
        conexion.connection.commit()

        # Obtener el nombre del álbum para la descripción
        cursor.execute("""
            SELECT nombre FROM albumes WHERE id_album = %s
        """, (id_album,))
        album = cursor.fetchone()
        descripcion = f"El álbum '{album['nombre']}' ha sido eliminado de tu wishlist"

        # Insertar notificación con el nombre del álbum
        id_notificacion = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO notificaciones (id_notificacion, id_usuario, id_album, estado, descripcion)
            VALUES (%s, %s, %s, 'pendiente', %s)
        """, (id_notificacion, usuario_id, id_album, descripcion))
        conexion.connection.commit()

        flash("¡El álbum ha sido eliminado de tu wishlist con éxito!", "success")
    except Exception as e:
        print(f"Error al eliminar de la wishlist: {e}")
        flash("Ocurrió un error al intentar eliminar el álbum de tu wishlist.", "danger")

    return redirect(url_for('wishlist'))

@app.route('/eliminar_notificacion/<id_notificacion>', methods=['GET'])
def eliminar_notificacion(id_notificacion):
    if 'usuario_id' not in session:
        return redirect(url_for('inicio_sesion'))

    usuario_id = session['usuario_id']
    cursor = conexion.connection.cursor()
    try:
        # Eliminamos la notificación solo si pertenece al usuario actual
        cursor.execute("""
            DELETE FROM notificaciones
            WHERE id_notificacion = %s AND id_usuario = %s
        """, (id_notificacion, usuario_id))
        conexion.connection.commit()  # Aseguramos que los cambios se guarden en la base de datos
    except Exception as e:
        print(f"Error al eliminar la notificación: {e}")
    
    return redirect(url_for('notificaciones'))  # Redirigir a la lista de notificaciones




@app.route('/wishlist')
def wishlist():
    if 'usuario_id' not in session:
        return redirect(url_for('inicio_sesion'))

    usuario_id = session['usuario_id']
    
    cursor = conexion.connection.cursor()
    cursor.execute("""
        SELECT albumes.id_album, albumes.nombre, albumes.artista, albumes.lastfm_image
        FROM wishlist
        JOIN albumes ON wishlist.id_album = albumes.id_album
        WHERE wishlist.id_usuario = %s
    """, (usuario_id,))
    
    wishlist_albumes = [{"id_album": fila["id_album"], "nombre": fila["nombre"], "artista": fila["artista"], "imagen": fila["lastfm_image"]} for fila in cursor.fetchall()]
    
    return render_template('wishlist.html', wishlist_albumes=wishlist_albumes)

@app.route('/eliminar_wishlist/<id_album>', methods=['POST'])
def eliminar_wishlist(id_album):
    if 'usuario_id' not in session:
        return redirect(url_for('inicio_sesion'))

    usuario_id = session['usuario_id']
    
    cursor = conexion.connection.cursor()
    cursor.execute("""
        DELETE FROM wishlist 
        WHERE id_usuario = %s AND id_album = %s
    """, (usuario_id, id_album))
    conexion.connection.commit()
    
    return redirect(url_for('wishlist'))

@app.route('/notificaciones', methods=['GET', 'POST'])
def notificaciones():
    if 'usuario_id' not in session:
        return redirect(url_for('inicio_sesion'))

    usuario_id = session['usuario_id']
    
    cursor = conexion.connection.cursor()
    cursor.execute("""
        SELECT notificaciones.id_notificacion, notificaciones.fecha_creacion, 
               notificaciones.descripcion, albumes.nombre AS album, notificaciones.estado
        FROM notificaciones
        LEFT JOIN albumes ON notificaciones.id_album = albumes.id_album
        WHERE notificaciones.id_usuario = %s
    """, (usuario_id,))
    
    lista_notificaciones = cursor.fetchall()
    
    return render_template('notificaciones.html', notificaciones=lista_notificaciones)

@app.route('/marcar_visto/<id_notificacion>', methods=['POST'])
def marcar_visto(id_notificacion):
    if 'usuario_id' not in session:
        return redirect(url_for('inicio_sesion'))

    cursor = conexion.connection.cursor()
    cursor.execute("""
        UPDATE notificaciones
        SET estado = 'enviada'
        WHERE id_notificacion = %s
    """, (id_notificacion,))
    conexion.connection.commit()
    
    return redirect(url_for('notificaciones'))

@app.route('/buscar_artista', methods=['GET', 'POST'])
def buscar_artista_view():
    """ Vista para buscar artistas en Discogs """
    artistas = []
    
    if request.method == 'POST':
        busqueda = request.form['busqueda']
        artistas = obtener_artistas_discogs(busqueda)  # Llama a la función de la API
    
    return render_template('buscar_artista.html', artistas=artistas)





if __name__ == '__main__':
    app.register_error_handler(404, lambda e: 'Recurso no encontrado')
    app.run(debug=True)
