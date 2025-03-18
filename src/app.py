from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from config import config  # Importa la configuración

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
        
        if usuario and check_password_hash(usuario[1], contraseña):
            session['usuario_id'] = usuario[0]
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
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
    artistas = []
    
    if request.method == 'POST':
        busqueda = request.form['busqueda']
        
        cursor = conexion.connection.cursor()
        cursor.execute("""
            SELECT DISTINCT artista 
            FROM albumes 
            WHERE artista LIKE %s
        """, ('%' + busqueda + '%',))
        
        artistas = cursor.fetchall()
    
    return render_template('busqueda_artistas.html', artistas=artistas)

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

@app.route('/busqueda_canciones', methods=['GET', 'POST'])
def busqueda_canciones():
    canciones = []

    if request.method == 'POST':
        busqueda = request.form['busqueda']

        cursor = conexion.connection.cursor()
        cursor.execute("""
            SELECT DISTINCT nombre, id_album 
            FROM albumes 
            WHERE nombre LIKE %s
        """, ('%' + busqueda + '%',))

        canciones = cursor.fetchall()

    return render_template('busqueda_canciones.html', canciones=canciones)


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


if __name__ == '__main__':
    app.register_error_handler(404, lambda e: 'Recurso no encontrado')
    app.run(debug=True)
