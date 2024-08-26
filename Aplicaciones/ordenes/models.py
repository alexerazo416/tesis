from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


class Usuario(models.Model):
    username = models.CharField(max_length=150, unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    ci_us = models.CharField(max_length=13, null=True)
    last_login = models.DateTimeField(blank=True, null=True)  # Añadir este campo
    ADMINISTRADOR = 'ADMINISTRADOR'
    MECANICO = 'MECANICO'
    ROLES = [
        (ADMINISTRADOR, 'Administrador'),
        (MECANICO, 'Mecánico'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES)
    is_active = models.BooleanField(default=True)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.username})"
    def get_email_field_name(self):
        return 'email'


class Categoria(models.Model):
    id_cat = models.AutoField(primary_key=True)
    tipo_cat = models.CharField(max_length=100, null=True)


class Producto(models.Model):
    id_pro = models.CharField(max_length=13,primary_key=True)
    nombre_pro = models.CharField(max_length=300, null=True)
    cantidad_pro = models.FloatField()
    descripcion_pro = models.CharField(max_length=3000, null=True)
    ftprodu = models.FileField(upload_to='producto',null=True,blank=True)
    fkcategoria = models.ForeignKey(Categoria,null=True,blank=True,on_delete=models.PROTECT)


class Clientes(models.Model):
    id_cli = models.CharField(max_length=13,primary_key=True)
    nombre_cli = models.CharField(max_length=50)
    apellido_cli = models.CharField(max_length=50,null=True )
    correo_cli = models.CharField(max_length=50)
    direccion_cli = models.CharField(max_length=200)
    estatura_cli=models.CharField(max_length=13,null =True)
    fono = models.CharField(max_length=13,null =True)
    is_deleted = models.BooleanField(default=False)  # Campo para eliminación lógica
    def restaurar(self):
        self.is_deleted = False
        self.save()

    def eliminar_logicamente(self):
        self.is_deleted = True
        self.save()


class Bicicleta(models.Model):
    id_bic = models.CharField(max_length=20,primary_key=True)
    color_bic = models.CharField(max_length=200,null=True)
    marca_bic = models.CharField(max_length=200,null=True)
    descripcion_bic = models.TextField()
    tipo_bic = models.CharField(max_length=300,null=True)
    accesorios_bic = models.CharField(max_length=3000,null=True)
    grupo_bic = models.CharField(max_length=100,null=True)
    talla_bic = models.CharField(max_length=100,null=True)
    fotografia = models.FileField(upload_to='bicicleta',null=True,blank=True)
    cliente=models.ForeignKey(Clientes,null=True,blank=True,on_delete=models.PROTECT)
    is_deleted = models.BooleanField(default=False)  # Campo para eliminación lógica
    def eliminar_logicamente(self):
        self.is_deleted = True
        self.save()

    def restaurar(self):
        self.is_deleted = False
        self.save()



class Mecanico(models.Model):
    id_mec = models.CharField(max_length=13,primary_key=True)
    nombre_mec = models.CharField(max_length=40)
    correo_mec = models.CharField(max_length=40)
    direc_mec = models.CharField(max_length=300)
    expdf_mec = models.FileField(upload_to='pdfsmecanicos',null=True,blank=True)
    fkusuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.PROTECT)


class Repuesto(models.Model):
    id_rep = models.CharField(max_length=20,primary_key=True)
    nombre_rep = models.CharField(max_length=255,null=True)
    precio_rep = models.CharField(max_length=7,null=True)
    proveedor_rep = models.CharField(max_length=200,null=True)
    marca_rep = models.CharField(max_length=50,null=True)
    descripcion_rep = models.TextField()
    cantidad = models.IntegerField(default=1)



class Orden(models.Model):
    id_ord = models.AutoField(primary_key=True)
    descripcion_ord = models.TextField()
    fecha_ord = models.DateField(null=True)
    bicicleta = models.ForeignKey(Bicicleta,null=True,blank=True,on_delete=models.PROTECT)
    mecanico = models.ForeignKey(Mecanico,null=True,blank=True,on_delete=models.PROTECT)
    fkusuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.PROTECT)

class Detalle(models.Model):
    id_det = models.AutoField(primary_key=True)
    entrega_det = models.DateField(null=True)
    metodoPago_det = models.CharField(max_length=100, null=True)
    estado_det = models.CharField(max_length=100, null=True)
    total_det = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    fkrepuestos = models.ManyToManyField(Repuesto, blank=True)
    orden = models.ForeignKey(Orden, null=True, blank=True, on_delete=models.PROTECT)

    def detalles_completos(self):
        return all([
            self.entrega_det,
            self.metodoPago_det,
            self.estado_det,
            self.total_det,
            self.fkrepuestos.exists()
        ])

class Orden_Detalle(models.Model):
    fkdetalle = models.ForeignKey(Detalle, on_delete=models.PROTECT)
    fkorden = models.ForeignKey(Orden, on_delete=models.PROTECT)
