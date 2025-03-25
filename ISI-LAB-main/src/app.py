from flask import Flask, json, request, render_template, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from config import config
from discogs_api import obtener_artistas_discogs, obtener_info_discogs  # Importar funciones de la API de Discogs
from lastfm_api import  obtener_info_album_lastfm, obtener_artistas_lastfm, obtener_info_artista_lastfm  # Importar funciones de la API de last.fm
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

def buscar_artistas_en_api(busqueda):
    """ 
    Busca primero en Discogs y usa esos resultados para buscar información más completa en Last.fm.
    """
    artistas_discogs = obtener_artistas_discogs(busqueda)
    artistas_completos = []

    if not artistas_discogs:
        print("⚠️ No se encontraron artistas en Discogs.")
        return []

    for artista in artistas_discogs:
        nombre = artista.get("nombre", "").strip()
        imagen_discogs = artista.get("imagen", "")
        url_discogs = artista.get("url", "#")

        # 🔹 Llamada a getinfo de Last.fm (para datos completos del artista)
        info_lastfm = obtener_info_artista_lastfm(nombre)  # Esta función debe ser tipo artist.getinfo

        artista_completo = {
            "id_artista": None,
            "nombre": nombre,
            "biografia": info_lastfm.get("biografia", "No disponible"),
            "imagen": imagen_discogs if imagen_discogs else info_lastfm.get("imagen", ""),
            "url_discogs": url_discogs,
            "url_lastfm": info_lastfm.get("url_lastfm", "#"),
            "listeners": info_lastfm.get("listeners", 0),
            "plays": info_lastfm.get("plays", 0),
            "tags": info_lastfm.get("tags", "No especificado"),
        }

        artistas_completos.append(artista_completo)

    print(f"✅ Artistas procesados con datos combinados: {artistas_completos}")
    return artistas_completos


@app.route('/busqueda_artistas', methods=['GET', 'POST'])
def busqueda_artistas():
    artistas = []

    if request.method == 'POST':
        busqueda = request.form['busqueda'].strip()

        # 🔹 1. Buscar en la base de datos
        cursor = conexion.connection.cursor()
        cursor.execute("""
            SELECT id_artista, nombre, biografia, imagen, url_discogs, url_lastfm, listeners, plays, tags
            FROM artistas
            WHERE LOWER(nombre) = LOWER(%s)
        """, (busqueda,))
        
        artistas_bd = [dict(fila) for fila in cursor.fetchall()]
        print("🎵 Artistas en BD:", artistas_bd)

        if not artistas_bd:  # Solo busca en API si no lo encuentra en la BD
            print("🔍 No encontrado en BD. Buscando en API...")
            artistas_api = buscar_artistas_en_api(busqueda)

            # Guardar en la BD los artistas nuevos
            for artista in artistas_api:
                guardar_artista(
                    id_artista=artista["id_artista"],
                    nombre=artista["nombre"],
                    biografia=artista["biografia"],
                    imagen=artista["imagen"],
                    url_discogs=artista["url_discogs"],
                    url_lastfm=artista["url_lastfm"],
                    listeners=artista["listeners"],
                    plays=artista["plays"],
                    tags=artista["tags"]
                )

            artistas = artistas_api  # Mostrar los nuevos resultados de la API
        else:
            print("✅ Artista encontrado en BD.")
            artistas = artistas_bd  # Mostrar los resultados de la BD

    return render_template('busqueda_artistas.html', artistas=artistas)

# --------------------------------------------------------------------------------------------------------------------------------- #

@app.route('/discografia/<artista>')
def discografia(artista):
    cursor = conexion.connection.cursor()
    cursor.execute("""
        SELECT nombre, year, formato, url
        FROM albumes 
        WHERE artista = %s
    """, (artista,))
    
    albumes = cursor.fetchall()
    return render_template('discografia.html', artista=artista, albumes=albumes)


@app.route('/busqueda_albumes', methods=['GET', 'POST'])
def busqueda_albumes():
    albumes = []  # Lista para almacenar los resultados finales
    mensaje_error = None  # Variable para almacenar el mensaje de error

    # Capturar el nombre del artista si se pasa como parámetro en la URL
    nombre_artista = request.args.get('artista', '').strip()

    if request.method == 'POST':
        busqueda = request.form['busqueda'].strip()  # Eliminar espacios extra
    else:
        # Si se llega desde "Consultar Discografía", usar el nombre del artista como búsqueda inicial
        busqueda = nombre_artista

    if busqueda:
        try:
            # Buscar en la base de datos
            cursor = conexion.connection.cursor()
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
                albumes_api = obtener_info_album_lastfm(busqueda)  # Llama a la función de la API para buscar álbumes

                if albumes_api:
                    # Guardar en la BD los álbumes nuevos
                    for album in albumes_api:
                        cursor.execute("""
                            INSERT INTO albumes (id_album, nombre, artista, year, formato, url, lastfm_image, lastfm_url)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (album["id_album"], album["nombre"], album["artista"], album["year"],
                              album["formato"], album["url"], album["imagen"], album["lastfm_url"]))
                        conexion.connection.commit()

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

    return render_template('busqueda_albumes.html', albumes=albumes, nombre_artista=nombre_artista, mensaje_error=mensaje_error)

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

    return render_template('visualizacionalbum.html', album=album_data, from_page=from_page)

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
        flash("¡El álbum ha sido eliminado de tu wishlist con éxito!", "success")
    except Exception as e:
        print(f"Error al eliminar de la wishlist: {e}")
        flash("Ocurrió un error al intentar eliminar el álbum de tu wishlist.", "danger")

    return redirect(url_for('wishlist'))

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
               albumes.nombre AS album, notificaciones.estado
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


@app.route('/discografia_discogs/<artista_id>')
def discografia_discogs(artista_id):
    """ Vista para mostrar la discografía de un artista en Discogs """
    #discografia = obtener_discografia(artista_id)
    return render_template('discografia_discogs.html', discografia=discografia)


if __name__ == '__main__':
    app.register_error_handler(404, lambda e: 'Recurso no encontrado')
    app.run(debug=True)
