from django.db import models

# Create your models here.

class paciente(models.Model):
	paciente_ak = models.AutoField(primary_key=True)
	paciente_dni = models.CharField(max_length=8)
	paciente_nombres = models.CharField(max_length=50)
	paciente_appaterno = models.CharField(max_length=50)
	paciente_apmaterno = models.CharField(max_length=50)
	paciente_telefono = models.IntegerField()

	def __str__(self):
		return f"{self.paciente_dni} - {self.paciente_nombres} {self.paciente_appaterno} {self.paciente_apmaterno}"

	def get_fullname(self):
		return f"{self.paciente_appaterno} {self.paciente_apmaterno}, {self.paciente_nombres}"

	class Meta:
		db_table = 'paciente'


class especialidad(models.Model):
	especialidad_ak = models.AutoField(primary_key=True)
	especialidad_nombre = models.CharField(max_length=50)
	especialidad_abrev = models.CharField(max_length=7)

	def __str__(self):
		return f"{self.especialidad_abrev}: {self.especialidad_nombre}"

	class Meta:
		db_table = 'especialidad'


class medico(models.Model):
	medico_ak = models.AutoField(primary_key=True)
	medico_nombres = models.CharField(max_length=50)
	medico_appaterno = models.CharField(max_length=50)
	medico_apmaterno = models.CharField(max_length=50)
	especialidad = models.ForeignKey(especialidad, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.medico_nombres} {self.medico_appaterno} {self.medico_apmaterno}"

	def get_description(self):
		return f"{self.medico_appaterno} {self.medico_apmaterno}, {self.medico_nombres} - {self.especialidad.especialidad_nombre}"

	def get_fullname(self):
		return f"{self.medico_appaterno} {self.medico_apmaterno}, {self.medico_nombres}"

	class Meta:
		db_table = 'medico'


class horario(models.Model):
	horario_ak = models.AutoField(primary_key=True)
	horario_dia = models.CharField(max_length=15)
	horario_ingreso = models.TimeField()
	horario_salida = models.TimeField()
	medico = models.ForeignKey(medico, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.medico}, {self.horario_dia} de {self.horario_ingreso} a {self.horario_salida}"

	class Meta:
		db_table = 'horario'


class cita(models.Model):
	cita_ak = models.AutoField(primary_key=True)
	cita_fecha = models.DateField()
	cita_hora = models.TimeField()
	paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
	medico = models.ForeignKey(medico, on_delete=models.CASCADE)

	def __str__(self):
		return f"PACIENTE: {self.paciente}, DIA: {self.cita_fecha} {self.cita_hora}, MEDICO: {self.medico}"

	def fecha(self):
		return self.cita_fecha.strftime('%d/%m/%Y')

	def hora(self):
		return self.cita_hora.strftime('%r')

	class Meta:
		db_table = 'cita'