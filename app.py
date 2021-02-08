import functools
import os
from flask import Flask, render_template, flash, request, redirect, url_for, current_app, session, send_file, current_app, g, make_response,send_from_directory
from formularios import formInicio, formSesion, formCambiarContrasena, formVerificarContrasena, formCrearImagen, formBuscarImagen, formEliminarImagen
import yagmail 
from modelo import sql_nuevo_usuario, sql_activar_usuario, sql_leer_imagenes_propias,sql_leer_imagen_propia, sql_leer_imagenes_publicas,sql_buscar_imagenes,sql_iniciar_sesion,sql_restablecer_contrasena,sql_cambiar_contrasena,sql_id_usuario,sql_id_imagen,sql_crear_imagen,sql_actualizar_imagen,sql_eliminar_imagen,sql_id_usuario_por_correo,sql_leer_usuario,sql_usuario_activo
#from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint

app = Flask(__name__)
app.secret_key = os.urandom( 24 )
#app.secret_key = '12345'
global rand
rand = str(randint(1000,9999))
global rand2 
rand2 = str(randint(1000,9999))

@app.route("/", methods= ["GET","POST"])
def index():
    form = formBuscarImagen()
    if g.user:
        return redirect(url_for('inicialSesion'))

    if request.method == 'POST':
        busqueda = request.form['busqueda']
        imagenes_publicas = sql_buscar_imagenes(busqueda)
        if imagenes_publicas ==[]:
            flash("Su búsqueda no arrojó resultados. Pruebe con otros términos de búsqueda.")            

        return render_template("vistaInicial.html",img_p = imagenes_publicas,form=form)
    
    else:
        imagenes_publicas = sql_leer_imagenes_publicas()
        return render_template("vistaInicial.html",form=form,img_p=imagenes_publicas)




@app.route("/registroUsuario", methods = ["GET", "POST"])
def registroUsuario():
    form = formInicio()
    if g.user:
        return redirect(url_for('inicialSesion'))

    if request.method == 'POST':
        if (form.validate_on_submit()):
                nombreUsuario = request.form['usuario']
                correo = request.form['email']
                contrasena = request.form['password']
                print('NombreUsuario = ' + nombreUsuario)
                if sql_id_usuario_por_correo(correo) is not None:
                    error = 'El correo ya existe'.format( correo )
                    flash ( error )
                    return render_template("registroUsuario2.html",form = form)
                    
                elif sql_id_usuario(nombreUsuario) is not None:
                    
                    error2 = 'El nombre de usuario ya existe.'.format( nombreUsuario )
                    flash ( error2 )
                    return render_template("registroUsuario2.html",form = form)

                else:    
                    hashContraseña = generate_password_hash(contrasena)
                    sql_nuevo_usuario(nombreUsuario,correo,hashContraseña)
                    
                    #flash( 'Revisa tu correo para activar tu cuenta' )
                    yag = yagmail.SMTP('misiontic2022grupo11@gmail.com', '2022Grupo11') 
                    yag.send(to=correo, subject='Activa tu cuenta',
                    contents= nombreUsuario + ' Da click en el link para activar tu cuenta: https://54.196.174.67//activar/'+nombreUsuario+'/'+rand) 
                    return redirect(url_for('activarUsuario'))

        return render_template("registroUsuario2.html",form = form)
    return render_template("registroUsuario2.html",form = form)
         

@app.route("/inicioSesion", methods = ["GET", "POST"])
def iniciarSesion():
    form2 = formSesion()
    if g.user:
        
        return redirect(url_for('inicialSesion'))
    if (form2.validate_on_submit()):
        
        NombreUsuario = request.form['usuario2']
        contrasena = request.form['password2']
        user = sql_iniciar_sesion(NombreUsuario)
        if user is not None:
            activo = sql_usuario_activo(NombreUsuario)


        if user is None:
            error = 'Usuario o contraseña inválidos'
            
        elif activo is None:
            error = 'Usuario o contraseña inválidos'
        elif activo is not None and activo == 0:
            error = 'El usuario no esta activo'
            
        elif check_password_hash( user[1], contrasena ):
            
            session.clear()
            session['user_id'] = user[0]
            resp = make_response( redirect( url_for( 'inicialSesion' ) ) )
            resp.set_cookie('NombreUsuario', NombreUsuario)
            load_logged_in_user()
            return resp
        else:
            error = 'Usuario o contraseña inválidos'
        flash(error)
    return render_template("iniciarSesion.html",form = form2)


      
