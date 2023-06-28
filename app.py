from flask import * 
from flask import render_template
from flask import Flask,request,url_for,redirect,session,flash
from datetime import datetime
import hashlib

app=Flask (__name__)
app.config.from_pyfile('config.py')
from clases import Preceptor,Padre,Estudiante,Curso,Asistencia,db

@app.route('/')
def inicio():
    return render_template('home.html')
@app.route('/alta',methods=['POST'])
def alta():
    email=request.form['email']
    clave=request.form['clave']
    clavecif=hashlib.md5(clave.encode()).hexdigest()
    usuario=Preceptor.query.filter_by(correo=email,clave=clavecif).first() #recorre la clase preceptor y toma el primero que cumpla estas condiciones
    
    if usuario!=None:
        session["id"]=usuario.id
        return render_template('preceptor.html')
    else:
        return render_template('home.html', mensaje='Usuario incorrecto')

@app.route('/VerAlumnos',methods=['POST','GET'])
def VerAlumnos():
    cursos=Curso.query.filter(Curso.idpreceptor==session["id"]).all()
    return render_template('seleccionarcurso.html',cursos=cursos)

@app.route('/infoAsistencia',methods=['POST','GET'])
def informes():
    cursos=Curso.query.filter(Curso.idpreceptor==session["id"]).all()
    return render_template('selecCursoInforme.html',cursos=cursos)
@app.route('/muestraInforme',methods=['POST','GET'])
def muestraInforme():
    cursoSelc=request.form.get("curso")
    alumnos=Estudiante.query.filter_by(idCurso=cursoSelc).all()
    asistencias=Asistencia.query.all()
    return render_template('informe.html',asistencias=asistencias,alumnos=alumnos)

@app.route('/cursoseleccionado',methods=['POST','GET'])
def cursoseleccionado():
    estudiantes=Estudiante.query.filter(Estudiante.idCurso==request.form.get("curso")).all()
    return render_template('cursoseleccionado.html',alumno=estudiantes)

@app.route('/registrarAsistencia',methods=['POST','GET'])
def registrarAsistencia():
    fecha=request.form.get('fecha')
    tipoclase=request.form.get('tipoclase')
    idcurso = request.form.get('curso')
    alumnos=Estudiante.query.filter(Estudiante.idCurso==idcurso).all()
    return render_template('cursoseleccionado.html', alumnos=alumnos,fecha=fecha, tipoclase=tipoclase)

    
@app.route('/marcarAsistencia', methods=['POST','GET'])
def marcarAsistencia():
    cursos=Curso.query.all()
    idAlumno=request.args.get('idalumno')
    fecha=request.args.get('fecha')
    tipoclase=request.args.get('tipoclase')
    return render_template("asistencia.html", fecha=fecha,idalumno=idAlumno,tipoclase=tipoclase)

@app.route('/confirmarAsistencia',methods=['POST','GET'])
def confirmarAsistencia():
    fecha=request.form['fecha']
    codigoclase=request.form['codigoclase']
    asistio=request.form['asis']
    justificacion=request.form['justificacion']
    idestudiante=request.form.get('idalumno')
    asistencia = Asistencia(fecha=fecha,codigoclase=codigoclase,asistio=asistio,justificacion=justificacion,idestudiante=idestudiante)
    db.session.add(asistencia)
    db.session.commit()
    return redirect('/VerAlumnos')

    
    
       

if __name__=='__main__':
    app.run(debug=True)
    
