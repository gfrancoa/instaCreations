from db import get_db,close_db
from flask import flash

#REGISTRO Y ACTIVACIÓN
def sql_nuevo_usuario(nombreUsuario,correo,contrasena):
    db = get_db()
    #strsql = "INSERT INTO usuario (nombreUsuario, correo, contrasena,activo) VALUES ('"+nombreUsuario +"', '"+correo+"', '"+contrasena+"',0)"
    #db.execute(strsql)
    strsql = 'INSERT INTO usuario (nombreUsuario, correo, contrasena,activo) VALUES (?,?,?,?)'
    db.execute(strsql,(nombreUsuario,correo,contrasena,"0"))
    db.commit()
    close_db()
    return "Usuario creado"

def sql_usuario_activo(nombreUsuario):
    strsql = 'SELECT activo FROM usuario WHERE nombreUsuario = ?'
    db = get_db()
    activo = db.execute(strsql,(nombreUsuario,)).fetchone()[0]
    close_db()
    return activo

def sql_activar_usuario(nombreUsuario):
    if sql_usuario_activo(nombreUsuario) == 0:
        strsql = 'UPDATE usuario SET activo = 1 WHERE nombreUsuario = ?'
        db = get_db()
        db.execute(strsql,(nombreUsuario,))
        db.commit()
        close_db()
        return flash("Cuenta activada")
    elif sql_usuario_activo(nombreUsuario)== 1:
        return flash("El usuario ya se encuentra activo. Por favor inicie sesión")


# LEER IMÁGENES 
def sql_leer_imagenes_propias(nombreUsuario):
    db = get_db()
    strsql = 'SELECT id FROM usuario WHERE nombreUsuario = ?'
    id = db.execute(strsql,(nombreUsuario,)).fetchone()[0]
    strsql2 = 'SELECT nombre, descripcion, imagen,id FROM imagenes WHERE id_usuario = ?'
    imagenes = db.execute(strsql2,(str(id),)).fetchall()
    #print("IMAGEN LEER IMGS PROPIAS: " + str(imagenes[0][3]))
    close_db()
    return imagenes

def sql_leer_imagenes_publicas():
    db = get_db()
    strsql = 'SELECT * FROM imagenes WHERE privado = ?'
    temp1 = "0"
    imagenes_publicas = db.execute(strsql,(temp1,)).fetchall()
    close_db()
    #print("IMAGEN LEER IMG PUBLICAS: " + imagenes_publicas[2][0])
    return imagenes_publicas

def sql_buscar_imagenes(texto_busqueda):
    db = get_db()
    strsql = "SELECT * FROM imagenes WHERE nombre LIKE ('%' || ? || '%') OR descripcion LIKE ('%' || ? || '%')"
    resultado_imagenes = db.execute(strsql,(texto_busqueda,texto_busqueda)).fetchall()
    close_db()
    return resultado_imagenes

def sql_leer_imagen_propia(idImagen):
    db = get_db()
    strsql = 'SELECT nombre, descripcion, imagen FROM imagenes WHERE id = ?'
    imagen = db.execute(strsql,(idImagen,)).fetchone()
    return imagen 

# INICIAR SESION
def sql_iniciar_sesion(nombreUsuario):
    #strsql = 'SELECT id FROM usuario WHERE nombreUsuario = ? AND contrasena = ? AND activo = ?;'
    strsql = 'SELECT * FROM usuario WHERE nombreUsuario = ?'
    db = get_db()
    resultado = db.execute(strsql,(nombreUsuario,)).fetchone()
    close_db()
    return resultado


#RESTABLECER CONTRASEÑA
def sql_restablecer_contrasena(correo):
    strsql = 'SELECT correo FROM usuario WHERE correo = ? and activo= ?; '
    db = get_db()
    resultado = 0
    if db.execute(strsql,(correo,"1")).fetchone() is not None:
        resultado = 1
    close_db()
    return resultado

#CAMBIAR CONTRASEÑA

def sql_cambiar_contrasena(correo, contrasena):
    strsql = 'UPDATE usuario SET contrasena = ?  WHERE correo = ?;'
    db = get_db()
    db.execute(strsql,(contrasena,correo))
    db.commit()
    close_db()
    return flash("Contraseña actualizada")

#EXTRAER ID USUARIO
def sql_id_usuario(NombreUsuario):
    db = get_db()
    strsql = 'SELECT id FROM usuario WHERE nombreUsuario = ?;'
    id = db.execute(strsql,(NombreUsuario,)).fetchone()
    return id

def sql_id_usuario_por_correo(correo):
    db = get_db()
    strsql = 'SELECT id FROM usuario WHERE correo = ?;'
    id = db.execute(strsql,(correo,)).fetchone()
    return id


def sql_leer_usuario(nombreUsuario):
    db = get_db()
    strsql = 'SELECT * FROM usuario WHERE nombreUsuario = ?'
    usuario = db.execute(strsql,(nombreUsuario,)).fetchone()
    return usuario

#EXTRAER ID IMAGEN
def sql_id_imagen(NombreImagen,id_usuario):
    db = get_db()
    strsql = 'SELECT id FROM imagenes WHERE nombre = ? and id_usuario = ?;'
    #REVISAR SI EL ID DEL USUARIO SE PASA g.user['id']
    idImagen = db.execute(strsql,(NombreImagen,str(id_usuario))).fetchone()[0]
    return idImagen

#CREAR IMAGEN
def sql_crear_imagen(NombreUsuario,nombreImagen,descripcion,privado,imagen):
    db = get_db()
    id_usuario = sql_id_usuario(NombreUsuario)[0]
    strsql = 'INSERT INTO IMAGENES(nombre, descripcion, privado, id_usuario, imagen) VALUES (?, ?, ?, ?, ?)'
    db.execute(strsql,(nombreImagen,descripcion,privado,id_usuario,imagen))
    db.commit()
    close_db()
    return print("Se creo con exito la imagen")

#ACTUALIZAR IMAGEN
def sql_actualizar_imagen(NombreUsuario,nombreImagen,descripcion,privado,imagen,idImagen):
    db = get_db()
    id_usuario = sql_id_usuario(NombreUsuario)[0]
    id_imagen = idImagen
    strsql= 'UPDATE IMAGENES SET NOMBRE = ?, DESCRIPCION = ?, PRIVADO = ?, ID_USUARIO = ?, IMAGEN = ? WHERE ID = ?;'
    db.execute(strsql,(nombreImagen,descripcion,privado,id_usuario,imagen,id_imagen))
    db.commit()
    close_db()
    return print("Se actualizo con exito la imagen")

#BORRAR IMAGEN
def sql_eliminar_imagen(idImagen):
    db = get_db()
    strsql= 'DELETE FROM imagenes WHERE ID = ?;'
    db.execute(strsql,(idImagen,))
    db.commit()
    close_db()
    return print("Se elimino con exito la imagen") 