@app.route("/activar", methods = ["GET", "POST"])
def activarUsuario():
            return render_template("activarUsuario2.html")     

@app.route("/activar/<string:nombreUsuario>/<string:r2>",methods = ["GET","POST"]) 
def activacionUsuario(nombreUsuario,r2):
    if r2 == rand:
        sql_activar_usuario(nombreUsuario)
        return redirect(url_for('iniciarSesion'))
    else:
        return "Ha ocurrido un error. Verifique el link de acceso"


def login_required(view):
    @functools.wraps( view )
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect( url_for( 'index' ) )
        return view( **kwargs )
    return wrapped_view

#########################
@app.route( '/downloadimage/<string:idImagen>', methods=('GET', 'POST') )
@login_required
def downloadimage(idImagen):
    imagen = sql_leer_imagen_propia(idImagen)
    img = imagen[2]
    return send_file( img[3:], as_attachment=True )
    #return send_from_directory(imagen[2],'image', as_attachment=True)
#########################

@app.route("/inicialConSesion/", methods = ["GET", "POST"])
@login_required 
def inicialSesion():
    from_id = g.user[0]
    
    form = formBuscarImagen()
    if request.method == 'POST':
        buscar = None
        buscar = request.form['busqueda']
        if buscar is not None:
            imagenes_publicas = sql_buscar_imagenes(buscar)
            print(imagenes_publicas)
            if imagenes_publicas ==[]:
                flash("Su búsqueda no arrojó resultados. Pruebe con otros términos de búsqueda.")
    else: 
        imagenes_publicas = sql_leer_imagenes_publicas()
    imagen = sql_leer_imagenes_propias(from_id)
    return render_template("vistaInicialConSesion.html",imagen = imagen, img_p=imagenes_publicas,form = form)
        


@app.route("/restablecerContrasena", methods = ["GET", "POST"])
def restablecerContrasena():
        #global rand2 = str(randint(1000,9999))
        form = formCambiarContrasena()  
        if request.method == 'POST':
            correo=request.form['email2']

            if (form.validate_on_submit()):
                if sql_restablecer_contrasena(correo) == 1:
                    
                    yag = yagmail.SMTP('misiontic2022grupo11@gmail.com', '2022Grupo11') 
                    yag.send(to=correo, subject='Restablecimiento de contraseña',
                            contents= ' Da click en el link para restablecer tu contraseña.. https://54.196.174.67/cambiarContrasena/'+correo+'/'+rand2)
                    flash('Se ha enviado un mensaje al correo electrónico registrado con su cuenta que contiene un link para restablecer su contraseña.')            
                    return redirect(url_for('restablecerContrasena'))
                else:
                    flash('No existe un usuario con el correo ingresado o su cuenta no esta activa')
                    return redirect(url_for('restablecerContrasena'))
            return render_template("vistaRestablecerContrasena.html",form = form )        
        return render_template("vistaRestablecerContrasena.html",form = form )
         



@app.route("/cambiarContrasena/<string:correo>/<string:r>", methods = ["GET", "POST"])
def cambiarContrasena(correo,r):
    print('r')
    print(r)
    print('rand')
    print(rand2)
    if r == rand2:
        form = formVerificarContrasena() 
        if request.method == 'POST':
            contrasena=request.form ['password1']
            hashContraseña = generate_password_hash(contrasena)
            sql_cambiar_contrasena(correo,hashContraseña)
            if (form.validate_on_submit()):
                return redirect(url_for('iniciarSesion'))
            return render_template("cambiarContrasena.html",form = form)    
        return render_template("cambiarContrasena.html",form = form)
    
    else:
        return "Un error ha ocurrido. Verifique el link de acceso"



