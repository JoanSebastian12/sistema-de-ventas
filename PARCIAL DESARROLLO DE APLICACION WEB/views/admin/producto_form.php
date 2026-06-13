<?php
require_once __DIR__ . '/../layout/header.php';
?>

<div class="card animate-fade-in" style="max-width:580px; margin:0 auto;">
    <h2 class="card-title">Registrar Producto</h2>

    <?php if (!empty($error)): ?>
        <div class="alert alert-danger">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <?= htmlspecialchars($error) ?>
        </div>
    <?php endif; ?>

    <p style="color:var(--texto2); margin-bottom:1.25rem; font-size:0.9rem;">
        Registra el producto antes de poder mover cajas en el inventario.
    </p>

    <form action="index.php?controller=Admin&action=registrarProducto" method="POST">
        <div class="form-group">
            <label for="codigo" class="form-label">Código único</label>
            <input type="text" id="codigo" name="codigo" class="form-control"
                   placeholder="Ej: PROD-001"
                   value="<?= isset($_POST['codigo']) ? htmlspecialchars($_POST['codigo']) : '' ?>" required>
            <small style="color:var(--texto2); display:block; margin-top:0.3rem;">No puede repetirse entre productos.</small>
        </div>

        <div class="form-group">
            <label for="nombre" class="form-label">Nombre del producto</label>
            <input type="text" id="nombre" name="nombre" class="form-control"
                   placeholder="Ej: Cerveza Club Colombia"
                   value="<?= isset($_POST['nombre']) ? htmlspecialchars($_POST['nombre']) : '' ?>" required>
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:1.25rem;">
            <div class="form-group">
                <label for="cajas" class="form-label">Cajas iniciales</label>
                <input type="number" id="cajas" name="cajas" min="0" class="form-control"
                       value="<?= isset($_POST['cajas']) ? intval($_POST['cajas']) : 0 ?>" required>
            </div>
            <div class="form-group">
                <label for="precio" class="form-label">Precio por caja ($)</label>
                <input type="number" id="precio" name="precio" min="0.01" step="0.01" class="form-control"
                       placeholder="Ej: 45.90"
                       value="<?= isset($_POST['precio']) ? htmlspecialchars($_POST['precio']) : '' ?>" required>
            </div>
        </div>

        <div class="form-group">
            <label for="edad_restriccion" class="form-label">Edad mínima para comprar (0 = sin restricción)</label>
            <input type="number" id="edad_restriccion" name="edad_restriccion" min="0" class="form-control"
                   placeholder="Ej: 18"
                   value="<?= isset($_POST['edad_restriccion']) ? intval($_POST['edad_restriccion']) : 0 ?>" required>
        </div>

        <div class="btn-group mt-4" style="justify-content:flex-end;">
            <a href="index.php?controller=Admin&action=bodega" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Registrar</button>
        </div>
    </form>
</div>

<?php require_once __DIR__ . '/../layout/footer.php'; ?>
