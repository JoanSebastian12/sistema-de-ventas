<?php
require_once __DIR__ . '/../layout/header.php';

$ok  = isset($_GET['success']) ? $_GET['success'] : '';
$err = isset($_GET['error'])   ? $_GET['error']   : '';
?>

<div class="card animate-fade-in">
    <div class="actions-bar">
        <h2 class="card-title" style="border-bottom:none; margin-bottom:0; padding-bottom:0;">Usuarios del Sistema</h2>
        <a href="index.php?controller=Admin&action=crearUsuario" class="btn btn-primary">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            Nuevo Usuario
        </a>
    </div>

    <?php if ($ok): ?>
        <div class="alert alert-success">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            <?= htmlspecialchars($ok) ?>
        </div>
    <?php endif; ?>

    <?php if ($err): ?>
        <div class="alert alert-danger">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <?= htmlspecialchars($err) ?>
        </div>
    <?php endif; ?>

    <div class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th>Nombre</th>
                    <th>Correo</th>
                    <th>Edad</th>
                    <th>Tipo</th>
                    <th>Saldo</th>
                    <th style="text-align:center;">Acciones</th>
                </tr>
            </thead>
            <tbody>
                <?php if (empty($usuarios)): ?>
                    <tr>
                        <td colspan="6" class="text-center" style="padding:2rem; color:var(--texto2);">No hay usuarios todavía.</td>
                    </tr>
                <?php else: ?>
                    <?php foreach ($usuarios as $u): ?>
                        <tr>
                            <td class="font-bold"><?= htmlspecialchars($u['nombre']) ?></td>
                            <td><?= htmlspecialchars($u['correo']) ?></td>
                            <td><?= $u['edad'] ?> años</td>
                            <td>
                                <?php if ($u['tipo'] == 'admin'): ?>
                                    <span class="badge-role badge-role-admin">Admin</span>
                                <?php else: ?>
                                    <span class="badge-role badge-role-user">Usuario</span>
                                <?php endif; ?>
                            </td>
                            <td class="text-success font-bold">$<?= number_format($u['dinero'], 2) ?></td>
                            <td>
                                <div class="btn-group" style="justify-content:center;">
                                    <a href="index.php?controller=Admin&action=editarUsuario&id=<?= $u['id'] ?>" class="btn btn-secondary btn-sm">Editar</a>
                                    <?php if ($_SESSION['user_id'] != $u['id']): ?>
                                        <a href="index.php?controller=Admin&action=eliminarUsuario&id=<?= $u['id'] ?>"
                                           class="btn btn-danger btn-sm"
                                           onclick="return confirm('¿Eliminar a <?= htmlspecialchars($u['nombre']) ?>?');">
                                            Eliminar
                                        </a>
                                    <?php else: ?>
                                        <button class="btn btn-secondary btn-sm" disabled style="opacity:0.4;" title="No puedes eliminarte">Eliminar</button>
                                    <?php endif; ?>
                                </div>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                <?php endif; ?>
            </tbody>
        </table>
    </div>
</div>

<?php require_once __DIR__ . '/../layout/footer.php'; ?>
