<?php

class UserController {
    private $usuarioModel;
    private $productoModel;

    public function __construct() {
        if (!isset($_SESSION['user_id']) || $_SESSION['user_tipo'] != 'user') {
            header('Location: index.php?controller=Auth&action=login');
            exit;
        }
        $this->usuarioModel  = new Usuario();
        $this->productoModel = new Producto();
    }

    public function perfil() {
        $id      = $_SESSION['user_id'];
        $usuario = $this->usuarioModel->obtenerPorId($id);
        $error   = '';
        $success = '';

        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $nombre = trim($_POST['nombre']);
            $pass   = trim($_POST['contrasena']);

            if (empty($nombre)) {
                $error = 'El nombre no puede quedar vacío.';
            } else {
                $this->usuarioModel->actualizarPerfil($id, $nombre, $pass);
                $_SESSION['user_nombre'] = $nombre;
                $usuario = $this->usuarioModel->obtenerPorId($id);
                $success = 'Perfil actualizado.';
            }
        }

        require_once __DIR__ . '/../views/user/perfil.php';
    }

    public function comprar() {
        $productos = $this->productoModel->obtenerTodos();
        $productoSeleccionado = null;
        $idSeleccionado = isset($_GET['id_producto']) ? intval($_GET['id_producto']) : null;

        if ($idSeleccionado) {
            $productoSeleccionado = $this->productoModel->obtenerPorId($idSeleccionado);
        }

        $error   = '';
        $success = '';

        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $idProducto    = intval($_POST['id_producto']);
            $cajasComprar  = intval($_POST['cajas_comprar']);

            $producto = $this->productoModel->obtenerPorId($idProducto);
            $usuario  = $this->usuarioModel->obtenerPorId($_SESSION['user_id']);

            if (!$producto) {
                $error = 'Ese producto no existe.';
            } elseif ($cajasComprar <= 0) {
                $error = 'Debes comprar al menos 1 caja.';
            } else {
                $total = $cajasComprar * $producto['precio'];

                if ($usuario['edad'] < $producto['edad_restriccion']) {
                    $error = 'No tienes la edad mínima para comprar este producto (mínimo ' . $producto['edad_restriccion'] . ' años).';
                } elseif ($producto['cajas'] < $cajasComprar) {
                    $error = 'No hay suficiente stock. Solo quedan ' . $producto['cajas'] . ' cajas.';
                } elseif ($usuario['dinero'] < $total) {
                    $error = 'No tienes suficiente saldo. Necesitas $' . number_format($total, 2) . ' y tienes $' . number_format($usuario['dinero'], 2) . '.';
                } else {
                    $this->productoModel->sacarCajas($idProducto, $cajasComprar);

                    $nuevoSaldo = $usuario['dinero'] - $total;
                    $this->usuarioModel->actualizarDinero($usuario['id'], $nuevoSaldo);
                    $_SESSION['user_dinero'] = $nuevoSaldo;

                    $success = 'Compra exitosa. Compraste ' . $cajasComprar . ' cajas de "' . $producto['nombre'] . '" por $' . number_format($total, 2) . '.';

                    // actualizo la lista y el detalle
                    $productos = $this->productoModel->obtenerTodos();
                    if ($idSeleccionado == $idProducto) {
                        $productoSeleccionado = $this->productoModel->obtenerPorId($idProducto);
                    }
                }
            }
        }

        require_once __DIR__ . '/../views/user/comprar.php';
    }
}
