# Sistema de Bodega MVC — Parcial Desarrollo de Aplicaciones Web

Básicamente lo que hice acá fue construir una aplicación web con PHP puro usando el patrón de arquitectura **MVC (Modelo - Vista - Controlador)**, que permite separar la lógica del negocio de la presentación. El sistema simula la gestión de una bodega con dos tipos de usuario: administrador y usuario regular.

---

## ¿De qué va el proyecto?

La aplicación permite a un administrador gestionar el inventario de productos y los usuarios del sistema. Por su parte, los usuarios registrados pueden consultar el catálogo y realizar compras descontando el saldo de su cuenta. Todo esto se maneja con sesiones PHP, una base de datos MySQL y acceso controlado según el rol.

---

## Tecnologías usadas

| Tecnología | Uso |
|---|---|
| PHP 8+ | Lógica del servidor y controladores |
| MySQL | Almacenamiento de datos |
| PDO | Conexión segura a la base de datos |
| HTML + CSS | Interfaz de usuario |
| Google Fonts (Inter) | Tipografía |

> Sin frameworks externos, sin librerías de terceros.



## Estructura del proyecto

El proyecto sigue el patrón MVC de forma manual, sin ningún framework:

```
/
├── index.php               ← Punto de entrada, enruta al controlador correspondiente
├── conexion.php            ← Clase de conexión a la BD con PDO (singleton)
├── db.sql                  ← Script para crear la base de datos y tablas
│
├── controllers/
│   ├── AuthController.php  ← Login y logout
│   ├── AdminController.php ← CRUD de usuarios e inventario
│   └── UserController.php  ← Compras y perfil del usuario
│
├── models/
│   ├── Usuario.php         ← Operaciones sobre la tabla usuarios
│   └── Producto.php        ← Operaciones sobre la tabla productos
│
├── views/
│   ├── login.php
│   ├── layout/
│   │   ├── header.php      ← Navbar + apertura del HTML
│   │   └── footer.php      ← Cierre del HTML
│   ├── admin/
│   │   ├── usuarios_list.php
│   │   ├── usuario_form.php
│   │   ├── bodega_list.php
│   │   ├── bodega_cajas.php
│   │   └── producto_form.php
│   └── user/
│       ├── comprar.php
│       └── perfil.php
│
└── css/
    └── style.css           ← Estilos del sistema (dark mode, glassmorphism)
```

---

## ¿Cómo funciona el enrutamiento?

No hay un router fancy ni nada por el estilo. El `index.php` lee los parámetros `controller` y `action` de la URL y carga el controlador correspondiente. Por ejemplo:

```
index.php?controller=Admin&action=bodega
```

Eso carga `AdminController.php` y ejecuta el método `bodega()`. Simple y directo.

---

## Instalación y puesta en marcha

Antes de correr el proyecto necesitás tener instalado **XAMPP** (o cualquier servidor local con Apache + MySQL + PHP).

### Pasos:

**1. Clonar o copiar la carpeta**

Copiá toda la carpeta del proyecto dentro de `htdocs` de XAMPP:

```
C:\xampp\htdocs\bodega\
```

**2. Crear la base de datos**

Abrí **phpMyAdmin** desde `http://localhost/phpmyadmin`, luego:
- Clic en "Importar"
- Seleccioná el archivo `db.sql` que está en la raíz del proyecto
- Ejecutar

Eso crea la base de datos `parcial_web` con las tablas `usuarios` y `productos`, y además inserta el usuario administrador por defecto.

**3. Verificar la conexión**

Abrí `conexion.php` y confirmá que los datos coincidan con tu configuración local:

```php
$dsn = "mysql:host=localhost;dbname=parcial_web;charset=utf8mb4";
self::$pdo = new PDO($dsn, "root", "");
```

Si tu MySQL tiene contraseña, cambiá `""` por tu contraseña.

**4. Acceder al sistema**

Abrí el navegador y entrá a:

```
http://localhost/bodega/
```

---

## Credenciales por defecto

| Campo | Valor |
|---|---|
| Usuario | `admin` |
| Contraseña | `admin` |
| Tipo | Administrador |

> ⚠️ El usuario admin inicial guarda la contraseña en texto plano en la BD. Al crear nuevos usuarios desde el sistema, las contraseñas se guardan con `password_hash()`.

---

## Funcionalidades del sistema

### Panel Administrador
- **Gestión de usuarios:** crear, editar y eliminar usuarios. No es posible eliminarse a uno mismo.
- **Inventario de bodega:** registrar productos con código único, precio, stock inicial y edad mínima de compra.
- **Movimiento de cajas:** ingresar o retirar cajas del inventario de cualquier producto.

### Panel Usuario
- **Comprar:** seleccionar un producto del catálogo, indicar la cantidad de cajas y confirmar la compra. El sistema valida automáticamente edad mínima, stock disponible y saldo suficiente.
- **Mi perfil:** actualizar nombre y contraseña. El correo y los datos económicos no los puede modificar el propio usuario.

---

## Modelo de datos

### Tabla `usuarios`

| Campo | Tipo | Descripción |
|---|---|---|
| id | INT (PK) | Identificador único |
| nombre | VARCHAR(100) | Nombre de usuario |
| correo | VARCHAR(100) | Correo electrónico (único) |
| contrasena | VARCHAR(255) | Contraseña hasheada |
| edad | INT | Edad del usuario |
| tipo | ENUM('admin','user') | Rol en el sistema |
| dinero | DECIMAL(10,2) | Saldo disponible |

### Tabla `productos`

| Campo | Tipo | Descripción |
|---|---|---|
| id | INT (PK) | Identificador único |
| nombre | VARCHAR(100) | Nombre del producto |
| codigo | VARCHAR(50) | Código único del producto |
| cajas | INT | Cantidad en inventario |
| precio | DECIMAL(10,2) | Precio por caja |
| edad_restriccion | INT | Edad mínima para comprar (0 = sin restricción) |

---

## Seguridad implementada

- Las contraseñas se almacenan usando `password_hash()` con `PASSWORD_DEFAULT` (bcrypt).
- Todas las consultas SQL usan **sentencias preparadas con PDO** para evitar inyección SQL.
- El acceso a cada panel está protegido por verificación de sesión y tipo de usuario al inicio de cada controlador.
- Los datos de entrada se sanitizan con `htmlspecialchars()` antes de mostrarse en la vista.

---

## Autor

Proyecto desarrollado como evaluación parcial del curso de **Desarrollo de Aplicaciones Web**.
