from django.urls import path

from . import views

app_name = 'citasmedicas'

urlpatterns = [
    # login & logout
    path('', views.cuenta_login, name='login'),
    path('logout', views.cuenta_logout, name='logout'),

    path('registro-paciente', views.registro_paciente, name='registro.paciente'),
    path('ver-pacientes', views.ver_pacientes, name='ver.pacientes'),

    path('registro-medico', views.registro_medico, name='registro.medico'),
    path('ver-medicos', views.ver_medicos, name='ver.medicos'),

    path('registro-especialidad', views.registro_especialidad, name='registro.especialidad'),
    path('ver-especialidades', views.ver_especialidades, name='ver.especialidades'),

    path('registro-citamedica', views.registro_citamedica, name='registro.citamedica'),
    path('ver-citasmedicas', views.ver_citasmedicas, name='ver.citasmedicas'),
]