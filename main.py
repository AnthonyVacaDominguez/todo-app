#libreria para usar flask
from flask import Flask, render_template, request, url_for, redirect
#librerias para el uso de base de datos
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
app = Flask(__name__)
#configuro parametro SQLALCHEMY_DATABASE_URI con la ubicacion de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.sqlite"

db = SQLAlchemy(app)

#cear tabla
class Todo(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String, nullable=False)
    state: Mapped[str] = mapped_column(db.String, nullable=False, default='incompleto')

#crea la base y las tablas necesarias con el contexto de la aplicacion
with app.app_context():
    db.create_all()


#RUTAS DE APLICACION
@app.route("/",methods=['GET','POST'])
def home():
    lista_tareas =[]
    #boton agregar
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            obj = Todo(name=name)
            db.session.add(obj)
            db.session.commit()
    lista_tareas = Todo.query.all()
    return render_template('select.html', lista_tareas = lista_tareas)


@app.route("/delete/<id>")
def delete(id):
    obj=Todo.query.filter_by(id=id).first()
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for('home'))
    

@app.route("/update/<id>")
def update(id):
    obj=Todo.query.filter_by(id=id).first()
    obj.state = "completo"
    db.session.commit()
    return redirect(url_for('home')) 

if __name__ == '__main__':
    app.run(debug=True)