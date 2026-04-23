from django.db import models


# 1. Entidad SERVICIO (Nos da el Many-to-Many)
class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    duracion_minutos = models.PositiveIntegerField(default=30)
    precio = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nombre


# 2. Entidad PROFESIONAL
class Profesional(models.Model):
    ESTADOS = (
        ('ACTIVO', 'Activo'),
        ('BAJA', 'De Baja'),
        ('VACACIONES', 'En Vacaciones'),
    )

    dni = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    especialidad = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ACTIVO')

    # RELACIÓN MANY-TO-MANY: Un profesional ofrece varios servicios y viceversa.
    servicios = models.ManyToManyField(Servicio, related_name='profesionales')

    def __str__(self):
        return f"{self.nombre} {self.apellidos} - {self.especialidad}"


# 3. Entidad CLIENTE
class Cliente(models.Model):
    dni = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


# 4. Entidad DISPONIBILIDAD (Horarios del profesional)
class Disponibilidad(models.Model):
    DIAS_SEMANA = (
        ('LUNES', 'Lunes'), ('MARTES', 'Martes'), ('MIERCOLES', 'Miércoles'),
        ('JUEVES', 'Jueves'), ('VIERNES', 'Viernes'), ('SABADO', 'Sábado'), ('DOMINGO', 'Domingo')
    )

    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name='disponibilidades')
    dia_semana = models.CharField(max_length=10, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.profesional.nombre} - {self.dia_semana} ({self.hora_inicio} a {self.hora_fin})"


# 5. Entidad CITA (El centro del proyecto)
class Cita(models.Model):
    ESTADOS_CITA = (
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('REALIZADA', 'Realizada'),
    )

    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS_CITA, default='PENDIENTE')
    observaciones = models.TextField(blank=True, null=True)

    # RELACIONES FOREIGN KEY (Uno a Muchos)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='citas')
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name='citas')
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True, related_name='citas')

    def __str__(self):
        return f"Cita {self.fecha} {self.hora_inicio} - {self.cliente.nombre} con {self.profesional.nombre}"
