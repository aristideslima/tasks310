# Imports
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

# My App
app = Flask(__name__)
Scss(app)

# Flask-SQLAlchemy

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(100),nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return  f"task {self.id}"

with app.app_context():
    db.create_all

# Routes do webpages
# Home Page
# Rota Inicial - Função de Consulta as Tasks e de Inclusão de Tasks
@app.route("/", methods=["POST","GET"])
def index():
    # Add A Task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    # See All Current Tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html', tasks=tasks)

# Rota para exclusão das Tasks
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"

# Rota para edição das Tasks
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template('edit.html', task=task)

if __name__ in "__main__":
    app.run(debug=True)
