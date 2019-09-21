
from flask import Flask, request, jsonify, redirect, url_for
import flask_excel as excel

app = Flask(__name__)
excel.init_excel(app)

from flask_sqlalchemy import SQLAlchemy  # noqa
from datetime import datetime  # noqa

#create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tomar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#create table Docente
class Docente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_docente = db.Column(db.String(200))
    
    area_nome = db.Column(db.String, db.ForeignKey('area.nome_area'))
    area = db.relationship('Area',
                               backref=db.backref('posts',
                                                  lazy='dynamic'))

    qualifica_docente = db.Column(db.String(200))

    def __init__(self, nome_docente, area, qualifica_docente):
        self.nome_docente = nome_docente
        self.area = area
        self.qualifica_docente = qualifica_docente

    def __repr__(self):
        return '<Docente %r>' % self.nome_docente

#create table Area
class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_area = db.Column(db.String(200))

    def __init__(self, nome_area):
        self.nome_area = nome_area

    def __repr__(self):
        return '<Area %r>' % self.nome_area

#create table Tipo
class Tipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_curso = db.Column(db.String(200))


    def __init__(self, tipo_curso):
        self.tipo_curso = tipo_curso

    def __repr__(self):
        return '<Tipo %r>' % self.tipo_curso
    
#create table Curso
class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_curso = db.Column(db.String(200))

    curso_tipo = db.Column(db.String, db.ForeignKey('tipo.tipo_curso'))
    tipo = db.relationship('Tipo',
                           backref=db.backref('posts',
                                              lazy='dynamic'))
    duracao_curso = db.Column(db.String(200))
    provas_ingresso = db.Column(db.String(200))
    classificacao_minima = db.Column(db.String(200))

    def __init__(self, nome_curso, tipo, duracao_curso, provas_ingresso, classificacao_minima):
        self.nome_curso = nome_curso
        self.tipo = tipo
        self.duracao_curso = duracao_curso
        self.provas_ingresso = provas_ingresso
        self.classificacao_minima = classificacao_minima

    def __repr__(self):
        return '<Curso %r>' % self.nome_curso

#create table Uc
class Uc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_uc = db.Column(db.String(200))

    def __init__(self, nome_uc):
        self.nome_uc = nome_uc

    def __repr__(self):
        return '<UC %r>' % self.nome_uc

#create table Plano
class Plano(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.String(200))
    semestre = db.Column(db.String(200))
    plano_area = db.Column(db.String(200))
    uc_nome = db.Column(db.Integer, db.ForeignKey('uc.nome_uc'))
    uc = db.relationship('Uc',
                         backref=db.backref('uc_posts',
                                            lazy='dynamic'))
    plano_ects = db.Column(db.String(200))
    plano_docente = db.Column(db.String(200))
    plano_curso = db.Column(db.String(200))
    plano_tipo = db.Column(db.String(200))

    def __init__(self, ano, semestre, plano_area , uc, plano_ects, plano_docente, plano_curso, plano_tipo):
        self.ano = ano
        self.semestre = semestre
        self.plano_area = plano_area
        self.uc = uc
        self.plano_ects = plano_ects
        self.plano_docente = plano_docente
        self.plano_curso = plano_curso
        self.plano = plano_tipo

    def __repr__(self):
        return '<Plano %r>' % self.plano_uc


db.create_all()

#when using import on the local browser, it requests a xls file to insert the values to the tables
@app.route("/import", methods=['GET', 'POST'])
def doimport():
    if request.method == 'POST':

        def area_init_func(row):
            a = Area(row['nome_area'])
            a.id = row['id']
            return a

        def docente_init_func(row):
            a = Area.query.filter_by(nome_area=row['area_docente']).first()
            d = Docente(row['nome_docente'], a,  row['qualifica_docente'])
            return d

        def uc_init_func(row):
            u = Uc(row['nome_uc'])
            u.id = row['id']
            return u

        def tipo_init_func(row):
            t = Tipo(row['tipo_curso'])
            t.id = row['id']
            return t

        def curso_init_func(row):
            t = Tipo.query.filter_by(tipo_curso=row['tipo_curso']).first()
            c = Curso(row['nome_curso'], t, row['duracao_curso'], row['provas_ingresso'],  row['classificacao_minima'])
            return c

        def plano_init_func(row):
            u = Uc.query.filter_by(nome_uc=row['plano_uc']).first()
            p = Plano(row['ano'], row['semestre'], row['plano_area'], u, row['plano_ects'], row['plano_docente'],
                      row['plano_curso'], row['plano_tipo'])
            return p

        request.save_book_to_database(
            field_name='file', session=db.session,
            tables=[Area, Docente, Tipo, Curso, Uc, Plano],
            initializers=[area_init_func, docente_init_func, tipo_init_func, curso_init_func, uc_init_func, plano_init_func])
        return redirect(url_for('.handson_table'), code=302)
    return '''
    <!doctype html>
    <head>
    <link rel="stylesheet" type="text/css" href="static/styles/main.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <title>Upload an excel file</title>
    </head>

    <body style="background-color: #f6f6f6">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <a class="navbar-brand" href="#!">IPT</a>

      <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
        <ul class="navbar-nav mr-auto mt-2 mt-md-0">
          <li class="nav-item active">
            <a class="nav-link" href="#!">Instituto Politécnico de Tomar<span class="sr-only">(current)</span></a>
          </li>
        </ul>
      </div>
    </nav>

    <header class="intro">
        <div class="intro-body">
            <div class="container">
                <div class="row">
                    <div class="col-md-12">
                      <h1 class="brand-heading">Instituto Politécnico</br>de Tomar</h1>
                      </a>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <section class="head-section text-center">
        <h1>Upload ficheiro dados (dadosBD.xlsx)</h1>
    </section>
    <section id="content" class="content-section text-center clearfix">
        <div class="container">
            <form action="" method=post enctype=multipart/form-data><p>
                <input type=file name="file">
                <input type=submit value=Upload>
            </form>
        </div>
    </section>

    <section class="plot text-center clearfix">
        <div class="container">
            <h4>Foi realizada uma pequena análise aos dados obtidos através da realização dos seguintes gráficos</h4>
            <p>Estudo do número de cursos existentes pelo tipo de curso.</p>
            <img src="/static/plot(1).png" class="img-fluid img-thumbnail" alt="...">
        </div>
    </section>

    <section class="plot text-center clearfix">
        <div class="container">
            <p>Estudo da qualificação dos docentes do instituto.</p>
            <img src="/static/plot(2).png" class="img-fluid img-thumbnail" alt="...">
        </div>
    </section>

    <section class="plot text-center clearfix">
        <div class="container">
            <p>Estudo do número de unidades curriculares por área.</p>
            <img src="/static/plot(3).png" class="img-fluid img-thumbnail" alt="...">
        </div>
    </section>
    
    <footer>
        <div class="container text-center" style="color: black">
        
            <div class="icons col-md-12">
                <p>Copyright &copy; 2018 - Instituto Politécnico de Tomar</p>
            </div>
        </div>
    </footer>
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    </body>
    </html>
    '''

#when using export on the local browser, it downloads a xls file of the database
@app.route("/export", methods=['GET'])
def doexport():
    return excel.make_response_from_tables(db.session, [Area, Docente, Tipo, Curso, Uc, Plano], "xls")

#when using handson_view on the local browser, it shows the database without values
@app.route("/handson_view", methods=['GET'])
def handson_table():
    return excel.make_response_from_tables(
        db.session, [Area, Docente, Tipo, Curso, Uc, Plano], 'handsontable.html')


if __name__ == "__main__":
    app.debug = True
    app.run()