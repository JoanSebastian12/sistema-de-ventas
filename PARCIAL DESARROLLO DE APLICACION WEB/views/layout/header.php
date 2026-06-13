<?php
$ctrl   = isset($_GET['controller']) ? $_GET['controller'] : 'Auth';
$accion = isset($_GET['action']) ? $_GET['action'] : '';
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Bodega</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>

<nav class="navbar">
    <a href="index.php" class="navbar-brand">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 21.88a2 2 0 0 0 2 0l8-4.58a2 2 0 0 0 1-1.73V5.26a2 2 0 0 0-1-1.73l-8-4.58a2 2 0 0 0-2 0l-8 4.58a1.98 1.98 0 0 0-1 1.73v10.31a2 2 0 0 0 1 1.73Z"/><path d="M2 5.7h20"/><path d="M10 12.1 2.2 7.7"/><path d="m14 12.1 7.8-4.4"/><path d="M12 22V12"/></svg>
        BodegaMVC
    </a>

    <ul class="navbar-nav">
        <?php if (isset($_SESSION['user_id'])): ?>
            <?php if ($_SESSION['user_tipo'] == 'admin'): ?>
                <li>
                    <a href="index.php?controller=Admin&action=usuarios"
                       class="nav-link <?= ($ctrl == 'Admin' && $accion == 'usuarios') ? 'active' : '' ?>">
                        Usuarios
                    </a>
                </li>
                <li>
                    <a href="index.php?controller=Admin&action=bodega"
                       class="nav-link <?= ($ctrl == 'Admin' && in_array($accion, ['bodega','registrarProducto','cajas'])) ? 'active' : '' ?>">
                        Bodega
                    </a>
                </li>
            <?php else: ?>
                <li>
                    <a href="index.php?controller=User&action=comprar"
                       class="nav-link <?= ($ctrl == 'User' && $accion == 'comprar') ? 'active' : '' ?>">
                        Comprar
                    </a>
                </li>
                <li>
                    <a href="index.php?controller=User&action=perfil"
                       class="nav-link <?= ($ctrl == 'User' && $accion == 'perfil') ? 'active' : '' ?>">
                        Mi Perfil
                    </a>
                </li>
            <?php endif; ?>

            <li class="nav-user-info">
                <span class="user-badge"><?= htmlspecialchars($_SESSION['user_nombre']) ?> (<?= $_SESSION['user_tipo'] ?>)</span>
                <?php if ($_SESSION['user_tipo'] == 'user'): ?>
                    <span class="text-success font-bold" style="font-size:0.88rem;">
                        $<?= number_format($_SESSION['user_dinero'], 2) ?>
                    </span>
                <?php endif; ?>
                <a href="index.php?controller=Auth&action=logout" class="btn btn-secondary btn-sm">Salir</a>
            </li>
        <?php else: ?>
            <li>
                <a href="index.php?controller=Auth&action=login" class="nav-link active">Iniciar Sesión</a>
            </li>
        <?php endif; ?>
    </ul>
</nav>

<div class="container animate-fade-in">
