CREATE DATABASE IF NOT EXISTS parcial_web;
USE parcial_web;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    edad INT NOT NULL,
    tipo ENUM('admin', 'user') NOT NULL,
    dinero DECIMAL(10, 2) NOT NULL DEFAULT 0.00
);

CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    cajas INT NOT NULL DEFAULT 0,
    precio DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    edad_restriccion INT NOT NULL DEFAULT 0
);

INSERT INTO usuarios (nombre, correo, contrasena, edad, tipo, dinero) 
VALUES ('admin', 'admin@admin.com', 'admin', 30, 'admin', 1000.00)
ON DUPLICATE KEY UPDATE nombre=nombre;
