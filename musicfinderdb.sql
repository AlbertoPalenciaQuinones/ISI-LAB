CREATE DATABASE IF NOT EXISTS musicfinder;
use musicfinder;

CREATE TABLE usuarios (
    id_usuario VARCHAR(36) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE albumes (
    id_album VARCHAR(255) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    artista VARCHAR(255) NOT NULL,
    year INT,
    formato VARCHAR(100),
    url VARCHAR(500),
    sello_discografico TEXT,
    rating FLOAT,
    lastfm_listeners INT,
    lastfm_plays INT,
    lastfm_url VARCHAR(500),
    lastfm_image VARCHAR(500),
    lastfm_tags VARCHAR(500),
    discogs_availability BOOLEAN
);

CREATE TABLE wishlist (
    id_wishlist VARCHAR(36) PRIMARY KEY,
    id_usuario VARCHAR(36),
    id_album VARCHAR(255),
    fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_album) REFERENCES albumes(id_album) ON DELETE CASCADE
);

CREATE TABLE notificaciones (
    id_notificacion VARCHAR(36) PRIMARY KEY,
    id_usuario VARCHAR(36),
    id_album VARCHAR(255),
    estado VARCHAR(20) CHECK (estado IN ('pendiente', 'enviada')),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_album) REFERENCES albumes(id_album) ON DELETE CASCADE
);
CREATE TABLE usuarios (
    id_usuario VARCHAR(36) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
