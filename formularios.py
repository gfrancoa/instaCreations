from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators, TextField, TextAreaField, RadioField, FileField
from wtforms.fields.html5 import EmailField 
from wtforms.validators import DataRequired,Length,Regexp,EqualTo, InputRequired
#este archivo es una clase

class formInicio(FlaskForm): #dentro de los paréntesis va la herencia
    pass_reguex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\W_]{8,}$"
    user_reguex = "^(?=.{8,20}$)"
    # email_reguex = "^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"
    email_reguex = "^[^@]+@[^@]+\.[a-zA-Z]{2,}$"

    #campos de registro
    usuario = TextField('Nombre de usuario', validators=[DataRequired(message="Campo requerido"),Regexp(user_reguex,message ='El nombre de usuario debe tener mínimo 8 caracteres y máximo 20')],render_kw={"placeholder": "miUsuario123", "class":"form-control","style":"text-transform: none"})
    password = PasswordField('Password',validators=[DataRequired(message="Campo requerido"),Regexp(pass_reguex,message='La contraseña debe contener mínimo 6 caracteres, un dígito, una mayúscula y una minúscula')],render_kw={"placeholder": "Contraseña", "class":"form-control","style":"text-transform: none"})
    email = EmailField('Correo electrónico',validators=[DataRequired(message="Campo requerido"),Regexp(email_reguex,message ='El email debe ser de la forma micorreo@ejemplo.com')],render_kw={"placeholder": "micorreo@example.com", "class":"form-control","style":"text-transform: none"})
    enviar = SubmitField('Enviar',render_kw={"class":"btn btn-defeault btn-send"})

class formSesion(FlaskForm):
    #campos de iniciar sesión
    iniciar = SubmitField('Iniciar',render_kw={"class":"btn btn-defeault btn-send"})
    usuario2 = TextField('Nombre de usuario', [DataRequired(message="Campo requerido")],render_kw={"placeholder": "miUsuario123", "class":"form-control","style":"text-transform: none"}) 
    password2 = PasswordField('Password',validators=[DataRequired(message="Campo requerido")],render_kw={"placeholder": "Contraseña", "class":"form-control", "style":"text-transform: none"})

class formCambiarContrasena(FlaskForm):
    #campos de restablecer contraseña
    email_reguex = "^[^@]+@[^@]+\.[a-zA-Z]{2,}$"
    cambiarContraseña = SubmitField('Cambiar Contraseña',render_kw={"class":"btn btn-defeault btn-send","style":"margin-left: 60px;"})
    email2 = EmailField('Correo electrónico',validators=[DataRequired(message="Campo requerido"),Regexp(email_reguex,message ='El email debe ser de la forma micorreo@ejemplo.com')],render_kw={"placeholder": "micorreo@example.com", "class":"form-control"})

class formVerificarContrasena(FlaskForm):
    #campos de cambiar contraseña
    pass_reguex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\W_]{8,}$"
    password1 = PasswordField('Contraseña',validators=[DataRequired(message="Campo requerido"),Regexp(pass_reguex,message='La contraseña debe contener mínimo 6 caracteres, un dígito, una mayúscula y una minúscula'),EqualTo('password3', message='Las contraseñas deben coincidir')],render_kw={"placeholder": "Contraseña", "class":"form-control"})
    password3 = PasswordField('Confirma tu contraseña',validators=[DataRequired(message="Campo requerido")],render_kw={"placeholder": "Contraseña", "class":"form-control"})
    cambioContrasena = SubmitField('Cambiar contraseña',render_kw={"class":"btn btn-defeault btn-send"})

class formCrearImagen(FlaskForm):
    nombre_reguex = "^(?=.{5,30}$)"
    descripcion_reguex = "^(?=.{15,250}$)"
    nombre = TextField('Nombre imagen', [DataRequired(message="Campo requerido"),Regexp(nombre_reguex,message ='El nombre de la imagen debe tener mínimo 5 caracteres y máximo 30')],render_kw={"placeholder": "miImagen123", "class":"form-control", "style":"color: #1f1f1f"})
    descripcion = TextAreaField('Descripción imagen', [DataRequired(message="Campo requerido"),Regexp(descripcion_reguex,message ='La descripción de la imagen debe tener mínimo 15 caracteres y máximo 250')],render_kw={"placeholder": "Coloca la descripción de tu imagen aquí", "class":"form-control", "style":"color: #1f1f1f"})
    privacidad = RadioField('Privacidad', choices=['Privada','Publica'], validators=[InputRequired(message="Campo requerido")],default='Privada')
    # Privacidad = BooleanField('Imagen Privada', [DataRequired(message="Campo requerido"), "class":"form-control"})
    file2= FileField('Image File')
    crearImagen2 = SubmitField('Guardar',render_kw={"class":"btn btn-defeault btn-send"})

class formEliminarImagen(FlaskForm):
    eliminar = SubmitField('Eliminar',render_kw={"class":"btn btn-defeault btn-send"})  

class formBuscarImagen(FlaskForm):
    busqueda = TextField('Buscar',render_kw={"class":"form-control form-text", "maxlength":"128", "placeholder":"Buscar", "size":"15"})
    botonBuscar = SubmitField('Buscar',render_kw={"class":"btn btn-primary"})