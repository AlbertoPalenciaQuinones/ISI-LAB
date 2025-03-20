from flask import Flask, json, request, render_template, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from config import config
from discogs_api import obtener_artistas_discogs, obtener_info_discogs  # Importar funciones de la API de Discogs
from lastfm_api import obtener_info_album_lastfm, obtener_artistas_lastfm  # Importar funciones de la API de last.fm

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


@app.route('/busqueda_artistas', methods=['GET', 'POST'])
def busqueda_artistas():
    artistas = []  # Lista para almacenar los resultados finales

    if request.method == 'POST':
        busqueda = request.form['busqueda'].strip()  # Eliminar espacios extra
        
        # 🔹 1. Buscar en la base de datos (SIN LÍMITE)
        cursor = conexion.connection.cursor()
        cursor.execute("""
            SELECT DISTINCT artista 
            FROM albumes 
            WHERE LOWER(artista) = LOWER(%s)
        """, (busqueda,))
        
        artistas_bd = [{"nombre": fila["artista"]} for fila in cursor.fetchall()]
        print("🎵 Artistas en BD:", artistas_bd)

        # 🔹 2. Buscar en las APIs (limitado a 5 artistas adicionales)
        artistas_api = buscar_artistas_en_api(busqueda)

        # 🔹 3. Filtrar resultados para que solo coincidan EXACTAMENTE con el nombre
        artistas_api_filtrados = []
        for artista in artistas_api:
            if isinstance(artista, dict):  
                nombre_artista = artista.get("nombre", "").strip().lower()
                if nombre_artista == busqueda.lower():  # Comparar nombres exactos
                    artistas_api_filtrados.append(artista)

        print("🎶 Artistas encontrados en API (filtrados):", artistas_api_filtrados)

        # 🔹 4. Evitar duplicados y agregar TODOS los artistas nuevos a la BD
        nombres_bd = {artista["nombre"].lower() for artista in artistas_bd}
        artistas_nuevos = [artista for artista in artistas_api_filtrados if artista["nombre"].lower() not in nombres_bd]

        # Guardar en la base de datos los artistas nuevos
      #  for artista in artistas_nuevos:
           # guardar_artista(
              #  id_artista=artista.get("id_artista", None),
               # nombre=artista.get("nombre", ""),
                #biografia=artista.get("biografia", "No disponible"),
                #imagen=artista.get("imagen", ""),
                #url_discogs=artista.get("url_discogs", ""),
                #url_lastfm=artista.get("url_lastfm", ""),
                #listeners=artista.get("listeners", None),
                #plays=artista.get("plays", None),
                #tags=artista.get("tags", "")
          #  )

        # 🔹 5. Combinar resultados finales
        artistas = artistas_bd + artistas_nuevos

        print("✅ Lista final de artistas (guardados en BD):", artistas)
    
    return render_template('busqueda_artistas.html', artistas=artistas)


# 🔹 Función para buscar artistas en las APIs de Discogs y Last.fm
def buscar_artistas_en_api(busqueda):
    """ Busca artistas en Discogs y Last.fm, pero devuelve máximo 5 nuevos artistas """
    artistas_encontrados = []

    # 📌 Buscar en Discogs
    artistas_discogs = obtener_artistas_discogs(busqueda)
    if artistas_discogs:
        artistas_encontrados.extend(artistas_discogs)

    # 📌 Buscar en Last.fm
    artistas_lastfm = obtener_artistas_lastfm(busqueda)
    if artistas_lastfm:
        artistas_encontrados.extend(artistas_lastfm)

    return artistas_encontrados  # 🔹 Retorna todos los encontrados (luego filtramos en `busqueda_artistas`)




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

    if request.method == 'POST':
        busqueda = request.form['busqueda'].strip()  # Eliminar espacios extra

        # 🔹 1. Buscar en la base de datos (SIN LÍMITE)
        cursor = conexion.connection.cursor()
        cursor.execute("""
            SELECT DISTINCT nombre, artista, year, formato, url 
            FROM albumes 
            WHERE LOWER(nombre) LIKE LOWER(%s)
        """, ('%' + busqueda + '%',))

        albumes_bd = [{"nombre": fila["nombre"], "artista": fila["artista"], "year": fila["year"], 
                       "formato": fila["formato"], "url": fila["url"]} for fila in cursor.fetchall()]
        print("📀 Álbumes en BD:", albumes_bd)

        # 🔹 2. No se realiza búsqueda en APIs externas en este caso

        # 🔹 3. Evitar duplicados (ya que no hay APIs, no es necesario filtrar)

        # 🔹 4. Combinar resultados finales
        albumes = albumes_bd

        print("✅ Lista final de álbumes:", albumes)

    return render_template('busqueda_albumes.html', albumes=albumes)


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
