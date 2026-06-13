<?php

class AdminController {
    private $usuarioModel;
    private $productoModel;

    public function __construct() {
        // verifico que sea admin
        if (!isset($_SESSION['user_id']) || $_SESSION['user_tipo'] != 'admin') {
            header('Location: index.php?controller=Auth&action=login');
            exit;
        }
        $this->usuarioModel = new Usuario();
        $this->productoModel = new Producto();
    }

    public function usuarios() {
        $usuarios = $this->usuarioModel->obtenerTodos();
        require_once __DIR__ . '/../views/admin/usuarios_list.php';
    }

    public function crearUsuario() {
        $error = '';
        $success = '';

        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $nombre = trim($_POST['nombre']);
            $correo = trim($_POST['correo']);
            $pass   = trim($_POST['contrasena']);
            $edad   = intval($_POST['edad']);
            $tipo   = $_POST['tipo'];
            $dinero = floatval($_POST['dinero']);

            if (empty($nombre) || empty($correo) || empty($pass) || empty($_POST['edad']) || empty($tipo)) {
                $error = 'Todos los campos son obligatorios.';
            } else {
                $existe = $this->usuarioModel->obtenerPorNombreOCorreo($correo);
                $existeNombre = $this->usuarioModel->obtenerPorNombreOCorreo($nombre);

                if ($existe || $existeNombre) {
                    $error = 'El nombre o correo ya está en uso.';
                } else {
                    $this->usuarioModel->crear($nombre, $correo, $pass, $edad, $tipo, $dinero);
                    header('Location: index.php?controller=Admin&action=usuarios&success=Usuario creado correctamente.');
                    exit;
                }
            }
        }

        require_once __DIR__ . '/../views/admin/usuario_form.php';
    }

    public function editarUsuario() {
        $id = isset($_GET['id']) ? intval($_GET['id']) : 0;
        $usuario = $this->usuarioModel->obtenerPorId($id);

        if (!$usuario) {
            header('Location: index.php?controller=Admin&action=usuarios');
            exit;
        }

        $error = '';

        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $nombre = trim($_POST['nombre']);
            $correo = trim($_POST['correo']);
            $pass   = trim($_POST['contrasena']);
            $edad   = intval($_POST['edad']);
            $tipo   = $_POST['tipo'];
            $dinero = floatval($_POST['dinero']);

            if (empty($nombre) || empty($correo) || empty($_POST['edad']) || empty($tipo)) {
                $error = 'Los campos nombre, correo, edad y tipo son obligatorios.';
            } else {
                $existe = $this->usuarioModel->obtenerPorNombreOCorreo($correo);
                if ($existe && $existe['id'] != $id) {
                    $error = 'Ese correo ya lo usa otro usuario.';
                } else {
                    $this->usuarioModel->actualizar($id, $nombre, $correo, $pass, $edad, $tipo, $dinero);
                    header('Location: index.php?controller=Admin&action=usuarios&success=Usuario actualizado.');
                    exit;
                }
            }
        }

        require_once __DIR__ . '/../views/admin/usuario_form.php';
    }

    public function eliminarUsuario() {
        $id = isset($_GET['id']) ? intval($_GET['id']) : 0;

        if ($this->usuarioModel->eliminar($id)) {
            header('Location: index.php?controller=Admin&action=usuarios&success=Usuario eliminado.');
        } else {
            header('Location: index.php?controller=Admin&action=usuarios&error=No se puede eliminar ese usuario.');
        }
        exit;
    }

    public function bodega() {
        $productos = $this->productoModel->obtenerTodos();
        require_once __DIR__ . '/../views/admin/bodega_list.php';
    }

    public function registrarProducto() {
        $error = '';

        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $nombre  = trim($_POST['nombre']);
            $codigo  = trim($_POST['codigo']);
            $cajas   = intval($_POST['cajas']);
            $precio  = floatval($_POST['precio']);
            $edad    = intval($_POST['edad_restriccion']);

            if (empty($nombre) || empty($codigo) || $precio < 0 || $edad < 0) {
                $error = 'Revisa los campos, algunos están vacíos o tienen valores inválidos.';
            } else {
                $existe = $this->productoModel->obtenerPorCodigo($codigo);
                if ($existe) {
                    $error = 'Ya existe un producto con ese código.';
                } else {
                    $this->productoModel->registrar($nombre, $codigo, $cajas, $precio, $edad);
                    header('Location: index.php?controller=Admin&action=bodega&success=Producto registrado.');
                    exit;
                }
            }
        }

        require_once __DIR__ . '/../views/admin/producto_form.php';
    }

    public function cajas() {
        $id = isset($_GET['id']) ? intval($_GET['id']) : 0;
        $producto = $this->productoModel->obtenerPorId($id);

        if (!$producto) {
            header('Location: index.php?controller=Admin&action=bodega');
            exit;
        }

        $error = '';

        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $accion   = $_POST['accion'];
            $cantidad = intval($_POST['cantidad']);

            if ($cantidad <= 0) {
                $error = 'La cantidad debe ser mayor a 0.';
            } else {
                if ($accion == 'ingresar') {
                    $this->productoModel->ingresarCajas($id, $cantidad);
                    header('Location: index.php?controller=Admin&action=bodega&success=Cajas ingresadas.');
                    exit;
                } elseif ($accion == 'sacar') {
                    if ($cantidad > $producto['cajas']) {
                        $error = 'No hay suficientes cajas. Hay ' . $producto['cajas'] . ' disponibles.';
                    } else {
                        $this->productoModel->sacarCajas($id, $cantidad);
                        header('Location: index.php?controller=Admin&action=bodega&success=Cajas retiradas.');
                        exit;
                    }
                }
            }
        }

        require_once __DIR__ . '/../views/admin/bodega_cajas.php';
    }
}
