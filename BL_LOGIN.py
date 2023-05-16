from tkinter import *
import tkinter as tk
from tkinter import messagebox
import mysql.connector


try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="valudbd"
    )
except mysql.connector.Error as e:
    messagebox.showerror("Error de conexión",
                         f"No se pudo conectar a la base de datos: {e}")
    exit()


# 	LEER USUARIOS DE LA BD

def leer_usuarioDB():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# CREAR VENTANA 1

ventana = tk.Tk()
ventana.title("BASQUET LIVE")
ventana.geometry("280x450+300+250")

color = '#c5e2f6'
ventana['bg'] = color


# CREAR WIDGETS VENTANA 1

Label(ventana, bg=color, text="Login").pack()

Label(ventana, text="Usuario : ", bg=color).pack()
login_usuario = Entry(ventana)
login_usuario.pack()

Label(ventana, text="Contraseña : ", bg=color).pack()
login_contraseña = Entry(ventana, show="*")
login_contraseña.pack()


# LOGIN

def login():
    usuario = login_usuario.get()
    contr = login_contraseña.get()
    cursor = db.cursor()
    cursor.execute("SELECT contrasenia FROM users WHERE usuario='" +
                   usuario+"' and contrasenia='"+contr+"'")

    if cursor.fetchall():
        messagebox.showinfo(title="Login Correcto",
                            message="Usuario y contraseña correctos")
    else:
        messagebox.showerror(title="Login incorrecto",
                             message="Usuario o contraseña incorrecto")


def nuevaVentana():

    newVentana = tk.Toplevel(ventana)
    newVentana.title("BASQUET LIVE")
    newVentana.geometry("300x290+800+250")
    newVentana['bg'] = color

    # CREAR WIDGETS VENTANA 2

    labeExample = tk.Label(newVentana, text="Registro : ").pack

    Label(newVentana, text="Nombre : ").pack()
    entrada_nombre = Entry(newVentana)
    entrada_nombre.pack()

    Label(newVentana, text="Apellidos : ").pack()
    entrada_apellido = Entry(newVentana)
    entrada_apellido.pack()

    Label(newVentana, text="Usuario : ").pack()
    entrada_usuario = Entry(newVentana)
    entrada_usuario.pack()

    Label(newVentana, text="Contraseña : ").pack() 
    entrada_contraseña = Entry(newVentana, show="*")
    entrada_contraseña.pack()

    Label(newVentana, text="Repita la Contraseña : ").pack()
    repetir_contraseña = Entry(newVentana, show="*")
    repetir_contraseña.pack()

    def agregar_usuarioDB(nombre, apellido, usuario, contrasenia):
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (nombre, apellido, usuario, contrasenia) VALUES (%s, %s, %s, %s)",
                           (nombre, apellido, usuario, contrasenia))
            db.commit()

        except mysql.connector.Error as error:
            messagebox.showerror("Error al agregar el usuario",
                                 f"No se pudo agregar el usuario: {error}")
        finally:
            cursor.close

    def agregar_user():

        cursor = db.cursor()

        # OBTENER DATOS DEL USER

        Nombre = entrada_nombre.get()
        Apellido = entrada_apellido.get()
        Usr_reg = entrada_usuario.get()
        Contra_reg = entrada_contraseña.get()
        Contra_reg_2 = repetir_contraseña.get()

        # VALIDAR NULL

        if not Nombre or not Apellido or not Usr_reg or not Contra_reg or not Contra_reg_2:
            messagebox.showerror("Error al agregar el usuario",
                                 "Por favor ingrese todos los datos del usuario")
            return

        # VALIDAR QUE LA CONTRA CON LA REPETICION SEAN IGUALES

        if (Contra_reg == Contra_reg_2):

            cursor.execute("INSERT INTO users (nombre, apellido, usuario, contrasenia) VALUES (%s, %s, %s, %s)",
                           (Nombre, Apellido, Usr_reg, Contra_reg))
            db.commit()
            messagebox.showinfo(title="Registro Correcto", message="Hola " +
                                Nombre+" "+Apellido+" ¡¡ \nSu registro fue exitoso.")
            newVentana.destroy()
        else:
            messagebox.showerror(title="Contraseña Incorrecta",
                                 message="Error¡¡¡ \nLas contraseñas no coinciden.")
            entrada_contraseña.delete(0, END)
            repetir_contraseña.delete(0, END)

        # 	AGREGAR EL NUEVO USUARIO

        agregar_usuarioDB(Nombre, Apellido, Usr_reg, Contra_reg)

        

    buttons = tk.Button(newVentana, text="Registrar ¡",
                        command=agregar_user, bg=color).pack(side="bottom")


Label(ventana, text=" ", bg=color).pack()
Button(text=" ENTRAR ", command=login, bg='#a6d4f2').pack()
Label(ventana, text=" ", bg=color).pack()
Label(ventana, text="No tienes una cuenta ? : ", bg=color).pack()
boton1 = Button(ventana, text="REGISTRO", bg='#a6d4f2',
                command=nuevaVentana).pack()


ventana.mainloop()
