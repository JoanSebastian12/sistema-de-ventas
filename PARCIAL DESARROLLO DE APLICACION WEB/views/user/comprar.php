<?php
require_once __DIR__ . '/../layout/header.php';
?>

<div class="animate-fade-in">
    <h2 class="mb-4" style="font-weight:800; font-size:2rem; background:linear-gradient(135deg,#a5b4fc,#6366f1); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        Comprar
    </h2>

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

    <div class="grid-compra">
        <!-- lista de productos -->
        <div class="card" style="margin-bottom:0;">
            <h3 class="mb-4" style="font-size:1.1rem; font-weight:600; color:var(--texto2); border-bottom:1px solid var(--borde); padding-bottom:0.5rem;">
                Productos disponibles
            </h3>

            <div class="list-group">
                <?php if (empty($productos)): ?>
                    <div style="color:var(--texto2); padding:1.5rem; text-align:center;">
                        No hay productos en este momento.
                    </div>
                <?php else: ?>
                    <?php foreach ($productos as $p): ?>
                        <a href="index.php?controller=User&action=comprar&id_producto=<?= $p['id'] ?>"
                           class="list-group-item <?= ($productoSeleccionado && $productoSeleccionado['id'] == $p['id']) ? 'active' : '' ?>">
                            <span><?= htmlspecialchars($p['nombre']) ?></span>
                            <span class="font-bold" style="color:var(--exito);">$<?= number_format($p['precio'], 2) ?></span>
                        </a>
                    <?php endforeach; ?>
                <?php endif; ?>
            </div>
        </div>

        <!-- detalle y formulario de compra -->
        <div class="card" style="margin-bottom:0;">
            <?php if ($productoSeleccionado): ?>
                <h3 class="mb-4" style="font-size:1.1rem; font-weight:600; color:var(--texto2); border-bottom:1px solid var(--borde); padding-bottom:0.5rem;">
                    Detalle del producto
                </h3>

                <div class="detail-grid">
                    <span class="detail-label">Nombre:</span>
                    <span class="detail-value" style="color:#a5b4fc;"><?= htmlspecialchars($productoSeleccionado['nombre']) ?></span>

                    <span class="detail-label">Código:</span>
                    <span class="detail-value"><?= htmlspecialchars($productoSeleccionado['codigo']) ?></span>

                    <span class="detail-label">Precio/Caja:</span>
                    <span class="detail-value text-success">$<?= number_format($productoSeleccionado['precio'], 2) ?></span>

                    <span class="detail-label">Stock:</span>
                    <span class="detail-value">
                        <?php if ($productoSeleccionado['cajas'] == 0): ?>
                            <span class="text-danger font-bold">Agotado</span>
                        <?php else: ?>
                            <span class="text-success font-bold"><?= $productoSeleccionado['cajas'] ?> cajas</span>
                        <?php endif; ?>
                    </span>

                    <span class="detail-label">Edad mínima:</span>
                    <span class="detail-value">
                        <?php if ($productoSeleccionado['edad_restriccion'] == 0): ?>
                            <span class="text-success">Sin restricción</span>
                        <?php else: ?>
                            <span class="text-warning font-bold">+<?= $productoSeleccionado['edad_restriccion'] ?> años</span>
                        <?php endif; ?>
                    </span>
                </div>

                <?php if ($productoSeleccionado['cajas'] > 0): ?>
                    <form action="index.php?controller=User&action=comprar&id_producto=<?= $productoSeleccionado['id'] ?>" method="POST">
                        <input type="hidden" name="id_producto" value="<?= $productoSeleccionado['id'] ?>">

                        <div class="form-group">
                            <label for="cajas_comprar" class="form-label">Cantidad de cajas</label>
                            <input type="number" id="cajas_comprar" name="cajas_comprar"
                                   min="1" max="<?= $productoSeleccionado['cajas'] ?>"
                                   class="form-control" placeholder="Ej: 2" required>
                        </div>

                        <!-- resumen de la compra -->
                        <div style="background:rgba(99,102,241,0.1); border:1px dashed var(--primario); padding:1rem; border-radius:8px; margin-bottom:1.25rem;">
                            <p style="font-size:0.88rem; color:var(--texto2); display:flex; justify-content:space-between; margin-bottom:0.2rem;">
                                Precio unitario: <span>$<?= number_format($productoSeleccionado['precio'], 2) ?></span>
                            </p>
                            <p style="font-size:0.95rem; font-weight:600; display:flex; justify-content:space-between;">
                                Total: <span id="total" class="text-success">$0.00</span>
                            </p>
                        </div>

                        <button type="submit" class="btn btn-primary btn-block">Comprar</button>
                    </form>

                    <script>
                        // calcula el total en tiempo real
                        var inputCajas = document.getElementById('cajas_comprar');
                        var spanTotal  = document.getElementById('total');
                        var precio     = <?= floatval($productoSeleccionado['precio']) ?>;

                        inputCajas.addEventListener('input', function() {
                            var cant  = parseInt(this.value) || 0;
                            var total = cant * precio;
                            spanTotal.textContent = '$' + total.toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2});
                        });
                    </script>
                <?php else: ?>
                    <div class="alert alert-danger" style="margin-top:1rem;">
                        Este producto está agotado.
                    </div>
                <?php endif; ?>

            <?php else: ?>
                <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; min-height:220px; text-align:center; color:var(--texto2);">
                    <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom:1rem;"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                    <p>Selecciona un producto de la izquierda.</p>
                </div>
            <?php endif; ?>
        </div>
    </div>
</div>

<?php require_once __DIR__ . '/../layout/footer.php'; ?>
