from flask import Flask, render_template, request, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

# Creating flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)


# Creating the table
class Tasks(db.Model):
    id: Mapped[int] = mapped_column(nullable=False, unique=True, primary_key=True)
    work: Mapped[str] = mapped_column(nullable=False)


@app.route("/", methods=["POST", "GET"])
def home():
    all_works = db.session.query(Tasks).all()
    return render_template("index.html", all_works=all_works)


@app.route("/new_task", methods=["POST", "GET"])
def new_task():
    if request.method == "POST":
        task = request.form.get("task")
        db_task = Tasks(work=task)
        db.session.add(db_task)
        db.session.commit()
        return redirect("/")


@app.route("/check", methods=["POST", "GET"])
def check():
    data = request.get_json()
    checkbox_state = data.get('test')
    delete_id = int(checkbox_state)
    delete_work = db.session.query(Tasks).get(delete_id)
    db.session.delete(delete_work)
    db.session.commit()
    return jsonify({"success": True, "message": "Task deleted successfully"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
