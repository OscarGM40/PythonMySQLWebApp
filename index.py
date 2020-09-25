# debe coincidir la version de python y el pylinter
from flask import Flask, render_template, request, redirect, url_for, flash
# importamos la clase MySQL del modulo flask_mysqldb
from flask_mysqldb import MySQL
#from flaskext.mysql import MySQL


# guardamos la instancia de la clase
app = Flask(__name__)

# Usando la instancia,damos valores a las constantes tipicas de configuracion de una BDD
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' #ojo en Linux tengo password puesta
app.config['MYSQL_DB'] = 'flaskcontacts'

# debemos crear una sesion,con decir el modo ya creamos una
app.secret_key = 'mysecretki'

# instanciamos la clase MySQL(flask_instance) con un objeto flask por argumento
mysql = MySQL(app)


# creamos una ruta para la Home
@app.route('/', methods=['GET'])
def Index():
    # esta funcion dirige al .html,asi que deberemos enviar alli una tabla virtual con la select
    # lo primero es obtener el cursor de nuevo
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    # esta vez debemos guardar los datos,usaremos el metodo fetchall que devuelve una hashtable
    data = cur.fetchall()
    # los imprimimos por cli para probar
    # print(data)
    # vemos que devuelve una tupla con tuplas anidadas,vamos a pasarla
    # por el metodo render_template al html
    # por defecto flask buscara en templates los .html
    return render_template('index.html', contacts=data)
    # ya tenemos la hashtable en la variable contacts en el index.html

# ruta para agregar contactos.Usaremos el objeto request del modulo flask,importandolo
# desde este objeto  podemos usar sus metodos y propiedades ,como la propiedad method


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        # print(fullname) comprobacion por la cli

        # obtenemos un cursor virtual para posicionarnos
        cur = mysql.connection.cursor()
        # ya podemos llamar al metodo execute a traves del cursor
        # este metodo solo la escribe la consulta,no la ejecuta
        cur.execute('INSERT INTO contacts (fullname,phone,email) VALUES (%s,%s,%s)',
                    (fullname, phone, email))
        # para ejecutarlo hay que commitear con la function commit()
        mysql.connection.commit()

        # vamos a mandar un mensaje entre vistas con flash,lo recoje la siguiente request
        # se puede mandar cualquier string o tmb prebuilts con error,warning etc ver API
        flash('Contact Added successfully')

    # si redireccionamos debemos usar las funciones redirect y url_for
    return redirect(url_for('Index'))  # Index es la funcion,no el archivo
    # ES url_for(functionname)


# ruta para eliminar contactos.Va a recibir un parametro
# concatenado a la ruta.
@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    # con la funcion format interpolamos el valor de id al string
    # en las llaves debemos indicar el indice de la variable,en el format el nombre
    cur.execute('DELETE FROM contacts where id = {0}'.format(id))

    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

# ruta para editar contactos.Esta vez no decimos el tipo


@app.route('/edit/<id>')
def edit_contact(id):
    # hacemos la select de ese id
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id={0}'.format(id))
    # Si le pasamos la interpolacion con %s %s el segundo parametro es una tupla,aunque sea un unico valor va entre parentesis
    # cur.execute('SELECT * FROM contacts where id = %s, (id))
    contacto = cur.fetchall()
    # ES contacto[0] para mandar solo la tupla 0, pues es la unica que hay
    return render_template('edit-contact.html', contact=contacto[0])

# ruta para update.Rescatamos las variables por POST y actaulizamos
#fijarse en el uso de triples comillas para hacer la instruccion multilinea

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE contacts SET
        fullname = %s,
        phone = %s,
        email = %s WHERE Id = %s
        """, (fullname, phone, email, id))
        # ojo FALTA EJECUTARLA!!
        print(id)
        mysql.connection.commit()
        flash('Contact Updated Successfully')
        return redirect(url_for('Index'))


# levantamos el server
if __name__ == "__main__":
    app.run( debug=True)
