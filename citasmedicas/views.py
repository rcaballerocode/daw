import socket

from builtins import print
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from citasmedicas.decorators import logout_required
from django.db.models import Sum, Max
from django.views import generic
from citasmedicas import models as m

# Create your views here.
# login
@logout_required
def cuenta_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            host_name = "-"
            host_ip = "-"
            try:
                host_name = socket.gethostname()
                host_ip = socket.gethostbyname(host_name)
            except:
                print("Unable to get Hostname and IP")
            messages.success(request, 'Inicio de sesion correcto!')
            return redirect('citasmedicas:ver.pacientes')

        else:
            messages.error(request, '¡Credenciales inválidas!')
            return redirect('citasmedicas:login')

    return render(request, 'citasmedicas/login.html')

# salir
@login_required
def cuenta_logout(request):
    logout(request)
    return redirect("citasmedicas:login")

def formatear_fecha(fecha):
    ## INPUT: 01/10/2019 -- OUTPUT: 2019-10-01
    if fecha == "":
        return "2100-01-01"
    return fecha[6:] + '-' + fecha[3:5] + '-' + fecha[:2]

def numero_to_string(numero):
    if numero == "":
        return "99999"
    return "{:05d}".format(int(numero))

def extraer_anyo(fecha):
    return int(fecha[:4])

@login_required
def ver_medicos(request):
    if request.method == "POST":
        context = {}
        return render(request, 'citasmedicas/Admin/listado_medicos.html', context)

    else:
        lista_medicos = m.medico.objects.all()
        context = {"lista": lista_medicos}
        return render(request, 'citasmedicas/Admin/listado_medicos.html', context)

@login_required
def ver_pacientes(request):
    if request.method == "POST":
        context = {}
        return render(request, 'citasmedicas/Admin/listado_pacientes.html', context)

    else:
        lista_pacientes = m.paciente.objects.all()
        context = {"lista": lista_pacientes}
        return render(request, 'citasmedicas/Admin/listado_pacientes.html', context)

@login_required
def ver_especialidades(request):
    if request.method == "POST":
        context = {}
        return render(request, 'citasmedicas/Admin/listado_especialidades.html', context)

    else:
        lista_especialidades = m.especialidad.objects.all()
        context = {"lista": lista_especialidades}
        return render(request, 'citasmedicas/Admin/listado_especialidades.html', context)

@login_required
def ver_citasmedicas(request):
    if request.method == "POST":
        context = {}
        return render(request, 'citasmedicas/Admin/listado_citasmedicas.html', context)

    else:
        lista_citasmedicas = m.cita.objects.all()
        context = {"lista": lista_citasmedicas}
        return render(request, 'citasmedicas/Admin/listado_citasmedicas.html', context)

@login_required
def registro_paciente(request):
    if request.method == "POST":
        paciente_dni = request.POST.get("paciente_dni")
        paciente_nombres = request.POST.get("paciente_nombres")
        paciente_appaterno = request.POST.get("paciente_appaterno")
        paciente_apmaterno = request.POST.get("paciente_apmaterno")
        paciente_telefono = request.POST.get("paciente_telefono")
 
        ## Verificando la no existencia del registro
        existe = m.paciente.objects.filter(paciente_dni=paciente_dni).exists()

        ## Insertando registro
        if not existe:
            try:
                paciente_nuevo = m.paciente(paciente_dni=paciente_dni, paciente_nombres=paciente_nombres,
                                          paciente_appaterno=paciente_appaterno, paciente_apmaterno=paciente_apmaterno,
                                          paciente_telefono=paciente_telefono)
                paciente_nuevo.save()
            except Exception as e:
                messages.error(request, "No se pudo registrar al paciente!")
                return redirect('citasmedicas:ver.pacientes')

            messages.success(request, "Registro de paciente correcto!")
            return redirect('citasmedicas:ver.pacientes')
        else:
            messages.error(request, "Ya existe un paciente con el Nº de DNI " + paciente_dni)
            return redirect('citasmedicas:ver.pacientes')

    # PETICION GET
    context = {}
    return render(request, 'citasmedicas/Admin/registro_paciente.html', context)

