<?php
require_once __DIR__ . '/../conexion.php';

class Usuario {
    private $db;

    public function __construct() {
        $this->db = Conexion::conectar();
    }

    // busca por nombre o por correo (para el login)
    public function obtenerPorNombreOCorreo($valor) {
        $sql = "SELECT * FROM usuarios WHERE nombre = :val OR correo = :val";
        $stmt = $this->db->prepare($sql);
        $stmt->execute([':val' => $valor]);
        return $stmt->fetch();
    }

    public function obtenerTodos() {
        $stmt = $this->db->query("SELECT * FROM usuarios");
        return $stmt->fetchAll();
    }

    public function obtenerPorId($id) {
        $stmt = $this->db->prepare("SELECT * FROM usuarios WHERE id = :id");
        $stmt->execute([':id' => $id]);
        return $stmt->fetch();
    }

    public function crear($nombre, $correo, $pass, $edad, $tipo, $dinero) {
        $hash = password_hash($pass, PASSWORD_DEFAULT);
        $sql = "INSERT INTO usuarios (nombre, correo, contrasena, edad, tipo, dinero) 
                VALUES (:nombre, :correo, :pass, :edad, :tipo, :dinero)";
        $stmt = $this->db->prepare($sql);
        return $stmt->execute([
            ':nombre' => $nombre,
            ':correo' => $correo,
            ':pass' => $hash,
            ':edad' => $edad,
            ':tipo' => $tipo,
            ':dinero' => $dinero
        ]);
    }

    public function actualizar($id, $nombre, $correo, $pass, $edad, $tipo, $dinero) {
        // si manda contraseña nueva la actualizo, sino la dejo igual
        if (!empty($pass)) {
            $hash = password_hash($pass, PASSWORD_DEFAULT);
            $sql = "UPDATE usuarios SET nombre=:nombre, correo=:correo, contrasena=:pass, edad=:edad, tipo=:tipo, dinero=:dinero WHERE id=:id";
            $params = [':nombre'=>$nombre, ':correo'=>$correo, ':pass'=>$hash, ':edad'=>$edad, ':tipo'=>$tipo, ':dinero'=>$dinero, ':id'=>$id];
        } else {
            $sql = "UPDATE usuarios SET nombre=:nombre, correo=:correo, edad=:edad, tipo=:tipo, dinero=:dinero WHERE id=:id";
            $params = [':nombre'=>$nombre, ':correo'=>$correo, ':edad'=>$edad, ':tipo'=>$tipo, ':dinero'=>$dinero, ':id'=>$id];
        }
        $stmt = $this->db->prepare($sql);
        return $stmt->execute($params);
    }

    public function eliminar($id) {
        // no me puedo eliminar a mi mismo
        if ($_SESSION['user_id'] == $id) return false;

        $stmt = $this->db->prepare("DELETE FROM usuarios WHERE id = :id");
        return $stmt->execute([':id' => $id]);
    }

    public function actualizarPerfil($id, $nombre, $pass) {
        if (!empty($pass)) {
            $hash = password_hash($pass, PASSWORD_DEFAULT);
            $stmt = $this->db->prepare("UPDATE usuarios SET nombre=:nombre, contrasena=:pass WHERE id=:id");
            $stmt->execute([':nombre'=>$nombre, ':pass'=>$hash, ':id'=>$id]);
        } else {
            $stmt = $this->db->prepare("UPDATE usuarios SET nombre=:nombre WHERE id=:id");
            $stmt->execute([':nombre'=>$nombre, ':id'=>$id]);
        }
    }

    public function actualizarDinero($id, $nuevoSaldo) {
        $stmt = $this->db->prepare("UPDATE usuarios SET dinero=:dinero WHERE id=:id");
        return $stmt->execute([':dinero'=>$nuevoSaldo, ':id'=>$id]);
    }

    public function verificarContrasena($pass, $hash) {
        // permite login con contraseña en texto plano (ej: el admin por defecto)
        if (password_verify($pass, $hash)) return true;
        return $pass === $hash;
    }
}
