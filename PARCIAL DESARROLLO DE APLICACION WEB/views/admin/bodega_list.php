<?php
require_once __DIR__ . '/../layout/header.php';

$ok  = isset($_GET['success']) ? $_GET['success'] : '';
$err = isset($_GET['error'])   ? $_GET['error']   : '';
?>

<div class="card animate-fade-in">
    <div class="actions-bar">
        <h2 class="card-title" style="border-bottom:none; margin-bottom:0; padding-bottom:0;">Inventario Bodega</h2>
        <a href="index.php?controller=Admin&action=registrarProducto" class="btn btn-primary">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            Registrar Producto
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
                    <th>Código</th>
                    <th>Nombre</th>
                    <th>Precio/Caja</th>
                    <th>Cajas</th>
                    <th>Edad mínima</th>
                    <th style="text-align:center;">Acciones</th>
                </tr>
            </thead>
            <tbody>
                <?php if (empty($productos)): ?>
                    <tr>
                        <td colspan="6" class="text-center" style="padding:2rem; color:var(--texto2);">No hay productos en bodega.</td>
                    </tr>
                <?php else: ?>
                    <?php foreach ($productos as $p): ?>
                        <tr>
                            <td class="font-bold" style="color:#a5b4fc;"><?= htmlspecialchars($p['codigo']) ?></td>
                            <td><?= htmlspecialchars($p['nombre']) ?></td>
                            <td class="font-bold">$<?= number_format($p['precio'], 2) ?></td>
                            <td>
                                <?php if ($p['cajas'] == 0): ?>
                                    <span class="text-danger font-bold">Sin stock</span>
                                <?php elseif ($p['cajas'] <= 5): ?>
                                    <span class="text-warning font-bold"><?= $p['cajas'] ?> (bajo stock)</span>
                                <?php else: ?>
                                    <span class="text-success font-bold"><?= $p['cajas'] ?></span>
                                <?php endif; ?>
                            </td>
                            <td>
                                <?php if ($p['edad_restriccion'] == 0): ?>
                                    <span style="color:var(--texto2);">Sin restricción</span>
                                <?php else: ?>
                                    <span class="text-warning font-bold">+<?= $p['edad_restriccion'] ?> años</span>
                                <?php endif; ?>
                            </td>
                            <td style="text-align:center;">
                                <a href="index.php?controller=Admin&action=cajas&id=<?= $p['id'] ?>" class="btn btn-primary btn-sm">
                                    Cajas
                                </a>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                <?php endif; ?>
            </tbody>
        </table>
    </div>
</div>

<?php require_once __DIR__ . '/../layout/footer.php'; ?>
