<?php
require_once __DIR__ . '/layout/header.php';
?>

<div class="login-wrapper">
    <div class="card card-login">
        <div class="login-header">
            <h1>Iniciar Sesión</h1>
            <p>Ingresa tus datos para continuar</p>
        </div>

        <?php if (!empty($error)): ?>
            <div class="alert alert-danger">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                <?= htmlspecialchars($error) ?>
            </div>
        <?php endif; ?>

        <form action="index.php?controller=Auth&action=login" method="POST">
            <div class="form-group">
                <label for="usuario" class="form-label">Usuario o correo</label>
                <input type="text" id="usuario" name="usuario" class="form-control"
                       placeholder="admin o tu correo" required autocomplete="username">
            </div>

            <div class="form-group">
                <label for="contrasena" class="form-label">Contraseña</label>
                <input type="password" id="contrasena" name="contrasena" class="form-control"
                       placeholder="••••••••" required autocomplete="current-password">
            </div>

            <button type="submit" class="btn btn-primary btn-block mt-4">Entrar</button>
        </form>

        <div class="text-center mt-4" style="font-size:0.83rem; color:var(--texto2);">
            <p>Admin por defecto: <strong>admin</strong> / <strong>admin</strong></p>
        </div>
    </div>
</div>

<?php require_once __DIR__ . '/layout/footer.php'; ?>
