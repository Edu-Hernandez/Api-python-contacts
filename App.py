from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# coneccion de musql
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "flaskcontacts"
mysql = MySQL(app)

# setting, esto se hace cuando se envia mensajes a index con flash
app.secret_key = "mysecretkey"


@app.route("/")
def Datos():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts")
    data = cur.fetchall()

    return render_template("index.html", contacts=data)


@app.route("/add_contact", methods=["POST"])
def add_contact():
    if request.method == "POST":
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)",
            (fullname, phone, email),
        )
        mysql.connection.commit()

        flash("Contacto agregado satisfactoriamente")
        # retorna a la funcion que muestra el formulario
        return redirect(url_for("Datos"))


@app.route("/edit/<id>")
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = %s", (id))
    data = cur.fetchall()
    return render_template("edit.html", contact=data[0])


@app.route("/update/<id>", methods=["POST"])
def update_contact(id):
    if request.method == "POST":
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        cur = mysql.connection.cursor()

        # Corregir la consulta SQL
        cur.execute(
            "UPDATE contacts SET fullname = %s, phone = %s, email = %s WHERE id = %s",
            (fullname, phone, email, id),
        )
        mysql.connection.commit()
        cur.close()  # No olvides cerrar el cursor
        flash("Contacto actualizado satisfactoriamente")

        # Redirigir después de la actualización
        return redirect(url_for("Datos"))


# recibe un numero que se convierte a string para eliminar
@app.route("/delete/<string:id>")
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contacts WHERE id = {0}".format(id))
    mysql.connection.commit()
    flash('contacto removido sasticfactoriamente"')
    return redirect(url_for("Datos"))


if __name__ == "__main__":
    app.run(port=3000, debug=True)
