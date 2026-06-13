<?php
require_once __DIR__ . '/../conexion.php';

class Producto {
    private $db;

    public function __construct() {
        $this->db = Conexion::conectar();
    }

    public function obtenerTodos() {
        $stmt = $this->db->query("SELECT * FROM productos");
        return $stmt->fetchAll();
    }

    public function obtenerPorId($id) {
        $stmt = $this->db->prepare("SELECT * FROM productos WHERE id = :id");
        $stmt->execute([':id' => $id]);
        return $stmt->fetch();
    }

    public function obtenerPorCodigo($codigo) {
        $stmt = $this->db->prepare("SELECT * FROM productos WHERE codigo = :codigo");
        $stmt->execute([':codigo' => $codigo]);
        return $stmt->fetch();
    }

    public function registrar($nombre, $codigo, $cajas, $precio, $edad_min) {
        $sql = "INSERT INTO productos (nombre, codigo, cajas, precio, edad_restriccion) 
                VALUES (:nombre, :codigo, :cajas, :precio, :edad)";
        $stmt = $this->db->prepare($sql);
        return $stmt->execute([
            ':nombre' => $nombre,
            ':codigo' => $codigo,
            ':cajas' => $cajas,
            ':precio' => $precio,
            ':edad' => $edad_min
        ]);
    }

    public function ingresarCajas($id, $cantidad) {
        $stmt = $this->db->prepare("UPDATE productos SET cajas = cajas + :cant WHERE id = :id");
        return $stmt->execute([':cant' => $cantidad, ':id' => $id]);
    }

    public function sacarCajas($id, $cantidad) {
        $prod = $this->obtenerPorId($id);
        if (!$prod || $prod['cajas'] < $cantidad) return false;

        $stmt = $this->db->prepare("UPDATE productos SET cajas = cajas - :cant WHERE id = :id");
        return $stmt->execute([':cant' => $cantidad, ':id' => $id]);
    }
}
