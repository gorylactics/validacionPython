from django.shortcuts import render , redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    if request.method  == 'GET':
        contexto = {'titulo' : 'Login/Registro'}
        return render(request , 'index.html' , contexto)

def registrar(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method  == 'POST':
        errores = User.objects.validacion(request.POST)
        if len(errores) > 0:
            for key , value in errores.items():
                messages.warning(request , value)
            request.session['user_first_name'] = request.POST['first_name']
            request.session['user_last_name'] = request.POST['last_name']
            request.session['user_email'] = request.POST['email']
            request.session['user_password'] = request.POST['password']
            request.session['user_password_confirm'] = request.POST['password_confirm']
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
            del request.session['user_first_name'] 
            del request.session['user_flast_name'] 
            del request.session['user_email'] 
            del request.session['user_password'] 
            del request.session['user_password_confirm'] 
            return redirect('/success/')

def login(request):
    if request.method == 'GET':
        return redirect('/')
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
                del request.session['user_email_login']
                del request.session['user_password_login']
                return redirect('/success/')
            else:
                messages.warning(request ,'Contraseña Invalida')
                request.session['user_email_login'] = request.POST['email']
                request.session['user_password_login'] = request.POST['password']
                return redirect('/')
        else:
            messages.warning(request ,'Correo Invalido')
            request.session['user_email_login'] = request.POST['email']
            request.session['user_password_login'] = request.POST['password']
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