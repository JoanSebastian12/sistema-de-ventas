<?php
require_once __DIR__ . '/../layout/header.php';
?>

<div class="card animate-fade-in" style="max-width:560px; margin:0 auto;">
    <h2 class="card-title">Mi Perfil</h2>

    <?php if (!empty($success)): ?>
        <div class="alert alert-success">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            <?= htmlspecialchars($success) ?>
        </div>
    <?php endif; ?>

    <?php if (!empty($error)): ?>
        <div class="alert alert-danger">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <?= htmlspecialchars($error) ?>
        </div>
    <?php endif; ?>

    <div class="detail-grid mb-4">
        <span class="detail-label">Correo:</span>
        <span class="detail-value"><?= htmlspecialchars($usuario['correo']) ?></span>

        <span class="detail-label">Edad:</span>
        <span class="detail-value"><?= $usuario['edad'] ?> años</span>

        <span class="detail-label">Tipo:</span>
        <span class="detail-value" style="text-transform:capitalize;"><?= $usuario['tipo'] ?></span>

        <span class="detail-label">Saldo:</span>
        <span class="detail-value text-success font-bold">$<?= number_format($usuario['dinero'], 2) ?></span>
    </div>

    <form action="index.php?controller=User&action=perfil" method="POST">
        <div class="form-group">
            <label for="nombre" class="form-label">Nombre</label>
            <input type="text" id="nombre" name="nombre" class="form-control"
                   value="<?= htmlspecialchars($usuario['nombre']) ?>" required>
        </div>

        <div class="form-group">
            <label for="contrasena" class="form-label">Nueva contraseña</label>
            <input type="password" id="contrasena" name="contrasena" class="form-control"
                   placeholder="Dejar vacío para no cambiar" autocomplete="new-password">
            <small style="color:var(--texto2); display:block; margin-top:0.3rem;">
                Si no quieres cambiar la contraseña, déjalo vacío.
            </small>
        </div>

        <button type="submit" class="btn btn-primary btn-block mt-4">Guardar cambios</button>
    </form>
</div>

<?php require_once __DIR__ . '/../layout/footer.php'; ?>
