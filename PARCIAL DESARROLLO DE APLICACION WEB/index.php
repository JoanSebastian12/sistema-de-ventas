<?php

session_start();

require_once 'conexion.php';
require_once 'models/Usuario.php';
require_once 'models/Producto.php';

// agarro el controlador y accion de la url, por defecto va al login
$ctrl = isset($_GET['controller']) ? $_GET['controller'] : 'Auth';
$accion = isset($_GET['action']) ? $_GET['action'] : 'login';

$clase = $ctrl . 'Controller';
$archivo = "controllers/{$clase}.php";

if (!file_exists($archivo)) {
    $clase = 'AuthController';
    $archivo = 'controllers/AuthController.php';
    $accion = 'login';
}

require_once $archivo;

$obj = new $clase();

if (method_exists($obj, $accion)) {
    $obj->$accion();
} else {
    header('Location: index.php?controller=Auth&action=login');
    exit;
}
