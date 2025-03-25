from flask import Flask, json, request, render_template, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from config import config
from discogs_api import obtener_artistas_discogs, obtener_info_discogs  # Importar funciones de la API de Discogs
from lastfm_api import obtener_info_album_lastfm, obtener_artistas_lastfm, obtener_info_artista_lastfm  # Importar funciones de la API de last.fm
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

    # 🔹 Capturar el nombre del artista si se pasa como parámetro en la URL
    nombre_artista = request.args.get('artista', '').strip()

    if request.method == 'POST':
        busqueda = request.form['busqueda'].strip()  # Eliminar espacios extra
    else:
        # Si se llega desde "Consultar Discografía", usar el nombre del artista como búsqueda inicial
        busqueda = nombre_artista

    if busqueda:
        # 🔹 1. Buscar en la base de datos (SIN LÍMITE)
        cursor = conexion.connection.cursor()
        cursor.execute("""
            SELECT DISTINCT nombre, artista, year, formato, url 
            FROM albumes 
            WHERE LOWER(nombre) LIKE LOWER(%s) OR LOWER(artista) = LOWER(%s)
        """, ('%' + busqueda + '%', busqueda))

        albumes_bd = [{"nombre": fila["nombre"], "artista": fila["artista"], "year": fila["year"], 
                       "formato": fila["formato"], "url": fila["url"]} for fila in cursor.fetchall()]
        print("📀 Álbumes en BD:", albumes_bd)

        # 🔹 2. Combinar resultados finales
        albumes = albumes_bd

        print("✅ Lista final de álbumes:", albumes)

    return render_template('busqueda_albumes.html', albumes=albumes, nombre_artista=nombre_artista)


@app.route('/ver_album/<id_album>')
def ver_album(id_album):
    cursor = conexion.connection.cursor()
    cursor.execute("""
        SELECT nombre, artista, year, formato, url 
        FROM albumes 
        WHERE id_album = %s
    """, (id_album,))

    album = cursor.fetchone()
    
    return render_template('ver_album.html', album=album)

@app.route('/wishlist')
def wishlist():
    if 'usuario_id' not in session:
        return redirect(url_for('inicio_sesion'))

    usuario_id = session['usuario_id']
    
    cursor = conexion.connection.cursor()
    cursor.execute("""
        SELECT albumes.id_album, albumes.nombre, albumes.artista 
        FROM wishlist
        JOIN albumes ON wishlist.id_album = albumes.id_album
        WHERE wishlist.id_usuario = %s
    """, (usuario_id,))
    
    wishlist_albumes = cursor.fetchall()
    
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
