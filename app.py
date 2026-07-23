# =====================================================
# PROYECTO: LOS DOS GARCIAS
# Sistema Web de Pedidos a Domicilio
# Desde 1994
# Flask + MySQL
# =====================================================


from flask import Flask, render_template, request, redirect, session

from flask_mysqldb import MySQL



# =====================================================
# CONFIGURACIÓN FLASK
# =====================================================


app = Flask(__name__)

app.secret_key = "los_dos_garcias_1994"



# =====================================================
# CONFIGURACIÓN MYSQL
# =====================================================
app.config['MYSQL_HOST'] = 'sql3.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql3833668'
app.config['MYSQL_PASSWORD'] = 'TSVzaYJsk1'
app.config['MYSQL_DB'] = 'los_dos_garcias'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# =====================================================
# PAGINA PRINCIPAL
# =====================================================


@app.route('/')

def inicio():

    return render_template('index.html')



# =====================================================
# MENU
# =====================================================


@app.route('/menu')

def menu():

    cursor = mysql.connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM productos
        WHERE disponible = TRUE
        """
    )


    productos = cursor.fetchall()


    cursor.close()


    return render_template(
        'menu.html',
        productos=productos
    )



# =====================================================
# AGREGAR AL CARRITO
# =====================================================


@app.route('/agregar_carrito', methods=['POST'])

def agregar_carrito():


    id_producto = request.form['id_producto']


    cursor = mysql.connection.cursor()


    cursor.execute(

        """
        SELECT *
        FROM productos
        WHERE id_producto=%s
        """,

        (id_producto,)

    )


    producto = cursor.fetchone()


    cursor.close()



    if not producto:

        return redirect('/menu')



    if 'carrito' not in session:

        session['carrito'] = []



    carrito = session['carrito']



    # CORREGIR DATOS ANTIGUOS DE SESION

    for item in carrito:


        if 'cantidad' not in item:

            item['cantidad'] = 1



        if 'subtotal' not in item:

            item['subtotal'] = (

                item['cantidad']

                *

                float(item['precio'])

            )



    encontrado = False



    for item in carrito:



        if item['id_producto'] == producto['id_producto']:


            item['cantidad'] += 1


            item['subtotal'] = (

                item['cantidad']

                *

                float(item['precio'])

            )


            encontrado = True



    if not encontrado:


        carrito.append({

            "id_producto": producto['id_producto'],

            "nombre": producto['nombre'],

            "precio": float(producto['precio']),

            "imagen": producto['imagen'],

            "cantidad": 1,

            "subtotal": float(producto['precio'])

        })



    session['carrito'] = carrito


    return redirect('/carrito')


# =====================================================
# AUMENTAR CANTIDAD
# =====================================================

@app.route('/sumar_carrito/<int:id_producto>')
def sumar_carrito(id_producto):

    carrito = session.get('carrito', [])

    for item in carrito:

        if item['id_producto'] == id_producto:

            item['cantidad'] += 1
            item['subtotal'] = item['cantidad'] * float(item['precio'])
            break

    session['carrito'] = carrito

    return redirect('/carrito')
# =====================================================
# DISMINUIR CANTIDAD
# =====================================================

@app.route('/restar_carrito/<int:id_producto>')
def restar_carrito(id_producto):

    carrito = session.get('carrito', [])

    for item in carrito:

        if item['id_producto'] == id_producto:

            item['cantidad'] -= 1

            if item['cantidad'] <= 0:
                carrito.remove(item)
            else:
                item['subtotal'] = item['cantidad'] * float(item['precio'])

            break

    session['carrito'] = carrito

    return redirect('/carrito')
# =====================================================
# MOSTRAR CARRITO
# =====================================================


@app.route('/carrito')

def carrito():


    carrito = session.get('carrito', [])


    total = 0


    cantidad_tacos = 0



    for producto in carrito:


        total += producto['subtotal']


        nombre = producto['nombre'].lower()



        if "taco" in nombre:

            cantidad_tacos += producto['cantidad']



    refresco_gratis = False

    envio_gratis = False



    if cantidad_tacos >= 10:

        refresco_gratis = True



    if cantidad_tacos >= 25:

        envio_gratis = True



    return render_template(

        'carrito.html',

        carrito=carrito,

        total=total,

        refresco_gratis=refresco_gratis,

        envio_gratis=envio_gratis

    )



# =====================================================
# ELIMINAR PRODUCTO
# =====================================================


@app.route('/eliminar_carrito/<int:id_producto>')

def eliminar_carrito(id_producto):


    carrito = session.get('carrito', [])



    carrito = [

        producto

        for producto in carrito

        if producto['id_producto'] != id_producto

    ]



    session['carrito'] = carrito



    return redirect('/carrito')


# =====================================================
# CONFIRMAR PEDIDO
# =====================================================


@app.route('/confirmar_pedido', methods=['GET','POST'])

def confirmar_pedido():


    carrito = session.get('carrito', [])


    if not carrito:

        return redirect('/menu')



    if request.method == 'POST':


        nombre = request.form['nombre']

        telefono = request.form['telefono']

        direccion = request.form['direccion']

        id_pago = request.form['id_pago']



        total = 0


        for producto in carrito:

            total += producto['subtotal']



        cursor = mysql.connection.cursor()



        # CREAR PEDIDO

        cursor.execute(

            """

            INSERT INTO pedidos

            (

            id_pago,

            nombre_cliente,

            telefono_cliente,

            direccion_entrega,

            total

            )

            VALUES

            (%s,%s,%s,%s,%s)

            """,

            (

            id_pago,

            nombre,

            telefono,

            direccion,

            total

            )

        )



        id_pedido = cursor.lastrowid



        # GUARDAR PRODUCTOS DEL PEDIDO


        for producto in carrito:


            cursor.execute(

                """

                INSERT INTO detalle_pedido

                (

                id_pedido,

                id_producto,

                cantidad,

                precio_unitario,

                subtotal

                )

                VALUES

                (%s,%s,%s,%s,%s)

                """,

                (

                id_pedido,

                producto['id_producto'],

                producto['cantidad'],

                producto['precio'],

                producto['subtotal']

                )

            )



        mysql.connection.commit()


        cursor.close()



        session.pop('carrito', None)



        return redirect(

            f'/pedido_exitoso/{id_pedido}'

        )



    return render_template(

        'confirmar_pedido.html',

        carrito=carrito

    )

# =====================================================
# PEDIDO EXITOSO
# =====================================================

@app.route('/pedido_exitoso/<int:id_pedido>')
def pedido_exitoso(id_pedido):

    return render_template(
        'pedido_exitoso.html',
        id_pedido=id_pedido
    )
# =====================================================
# PROMOCIONES
# =====================================================


@app.route('/promociones')

def promociones():


    cursor = mysql.connection.cursor()


    cursor.execute(

        """
        SELECT *
        FROM promociones
        WHERE activa = TRUE
        """

    )


    promociones = cursor.fetchall()


    cursor.close()


    return render_template(

        'promociones.html',

        promociones=promociones

    )



# =====================================================
# CONTACTO
# =====================================================


@app.route('/contacto')

def contacto():

    return render_template('contacto.html')



# =====================================================
# SEGUIMIENTO
# =====================================================


# =====================================================
# SEGUIMIENTO DE PEDIDO
# =====================================================

@app.route('/seguimiento', methods=['GET','POST'])
def seguimiento():


    pedido = None


    if request.method == 'POST':


        id_pedido = request.form['id_pedido']


        cursor = mysql.connection.cursor()


        cursor.execute(

            """
            SELECT

            p.id_pedido,

            p.nombre_cliente,

            p.telefono_cliente,

            p.direccion_entrega,

            p.fecha,

            p.total,

            p.estado,

            mp.metodo


            FROM pedidos p


            INNER JOIN metodos_pago mp

            ON p.id_pago = mp.id_pago


            WHERE p.id_pedido=%s

            """,

            (id_pedido,)

        )


        pedido = cursor.fetchone()


        cursor.close()



    return render_template(

        'seguimiento.html',

        pedido=pedido

    )
# ===================================================== 
# # LOGIN #
#  =====================================================

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        correo = request.form['correo']

        password = request.form['password']


        cursor = mysql.connection.cursor()


        cursor.execute(
            """
            SELECT *
            FROM usuarios
            WHERE correo=%s
            AND password=%s
            """,
            (correo,password)
        )


        usuario = cursor.fetchone()


        cursor.close()


        if usuario:

            session['id_usuario'] = usuario['id_usuario']

            session['usuario'] = usuario['nombre']

            session['rol'] = usuario['rol']


            if usuario['rol'] == "administrador":

                return redirect('/admin/pedidos')


            else:

                return redirect('/')


        return "Usuario o contraseña incorrectos"


    return render_template('login.html')

# =====================================================
# REGISTRO
# =====================================================


@app.route('/registro', methods=['GET','POST'])

def registro():


    if request.method == 'POST':


        datos = (

            request.form['nombre'],

            request.form['correo'],

            request.form['password'],

            request.form['telefono'],

            request.form['direccion']

        )



        cursor = mysql.connection.cursor()



        cursor.execute(

            """

            INSERT INTO usuarios

            (nombre,correo,password,telefono,direccion)

            VALUES

            (%s,%s,%s,%s,%s)

            """,

            datos

        )



        mysql.connection.commit()


        cursor.close()


        return redirect('/login')



    return render_template('registro.html')



# =====================================================
# ADMIN
# =====================================================


@app.route('/admin')

def admin():


    if session.get('rol') == "administrador":


        return render_template('admin.html')


    return redirect('/login')


# =====================================================
# ADMIN PEDIDOS
# =====================================================

@app.route('/admin/pedidos')
def admin_pedidos():

    if session.get('rol') != "administrador":

        return redirect('/login')


    cursor = mysql.connection.cursor()


    cursor.execute(
        """
        SELECT

        p.id_pedido,

        p.nombre_cliente,

        p.telefono_cliente,

        p.direccion_entrega,

        p.fecha,

        p.total,

        p.estado,

        mp.metodo


        FROM pedidos p


        INNER JOIN metodos_pago mp

        ON p.id_pago = mp.id_pago


        ORDER BY p.fecha DESC

        """
    )


    pedidos = cursor.fetchall()


    cursor.close()


    return render_template(
        'admin_pedidos.html',
        pedidos=pedidos
    )
# =====================================================
# DETALLE DE PEDIDO ADMIN
# =====================================================

@app.route('/admin/pedido/<int:id_pedido>')
def detalle_pedido_admin(id_pedido):


    if session.get('rol') != "administrador":

        return redirect('/login')


    cursor = mysql.connection.cursor()


    cursor.execute(
        """
        SELECT

        p.id_pedido,

        p.nombre_cliente,

        p.telefono_cliente,

        p.direccion_entrega,

        p.fecha,

        p.total,

        p.estado,


        dp.cantidad,

        dp.precio_unitario,

        dp.subtotal,


        pr.nombre,

        pr.imagen


        FROM pedidos p


        INNER JOIN detalle_pedido dp

        ON p.id_pedido = dp.id_pedido


        INNER JOIN productos pr

        ON dp.id_producto = pr.id_producto


        WHERE p.id_pedido=%s

        """,
        (id_pedido,)
    )


    detalle = cursor.fetchall()


    cursor.close()



    return render_template(

        'detalle_pedido_admin.html',

        detalle=detalle

    )
# =====================================================
# ACTUALIZAR ESTADO PEDIDO
# =====================================================

@app.route('/admin/actualizar_estado/<int:id_pedido>', methods=['POST'])
def actualizar_estado(id_pedido):


    if session.get('rol') != "administrador":

        return redirect('/login')


    estado = request.form['estado']


    cursor = mysql.connection.cursor()


    cursor.execute(
        """
        UPDATE pedidos

        SET estado=%s

        WHERE id_pedido=%s
        """,
        (
        estado,
        id_pedido
        )
    )


    mysql.connection.commit()


    cursor.close()


    return redirect('/admin/pedidos')

# =====================================================
# ELIMINAR PEDIDO ADMIN
# =====================================================

@app.route('/admin/eliminar_pedido/<int:id_pedido>', methods=['POST'])
def eliminar_pedido(id_pedido):


    if session.get('rol') != "administrador":

        return redirect('/login')


    cursor = mysql.connection.cursor()



    # ELIMINAR PRODUCTOS DEL PEDIDO

    cursor.execute(
        """
        DELETE FROM detalle_pedido
        WHERE id_pedido=%s
        """,
        (id_pedido,)
    )



    # ELIMINAR PEDIDO

    cursor.execute(
        """
        DELETE FROM pedidos
        WHERE id_pedido=%s
        """,
        (id_pedido,)
    )



    mysql.connection.commit()


    cursor.close()


    return redirect('/admin/pedidos')
# =====================================================
# LOGOUT
# =====================================================


@app.route('/logout')

def logout():

    session.clear()

    return redirect('/')



# =====================================================
# ERROR 404
# =====================================================


@app.errorhandler(404)

def pagina_no_encontrada(error):

    return render_template('error404.html')



# =====================================================
# EJECUTAR
# =====================================================
# =====================================================
# EJECUTAR
# =====================================================


if __name__ == '__main__':

    app.run(
        host="0.0.0.0",
        port=5000
    )
