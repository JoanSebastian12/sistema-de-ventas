<?php
require_once __DIR__ . '/../layout/header.php';

// detecta si es edicion o creacion
$esEdicion  = isset($usuario) && !empty($usuario);
$titulo     = $esEdicion ? 'Editar Usuario' : 'Crear Usuario';
$urlAccion  = $esEdicion
    ? 'index.php?controller=Admin&action=editarUsuario&id=' . $usuario['id']
    : 'index.php?controller=Admin&action=crearUsuario';
?>

<div class="card animate-fade-in" style="max-width:620px; margin:0 auto;">
    <h2 class="card-title"><?= $titulo ?></h2>

    <?php if (!empty($error)): ?>
        <div class="alert alert-danger">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <?= htmlspecialchars($error) ?>
        </div>
    <?php endif; ?>

    <form action="<?= $urlAccion ?>" method="POST">
        <div class="form-group">
            <label for="nombre" class="form-label">Nombre</label>
            <input type="text" id="nombre" name="nombre" class="form-control"
                   placeholder="Ej: Juan Pérez"
                   value="<?= $esEdicion ? htmlspecialchars($usuario['nombre']) : (isset($_POST['nombre']) ? htmlspecialchars($_POST['nombre']) : '') ?>"
                   required>
        </div>

        <div class="form-group">
            <label for="correo" class="form-label">Correo</label>
            <input type="email" id="correo" name="correo" class="form-control"
                   placeholder="Ej: juan@correo.com"
                   value="<?= $esEdicion ? htmlspecialchars($usuario['correo']) : (isset($_POST['correo']) ? htmlspecialchars($_POST['correo']) : '') ?>"
                   required>
        </div>

        <div class="form-group">
            <label for="contrasena" class="form-label">Contraseña</label>
            <input type="password" id="contrasena" name="contrasena" class="form-control"
                   placeholder="<?= $esEdicion ? 'Dejar vacío para no cambiar' : 'Escribe una contraseña' ?>"
                   <?= $esEdicion ? '' : 'required' ?> autocomplete="new-password">
            <?php if ($esEdicion): ?>
                <small style="color:var(--texto2); display:block; margin-top:0.3rem;">Si no cambias la contraseña, déjalo vacío.</small>
            <?php endif; ?>
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:1.25rem;">
            <div class="form-group">
                <label for="edad" class="form-label">Edad</label>
                <input type="number" id="edad" name="edad" min="1" max="120" class="form-control"
                       placeholder="Ej: 25"
                       value="<?= $esEdicion ? htmlspecialchars($usuario['edad']) : (isset($_POST['edad']) ? htmlspecialchars($_POST['edad']) : '') ?>"
                       required>
            </div>
            <div class="form-group">
                <label for="tipo" class="form-label">Tipo</label>
                <select id="tipo" name="tipo" class="form-control" required>
                    <?php $tipoSel = $esEdicion ? $usuario['tipo'] : (isset($_POST['tipo']) ? $_POST['tipo'] : 'user'); ?>
                    <option value="user"  <?= $tipoSel == 'user'  ? 'selected' : '' ?>>Usuario</option>
                    <option value="admin" <?= $tipoSel == 'admin' ? 'selected' : '' ?>>Administrador</option>
                </select>
            </div>
        </div>

        <div class="form-group">
            <label for="dinero" class="form-label">Saldo ($)</label>
            <input type="number" id="dinero" name="dinero" min="0" step="0.01" class="form-control"
                   placeholder="Ej: 500.00"
                   value="<?= $esEdicion ? htmlspecialchars($usuario['dinero']) : (isset($_POST['dinero']) ? htmlspecialchars($_POST['dinero']) : '0.00') ?>"
                   required>
        </div>

        <div class="btn-group mt-4" style="justify-content:flex-end;">
            <a href="index.php?controller=Admin&action=usuarios" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary"><?= $titulo ?></button>
        </div>
    </form>
</div>

<?php require_once __DIR__ . '/../layout/footer.php'; ?>
