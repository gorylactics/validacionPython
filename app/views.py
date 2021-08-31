from django.shortcuts import render , redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    if request.method  == 'GET':
        contexto = {
            'titulo' : 'Login/Registro  ',
        }
        return render(request , 'index.html' , contexto)
    if request.method  == 'POST':
        errores = User.objects.validacion(request.POST)
        if len(errores) > 0:
            print(errores)
            for key , value in errores.items():
                messages.warning(request , value)
            print(request.POST)
            return redirect('/')
        else:
            print(request.POST)
            encriptacion = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = encriptacion,
            )
            print('el pasword sin encriptar es:'+' '+request.POST['password'])
            print('el password encriptado es:' +' '+  encriptacion)
            return redirect('/success')

def success(request):
    contexto = {
        'titulo': 'Exito'
    }
    return render(request , 'success.html')