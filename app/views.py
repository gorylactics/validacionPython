from django.shortcuts import render , redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    if request.method  == 'GET':
        contexto = {'titulo' : 'Login/Registro'}
        # dependiendo de si la sesion exite muestra el index o una pag nueva como un muro dentro de la misma direccion raiz
        # if sesion:
        #     render(request, paginaprincipalnueva.html , contexto)
        # else:
        #     return render(request , 'index.html' , contexto)
        return render(request , 'index.html' , contexto)

def registrar(request):
    if request.method  == 'POST':
        errores = User.objects.validacion(request.POST)
        if len(errores) > 0:
            for key , value in errores.items():
                messages.warning(request , value)
            return redirect('/')
        else:
            encriptacion = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = encriptacion,
                
            )
            sesion_de_usuario = {
                    'id' : user.id,
                    'nombre' : user.first_name,
                    'apellido' : user.last_name,
                    'email' : user.email
                    # aca no se puede guardar un objeto completo , hay que separarlo por partes para que pueda ser tomado
                }
            request.session['usuario'] = sesion_de_usuario
            messages.success(request ,'Usuario registrado')
            return redirect('/success/')

def log(request):
    if request.method  == 'POST':
        user = User.objects.filter(email = request.POST['email'])
        if user:
            user_logeado = user[0]
            if bcrypt.checkpw(request.POST['password'].encode() , user_logeado.password.encode()):
                sesion_de_usuario = {
                    'id' : user_logeado.id,
                    'nombre' : user_logeado.first_name,
                    'apellido' : user_logeado.last_name,
                    'email' : user_logeado.email
                    # aca no se puede guardar un objeto completo , hay que separarlo por partes para que pueda ser tomado
                }
                request.session['usuario'] = sesion_de_usuario
                return redirect('/success/')
            else:
                messages.warning(request ,'Contraseña Invalida')
                return redirect('/')
        else:
            messages.warning(request ,'Correo Invalido')
            return redirect('/')

def success(request):
    if 'usuario' in request.session:
        contexto = {
            'titulo': 'Exito',
        }
        return render(request , 'success.html' ,contexto)
    else:
        return redirect('/')

def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
        return redirect('/')
    else:
        return redirect('/')