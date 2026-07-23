-- ======================================================
-- BASE DE DATOS
-- TAQUERÍA LOS DOS GARCIAS
-- Desde 1994
-- Servicio Exclusivo a Domicilio
-- ======================================================

DROP DATABASE IF EXISTS los_dos_garcias;

CREATE DATABASE los_dos_garcias;

USE los_dos_garcias;

-- ======================================================
-- TABLA USUARIOS
-- ======================================================

CREATE TABLE usuarios(

id_usuario INT AUTO_INCREMENT PRIMARY KEY,

nombre VARCHAR(100) NOT NULL,

correo VARCHAR(100) UNIQUE NOT NULL,

password VARCHAR(255) NOT NULL,

telefono VARCHAR(15) NOT NULL,

direccion VARCHAR(250) NOT NULL,

rol ENUM('cliente','administrador') DEFAULT 'cliente'

);

-- ======================================================
-- TABLA CATEGORIAS
-- ======================================================

CREATE TABLE categorias(

id_categoria INT AUTO_INCREMENT PRIMARY KEY,

nombre VARCHAR(50) NOT NULL

);

-- ======================================================
-- TABLA PRODUCTOS
-- ======================================================

CREATE TABLE productos(

id_producto INT AUTO_INCREMENT PRIMARY KEY,

id_categoria INT,

nombre VARCHAR(100) NOT NULL,

descripcion TEXT,

precio DECIMAL(10,2),

imagen VARCHAR(200),

disponible BOOLEAN DEFAULT TRUE,

FOREIGN KEY(id_categoria)

REFERENCES categorias(id_categoria)

);

-- ======================================================
-- TABLA MÉTODOS DE PAGO
-- ======================================================

CREATE TABLE metodos_pago(

id_pago INT AUTO_INCREMENT PRIMARY KEY,

metodo VARCHAR(50)

);

-- ======================================================
-- TABLA PEDIDOS
-- ======================================================

CREATE TABLE pedidos(

id_pedido INT AUTO_INCREMENT PRIMARY KEY,

id_usuario INT,

id_pago INT,

fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

direccion_entrega VARCHAR(250),

total DECIMAL(10,2),

estado ENUM(

'Pedido recibido',

'En preparación',

'En camino',

'Entregado'

) DEFAULT 'Pedido recibido',

FOREIGN KEY(id_usuario)

REFERENCES usuarios(id_usuario),

FOREIGN KEY(id_pago)

REFERENCES metodos_pago(id_pago)

);

-- ======================================================
-- TABLA DETALLE PEDIDO
-- ======================================================

CREATE TABLE detalle_pedido(

id_detalle INT AUTO_INCREMENT PRIMARY KEY,

id_pedido INT,

id_producto INT,

cantidad INT,

precio_unitario DECIMAL(10,2),

subtotal DECIMAL(10,2),

FOREIGN KEY(id_pedido)

REFERENCES pedidos(id_pedido),

FOREIGN KEY(id_producto)

REFERENCES productos(id_producto)

);

-- ======================================================
-- TABLA PROMOCIONES
-- ======================================================

CREATE TABLE promociones(

id_promocion INT AUTO_INCREMENT PRIMARY KEY,

nombre VARCHAR(100),

descripcion TEXT,

condicion VARCHAR(100),

beneficio VARCHAR(100),

activa BOOLEAN DEFAULT TRUE

);

-- ======================================================
-- CATEGORÍAS
-- ======================================================

INSERT INTO categorias(nombre)

VALUES

('Tacos'),

('Especialidad'),

('Refrescos');

-- ======================================================
-- MÉTODOS DE PAGO
-- ======================================================

INSERT INTO metodos_pago(metodo)

VALUES

('Efectivo'),

('Transferencia'),

('Tarjeta');

-- ======================================================
-- ADMINISTRADOR
-- ======================================================

INSERT INTO usuarios

(nombre,correo,password,telefono,direccion,rol)

VALUES

(

'Administrador',

'emiliogarcianmms@gmail.com',

'123456',

'7474275925',

'LOS DOS GARCIAS',

'administrador'

);

-- ======================================================
-- PRODUCTOS
-- ======================================================

INSERT INTO productos

(id_categoria,nombre,descripcion,precio,imagen)

VALUES

(1,'Taco de Suadero','Taco tradicional.',27,'suadero.jpg'),

(1,'Taco de Longaniza','Longaniza.',27,'longaniza.jpg'),

(1,'Taco Campechano','Suadero y bistec.',27,'campechano.jpg'),

(1,'Taco de Bistec','Bistec.',30,'bistec.jpg'),

(1,'Taco de Tripa','Tripa dorada.',30,'tripa.jpg'),

(1,'Taco de Chuleta','Chuleta.',30,'chuleta.jpg'),

(1,'Taco de Pollo','Pollo.',30,'pollo.jpg'),

(2,'LA GARCITORTA','Especialidad de la casa.',40,'garcitorta.jpg'),

(3,'Coca-Cola','600 ml',30,'coca.jpg'),

(3,'Sprite','600 ml',30,'sprite.jpg'),

(3,'Ameyal','600 ml',30,'ameyal.jpg'),

(3,'Jugos del Valle','600 ml',30,'delvalle.jpg'),

(3,'Manzanita Sol','600 ml',30,'manzanita.jpg'),

(3,'Pepsi','600 ml',30,'pepsi.jpg'),

(3,'Fanta','600 ml',30,'fanta.jpg'),

(3,'Topo Chico','600 ml',30,'topochico.jpg');

-- ======================================================
-- PROMOCIONES
-- ======================================================

INSERT INTO promociones

(nombre,descripcion,condicion,beneficio)

VALUES

(

'Refresco Gratis',

'Obtén un refresco de 600 ml.',

'Comprar 10 tacos o más',

'1 refresco gratis'

),

(

'Envío Gratis',

'Servicio a domicilio sin costo.',

'Comprar 25 tacos o más',

'Envío gratuito'

);

-- ======================================================
-- CONSULTAS CRUD
-- ======================================================

-- CREAR CLIENTE

INSERT INTO usuarios

(nombre,correo,password,telefono,direccion)

VALUES

(

'Juan Pérez',

'juan@gmail.com',

'12345',

'7221112233',

'Toluca, Estado de México'

);

------------------------------------------------------

-- LEER PRODUCTOS

SELECT * FROM productos;

------------------------------------------------------

-- LEER CLIENTES

SELECT * FROM usuarios;

------------------------------------------------------

-- VER PEDIDOS

SELECT

p.id_pedido,

u.nombre,

p.fecha,

p.total,

p.estado,

mp.metodo

FROM pedidos p

INNER JOIN usuarios u

ON p.id_usuario=u.id_usuario

INNER JOIN metodos_pago mp

ON p.id_pago=mp.id_pago;

------------------------------------------------------

-- ACTUALIZAR PRECIO

UPDATE productos

SET precio=30

WHERE id_producto=4;

------------------------------------------------------

-- CAMBIAR ESTADO

UPDATE pedidos

SET estado='En camino'

WHERE id_pedido=1;

------------------------------------------------------

-- ELIMINAR PRODUCTO

DELETE FROM productos

WHERE id_producto=16;

------------------------------------------------------

-- ELIMINAR CLIENTE

DELETE FROM usuarios

WHERE id_usuario=2;

USE los_dos_garcias;

ALTER TABLE pedidos
ADD COLUMN nombre_cliente VARCHAR(100),
ADD COLUMN telefono_cliente VARCHAR(15);

USE los_dos_garcias;

DESCRIBE pedidos;