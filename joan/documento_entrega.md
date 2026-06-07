# Documento de Entrega - Sistema de Gestión de Ventas (SGV)

## 1. Entregables

1. **Código de la aplicación**
   - Archivos Python principales:
     - `main.py`
     - `database.py`
     - `auth.py`
     - `cliente_service.py`
     - `producto_service.py`
     - `inventario_service.py`
     - `venta_service.py`
     - `caja_service.py`
     - `reporte_service.py`
   - Carpeta de interfaz gráfica:
     - `ui/login.py`
     - `ui/dashboard.py`
     - `ui/productos.py`
     - `ui/clientes.py`
     - `ui/ventas.py`
     - `ui/inventario.py`
     - `ui/caja.py`
     - `ui/reportes.py`
     - `ui/usuarios.py`

2. **Base de datos**
   - Archivo SQLite: `sistema_ventas.db`
   - Se crea automáticamente al iniciar `main.py`.
   - Contiene las tablas:
     - `usuarios`
     - `clientes`
     - `productos`
     - `movimientos_inventario`
     - `ventas`
     - `detalles_venta`
     - `cajas`
     - `auditoria`

3. **Pantallas conectadas con la base de datos**
   - Sí, las pantallas están conectadas:
     - `main.py` arranca la app y muestra login.
     - `ui/login.py` usa `auth.py` para autenticar usuarios.
     - `ui/dashboard.py` navega a los módulos.
     - Cada pantalla de `ui/` llama a su servicio correspondiente.
     - Los servicios usan `database.py` para leer/escribir en SQLite.
   - Ejemplos de conexión:
     - `ui/productos.py` → `ProductoService` → `database.py`
     - `ui/clientes.py` → `ClienteService` → `database.py`
     - `ui/ventas.py` → `VentaService` → `InventarioService` → `database.py`
     - `ui/caja.py` → `CajaService` → `database.py`
     - `ui/reportes.py` → `ReporteService` → `database.py`

## 2. Cómo funciona la aplicación

### 2.1 Flujo de inicio

- `main.py` inicializa la base de datos
- Crea usuario `admin` si no está presente
- Muestra el formulario de login

### 2.2 Login y roles

- El login está en `ui/login.py`
- Verifica credenciales con `AuthService.login()`
- El usuario predeterminado es:
  - `usuario`: `admin`
  - `contraseña`: `admin123`
- Rol del usuario define qué pantallas aparecen en el menú.

### 2.3 Navegación

- `ui/dashboard.py` es el centro del sistema.
- Desde ahí se accede a:
  - Gestión de usuarios
  - Gestión de productos
  - Gestión de clientes
  - Inventario
  - Punto de venta
  - Caja
  - Reportes

### 2.4 Conexión con la base de datos

- Cada servicio usa `get_connection()` de `database.py`
- Las operaciones CRUD y reportes se ejecutan directamente en SQLite
- La estructura de capas es:
  - UI → Servicio → Database → SQLite

## 3. Explicación de los archivos clave

### `main.py`
- Inicia la interfaz de Tkinter
- Inicializa la base de datos
- Muestra `LoginUI`
- Controla la transición a `DashboardUI`

### `database.py`
- Crea todas las tablas necesarias
- Normaliza la base de datos en SQLite
- Administra conexiones y registros base

### `auth.py`
- Gestiona login
- Hashea contraseñas con SHA256
- Crea y actualiza usuarios
- Registra auditoría de accesos

### `cliente_service.py`
- CRUD de clientes
- Búsqueda por nombre o documento
- Historial de compras

### `producto_service.py`
- CRUD de productos
- Validaciones de precio y stock
- Control de stock mínimo

### `inventario_service.py`
- Registra movimientos de inventario
- Ajusta stock automáticamente
- Muestra productos con bajo stock

### `venta_service.py`
- Procesa ventas y genera facturas
- Calcula subtotal, IVA y total
- Actualiza inventario al vender
- Guarda detalles de venta

### `caja_service.py`
- Maneja apertura y cierre de caja
- Calcula diferencias entre monto final y ventas
- Registra historiales de caja

### `reporte_service.py`
- Genera reportes de ventas e inventario
- Permite análisis de ganancias y productos vendidos

## 4. Cómo ejecutar el sistema

1. Abrir carpeta del proyecto
2. Ejecutar en terminal:
   ```bash
   python main.py
   ```
3. Iniciar sesión con:
   - Usuario: `admin`
   - Contraseña: `admin123`

## 5. Qué entregar al profesor

1. Carpeta del proyecto con todos los archivos `.py`.
2. Archivo `sistema_ventas.db`.
3. Documentación en PDF con:
   - Capturas de pantalla de la aplicación en ejecución
   - Explicación de la arquitectura
   - Explicación de cada módulo principal
   - Ejemplo de flujo de venta
4. Si el profesor pide, incluir el `README.md` y el `documento_entrega.md`.

## 6. Capturas de pantalla

> Agrega capturas reales de tu ejecución dentro del PDF.

- Pantalla de login
- Menú principal
- Gestión de productos
- Ventas/Carrito
- Cierre de caja
- Reportes

## 7. Nota final

Tu entrega ya incluye el código correcto, la base de datos y las pantallas enlazadas. Solo falta generar el PDF final con las capturas y las explicaciones, que puedo ayudarte a montar en texto y luego convertir si quieres.
