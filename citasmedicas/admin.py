from django.contrib import admin
from citasmedicas import models

# Register your models here.
admin.site.register(models.paciente)
admin.site.register(models.especialidad)
admin.site.register(models.medico)
admin.site.register(models.horario)
admin.site.register(models.cita)

