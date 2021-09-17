from flask import Flask
app = Flask(__name__)

from flask import render_template, request

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

from werkzeug.utils import secure_filename
import os

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

app.config["SECRET_KEY"] = "seckey"
app.config["RECAPTCHA_PUBLIC_KEY"] = "6LfvPRgbAAAAADNED3uO5xbBAJo3Lo7LsMqmNIeZ"
app.config["RECAPTCHA_PRIVATE_KEY"]="6LfvPRgbAAAAAF0AxKU-muhLdXlrFhzHI3p81CXD"

app.config['UPLOAD_FOLDER'] = 'static/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

class Widgets(FlaskForm):
    recaptcha = RecaptchaField()
    upload_first = FileField('Загрузите изображение', validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')])

class ITask(FlaskForm):
    upload_file1 = FileField('Загрузите изображение', validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')])
    upload_file2 = FileField('Загрузите изображение', validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')])
    selector = SelectField('Ориентация присоединения', choices=[(1, 'Горизонтально'), (2, 'Вертикально')])

import neural

@app.route("/", methods=("GET", "POST"))
def home():
    form = Widgets()
    if request.method == "POST":
        if form.validate_on_submit():
            form.upload_first.data.save(app.config['UPLOAD_FOLDER'] + 'neural_img.png')
            image = neural.recognize(app.config['UPLOAD_FOLDER'] + 'neural_img.png')
            return render_template('start.html', form=form, img=app.config['UPLOAD_FOLDER'] + 'neural_img.png', neur=image)
    if request.method == "GET":
        return render_template("start.html", form=form)

import defs

@app.route('/load', methods=['GET', 'POST'])
def upload_file():
    form = ITask()
    if request.method == 'POST':
        if form.validate_on_submit():
            img_1 = app.config['UPLOAD_FOLDER'] + 'to_be_joined_first.png'
            img_2 = app.config['UPLOAD_FOLDER'] + 'to_be_joined_second.png'
            form.upload_file1.data.save(img_1)
            form.upload_file2.data.save(img_2)

            if form.selector.data == '1':
                defs.ofromt(img_1, img_2)
            else:
                defs.ofromt(img_1, img_2, 1)

            final_image = app.config['UPLOAD_FOLDER'] + 'timages_joined.png'

            graph_1 = app.config['UPLOAD_FOLDER'] + 'to_be_joined_first_graph.png'
            graph_2 = app.config['UPLOAD_FOLDER'] + 'to_be_joined_second_graph.png'
            graph_3 = app.config['UPLOAD_FOLDER'] + 'timages_joined_graph.png'

            # Графики
            defs.GRAPHS(app.config['UPLOAD_FOLDER'] + 'to_be_joined_first.png', app.config['UPLOAD_FOLDER'] + 'to_be_joined_first_graph.png', graph_1)
            defs.GRAPHS(app.config['UPLOAD_FOLDER'] + 'to_be_joined_second.png', app.config['UPLOAD_FOLDER'] + 'to_be_joined_second_graph.png', graph_2)
            defs.GRAPHS(app.config['UPLOAD_FOLDER'] + 'timages_joined.png', app.config['UPLOAD_FOLDER'] + 'timages_joined_graph.png', graph_3)

            return render_template('form.html', form = form, img_1 = img_1, img_2 = img_2, compiled = final_image, graphs = [graph_1, graph_2, graph_3])

    return render_template('form.html', form = form)

if __name__ == "__main__":
  app.run(debug=True)