@login_required
def registro_medico(request):
    if request.method == "POST":
        medico_nombres = request.POST.get("medico_nombres")
        medico_appaterno = request.POST.get("medico_appaterno")
        medico_apmaterno = request.POST.get("medico_apmaterno")
        especialidad_abrev = request.POST.get("especialidad_abrev")

        especialidad = m.especialidad.objects.get(especialidad_abrev=especialidad_abrev)

 		## Verificando la no existencia del registro
        existe = m.medico.objects.filter(medico_nombres=medico_nombres,medico_appaterno=medico_appaterno,medico_apmaterno=medico_apmaterno).exists()

        ## Insertando registro
        if not existe:
            try:
                medico_nuevo = m.medico(medico_nombres=medico_nombres,medico_appaterno=medico_appaterno,medico_apmaterno=medico_apmaterno, especialidad=especialidad)
                medico_nuevo.save()
            except Exception as e:
                messages.error(request, "No se pudo registrar al medico!")
                return redirect('citasmedicas:ver.medicos')

            messages.success(request, "Registro de medico correcto!")
            return redirect('citasmedicas:ver.medicos')
        else:
            messages.error(request, "Ya existe un medico con esos datos")
            return redirect('citasmedicas:ver.medicos')

    # PETICION GET
    lista_especialidades = m.especialidad.objects.all()
    context = {"lista": lista_especialidades}
    return render(request, 'citasmedicas/Admin/registro_medico.html', context)

@login_required
def registro_especialidad(request):
    if request.method == "POST":
        especialidad_abrev  = request.POST.get("especialidad_abrev")
        especialidad_nombre  = request.POST.get("especialidad_nombre")

        ## Verificando la no existencia del registro
        existe = m.especialidad.objects.filter(especialidad_abrev=especialidad_abrev).exists()

        ## Insertando registro
        if not existe:
            try:
                especialidad_nuevo = m.especialidad(especialidad_abrev=especialidad_abrev,especialidad_nombre=especialidad_nombre)
                especialidad_nuevo.save()
            except Exception as e:
                messages.error(request, "No se pudo registrar la especialidad!")
                return redirect('citasmedicas:ver.especialidades')

            messages.success(request, "Registro de especialidad correcto!")
            return redirect('citasmedicas:ver.especialidades')
        else:
            messages.error(request, "Ya existe una especialidad con esa abreviatura")
            return redirect('citasmedicas:ver.especialidades')

    # PETICION GET
    context = {}
    return render(request, 'citasmedicas/Admin/registro_especialidad.html', context)

@login_required
def registro_citamedica(request):
    if request.method == "POST":
        cita_fecha = formatear_fecha(request.POST.get("cita_fecha"))
        cita_hora = request.POST.get("cita_hora")
        paciente_ak = request.POST.get("paciente_ak")
        medico_ak = request.POST.get("medico_ak")

        paciente = m.paciente.objects.get(paciente_ak=paciente_ak)
        medico = m.medico.objects.get(medico_ak=medico_ak)

        try:
            cita_nuevo = m.cita(cita_fecha=cita_fecha,cita_hora=cita_hora,paciente=paciente,medico=medico)
            cita_nuevo.save()
        except Exception as e:
            messages.error(request, "No se pudo registrar la cita medica!")
            return redirect('citasmedicas:ver.citasmedicas')

        messages.success(request, "Registro de cita correcto!")
        return redirect('citasmedicas:ver.citasmedicas')
 
    # PETICION GET
    lista_pacientes = m.paciente.objects.all()
    lista_medicos = m.medico.objects.all()
    context = {"lista_pacientes": lista_pacientes, "lista_medicos": lista_medicos}
    return render(request, 'citasmedicas/Admin/registro_citamedica.html', context)