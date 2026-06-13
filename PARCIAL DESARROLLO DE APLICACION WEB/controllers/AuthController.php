<?php

class AuthController {
    private $usuarioModel;

    public function __construct() {
        $this->usuarioModel = new Usuario();
    }

    public function login() {
        // si ya inicio sesion lo mando directo
        if (isset($_SESSION['user_id'])) {
            if ($_SESSION['user_tipo'] == 'admin') {
                header('Location: index.php?controller=Admin&action=usuarios');
            } else {
                header('Location: index.php?controller=User&action=comprar');
            }
            exit;
        }

        $error = '';

        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $usuario = trim($_POST['usuario']);
            $pass = trim($_POST['contrasena']);

            if (empty($usuario) || empty($pass)) {
                $error = 'Completa todos los campos.';
            } else {
                $datos = $this->usuarioModel->obtenerPorNombreOCorreo($usuario);

                if ($datos && $this->usuarioModel->verificarContrasena($pass, $datos['contrasena'])) {
                    $_SESSION['user_id']     = $datos['id'];
                    $_SESSION['user_nombre'] = $datos['nombre'];
                    $_SESSION['user_correo'] = $datos['correo'];
                    $_SESSION['user_tipo']   = $datos['tipo'];
                    $_SESSION['user_edad']   = $datos['edad'];
                    $_SESSION['user_dinero'] = $datos['dinero'];

                    if ($datos['tipo'] == 'admin') {
                        header('Location: index.php?controller=Admin&action=usuarios');
                    } else {
                        header('Location: index.php?controller=User&action=comprar');
                    }
                    exit;
                } else {
                    $error = 'Usuario o contraseña incorrectos.';
                }
            }
        }

        require_once __DIR__ . '/../views/login.php';
    }

    public function logout() {
        session_destroy();
        header('Location: index.php?controller=Auth&action=login');
        exit;
    }
}