@app.route("/crearImagen/", methods = ["GET", "POST"])
@login_required
def crearImagen():
    
    imgQuery ='../static/images/1.png'
    
    NombreUsuario = g.user[0]
    form = formCrearImagen()

    if request.method == 'POST':
        if (form.validate_on_submit()):
            estado = 0

            nombreImg = str(randint(1000,9999))

            nombreImagen = request.form['nombre']
            descripcion = request.form['descripcion']
            privacidad = request.form['privacidad']

            imgSave = './static/images/'+nombreImagen+nombreImg+'.jpg'
            imgQuery = '../static/images/'+nombreImagen+nombreImg+'.jpg'
            request.files['file2'].save(imgSave)

            if privacidad == "Privada": estado = 1 
            sql_crear_imagen(NombreUsuario,nombreImagen,descripcion,estado,imgQuery)
            return redirect('/inicialConSesion/')
        else:
            print("ERROR AL CREAR")
            flash("Ocurrio un Error, contactese con el administrador del sistema...")
            return render_template("vistaCrear.html",form = form, NombreUsuario = NombreUsuario,imgQuery = imgQuery)   
        
    return render_template("vistaCrear.html",form = form, NombreUsuario = NombreUsuario,imgQuery = imgQuery)    


@app.route("/editarImagen/<string:idImagen>", methods = ["GET", "POST"])
@login_required
def editarImagen(idImagen):
    NombreUsuario = g.user[0]
    imagen = sql_leer_imagen_propia(idImagen)

    form = formCrearImagen()
    form2 = formEliminarImagen()
    form.nombre.data = imagen[0]
    form.descripcion.data = imagen[1]
    
    if request.method == 'POST':
        if (form.validate_on_submit()):
            
            nombreImg = str(randint(1000,9999))
            estado = 0
            nombreImagen = request.form['nombre']
            descripcion = request.form['descripcion']
            privacidad = request.form['privacidad']
  
            

            if request.files['file2'].filename == '':
                imgQuery = imagen[2]
            else:
                imgSave = './static/images/'+nombreImagen+nombreImg+'.jpg'
                imgQuery = '../static/images/'+nombreImagen+nombreImg+'.jpg'
                request.files['file2'].save(imgSave)

            if privacidad == "Privada": estado = 1 
            sql_actualizar_imagen(NombreUsuario,nombreImagen,descripcion,estado,imgQuery,idImagen)
            return redirect('/inicialConSesion/')

        elif form2.validate_on_submit():
            sql_eliminar_imagen(idImagen)
           
            return redirect('/inicialConSesion/')
        else:
            
            flash("Ocurrio un Error, contactese con el administrador del sistema...")
            return render_template("vistaEditarImagen.html",form = form, form2 = form2,NombreUsuario = NombreUsuario, imagen = imagen)
        
    return render_template("vistaEditarImagen.html",form = form, form2 = form2 ,NombreUsuario = NombreUsuario, imagen = imagen)




@app.route("/editarImagenes/", methods = ["GET", "POST"])
@login_required
def editarImagenes(): 
    NombreUsuario = g.user[0]
    imagen = sql_leer_imagenes_propias(NombreUsuario)  
    return render_template("vistaEditarImagenes.html",imagen=imagen,NombreUsuario = NombreUsuario)


#Metodo Eliminar Imagen
@app.route("/eliminarImagen/")
def eliminarImagen(id_imagen):
    sql_eliminar_imagen(id_imagen)
    return redirect('/inicialConSesion/')

@app.before_request
def load_logged_in_user():
    user_id = session.get( 'user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = sql_leer_usuario(user_id)

@app.route( '/logout' )
def logout():
    session.clear()
    return redirect( url_for( 'index' ) )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=443, ssl_context=('micertificado.pem', 'llaveprivada.pem') )
    #app.run( host='127.0.0.1', port =443, ssl_context=('micertificado.pem', 'llaveprivada.pem') )

