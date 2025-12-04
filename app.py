import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from config import Config
from models import db, Teacher

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "supersecretkey123"

# Инициализация базы
db.init_app(app)
with app.app_context():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    db.create_all()

ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Каталог учителей
@app.route('/catalog')
def catalog():
    q = request.args.get('q', '').strip()
    if q:
        teachers = Teacher.query.filter(
            (Teacher.name.ilike(f"%{q}%")) |
            (Teacher.subject.ilike(f"%{q}%")) |
            (Teacher.description.ilike(f"%{q}%")) |
            (Teacher.position.ilike(f"%{q}%"))
        ).order_by(Teacher.name).all()
    else:
        teachers = Teacher.query.order_by(Teacher.name).all()
    return render_template('catalog.html', teachers=teachers, query=q)

# Профиль учителя
@app.route('/teacher/<int:teacher_id>')
def profile(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    return render_template('profile.html', teacher=teacher)

# Добавление учителя (только админ)
@app.route('/add', methods=['GET', 'POST'])
def add_teacher():
    if "admin" not in session:
        flash("Бұл бетке кіруге құқығыңыз жоқ!", "danger")
        return redirect(url_for("login"))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        subject = request.form.get('subject', '').strip()
        years = request.form.get('years', '').strip()
        description = request.form.get('description', '').strip()
        position = request.form.get('position', '').strip()

        errors = []
        if not name:
            errors.append("Аты міндетті.")
        if not subject:
            errors.append("Пәні міндетті.")
        years_int = None
        if years:
            try:
                years_int = int(years)
            except:
                errors.append("Жылдар саны тек бүтін сан болуы керек.")

        # Работа с фото
        photo_file = request.files.get("photo")
        filename = "default.png"
        if photo_file and allowed_file(photo_file.filename):
            filename = secure_filename(photo_file.filename)
            photo_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('add_teacher.html',
                                   form_data={'name': name, 'subject': subject, 'years': years,
                                              'description': description, 'position': position})

        # Добавляем учителя
        t = Teacher(name=name, subject=subject, years=years_int,
                    description=description, position=position, photo=filename)
        db.session.add(t)
        db.session.commit()
        flash("Мұғалім сәтті қосылды!", "success")
        return redirect(url_for('catalog'))

    return render_template('add_teacher.html', form_data={})

# Авторизация
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "qwerty123":
            session["admin"] = True
            flash("Сіз сәтті кірдіңіз!", "success")
            return redirect(url_for("add_teacher"))
        else:
            flash("Қате логин немесе құпия сөз!", "danger")
    return render_template("login.html")

# Выход
@app.route("/logout")
def logout():
    session.pop("admin", None)
    flash("Сіз жүйеден шықтыңыз!", "info")
    return redirect(url_for("index"))


# Удаление учителя
@app.route("/teacher/<int:teacher_id>/delete", methods=["POST","GET"])
def delete_teacher(teacher_id):
    if "admin" not in session:
        flash("Құқығыңыз жоқ!", "danger")
        return redirect(url_for("login"))
    teacher = Teacher.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    flash("Мұғалім өшірілді!", "success")
    return redirect(url_for("catalog"))

# Редактирование учителя
@app.route("/teacher/<int:teacher_id>/edit", methods=["GET", "POST"])
def edit_teacher(teacher_id):
    if "admin" not in session:
        flash("Құқығыңыз жоқ!", "danger")
        return redirect(url_for("login"))

    teacher = Teacher.query.get_or_404(teacher_id)
    if request.method == "POST":
        teacher.name = request.form.get('name', teacher.name)
        teacher.subject = request.form.get('subject', teacher.subject)
        teacher.years = int(request.form.get('years', teacher.years or 0))
        teacher.position = request.form.get('position', teacher.position)
        teacher.description = request.form.get('description', teacher.description)

        # Фото
        photo_file = request.files.get("photo")
        if photo_file and allowed_file(photo_file.filename):
            filename = secure_filename(photo_file.filename)
            photo_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            teacher.photo = filename

        db.session.commit()
        flash("Мұғалім жаңартылды!", "success")
        return redirect(url_for("profile", teacher_id=teacher.id))

    return render_template("edit_teacher.html", teacher=teacher)



# Запуск
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
