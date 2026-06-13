<?php
require_once __DIR__ . '/../layout/header.php';
?>

<div class="card animate-fade-in" style="max-width:580px; margin:0 auto;">
    <h2 class="card-title">Ingresar / Sacar Cajas</h2>

    <?php if (!empty($error)): ?>
        <div class="alert alert-danger">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <?= htmlspecialchars($error) ?>
        </div>
    <?php endif; ?>

    <div class="detail-grid">
        <span class="detail-label">Producto:</span>
        <span class="detail-value"><?= htmlspecialchars($producto['nombre']) ?></span>

        <span class="detail-label">Código:</span>
        <span class="detail-value" style="color:#a5b4fc;"><?= htmlspecialchars($producto['codigo']) ?></span>

        <span class="detail-label">Cajas actuales:</span>
        <span class="detail-value">
            <?php if ($producto['cajas'] == 0): ?>
                <span class="text-danger font-bold">Sin stock</span>
            <?php else: ?>
                <span class="text-success font-bold"><?= $producto['cajas'] ?> cajas</span>
            <?php endif; ?>
        </span>

        <span class="detail-label">Precio/Caja:</span>
        <span class="detail-value">$<?= number_format($producto['precio'], 2) ?></span>
    </div>

    <form action="index.php?controller=Admin&action=cajas&id=<?= $producto['id'] ?>" method="POST">
        <div class="form-group">
            <label for="accion" class="form-label">Movimiento</label>
            <select id="accion" name="accion" class="form-control" required>
                <option value="ingresar" <?= (isset($_POST['accion']) && $_POST['accion'] == 'ingresar') ? 'selected' : '' ?>>Ingresar cajas (+)</option>
                <option value="sacar"    <?= (isset($_POST['accion']) && $_POST['accion'] == 'sacar')    ? 'selected' : '' ?>>Sacar cajas (-)</option>
            </select>
        </div>

        <div class="form-group">
            <label for="cantidad" class="form-label">Cantidad</label>
            <input type="number" id="cantidad" name="cantidad" min="1" class="form-control"
                   placeholder="Ej: 10"
                   value="<?= isset($_POST['cantidad']) ? intval($_POST['cantidad']) : '' ?>" required>
            <small style="color:var(--texto2); display:block; margin-top:0.3rem;">
                No se puede sacar más de las cajas disponibles.
            </small>
        </div>

        <div class="btn-group mt-4" style="justify-content:flex-end;">
            <a href="index.php?controller=Admin&action=bodega" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Confirmar</button>
        </div>
    </form>
</div>

<?php require_once __DIR__ . '/../layout/footer.php'; ?>
