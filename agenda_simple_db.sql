CREATE DATABASE IF NOT EXISTS agenda_simple_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE agenda_simple_db;

CREATE TABLE IF NOT EXISTS clientes (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL,
    dni VARCHAR(20) NOT NULL,
    telefono VARCHAR(30) NULL,
    created_at TIMESTAMP(6) NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at TIMESTAMP(6) NULL DEFAULT CURRENT_TIMESTAMP(6)
        ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    INDEX clientes_nombre_apellido_idx (apellido, nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS citas (
    id INT NOT NULL AUTO_INCREMENT,
    client_id INT NOT NULL,
    asunto VARCHAR(200) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    referencia VARCHAR(255) NULL,
    notas TEXT NULL,
    estado ENUM('pendiente', 'confirmada', 'realizada', 'cancelada')
        NULL DEFAULT 'pendiente',
    created_at TIMESTAMP(6) NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at TIMESTAMP(6) NULL DEFAULT CURRENT_TIMESTAMP(6)
        ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    INDEX citas_client_id_idx (client_id),
    INDEX citas_fecha_hora_idx (fecha, hora),
    CONSTRAINT citas_client_id_fk
        FOREIGN KEY (client_id) REFERENCES clientes (id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
