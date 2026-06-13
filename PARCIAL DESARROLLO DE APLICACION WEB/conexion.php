<?php

// conexion a la base de datos
$host = "localhost";
$dbname = "parcial_web";
$user = "root";
$pass = "";

class Conexion {
    private static $pdo = null;

    public static function conectar() {
        if (self::$pdo == null) {
            try {
                $dsn = "mysql:host=localhost;dbname=parcial_web;charset=utf8mb4";
                self::$pdo = new PDO($dsn, "root", "", [
                    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
                ]);
            } catch (PDOException $e) {
                die("Error al conectar con la BD: " . $e->getMessage());
            }
        }
        return self::$pdo;
    }
}
