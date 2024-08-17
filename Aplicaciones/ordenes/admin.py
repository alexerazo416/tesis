from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'nombre', 'apellido', 'telefono', 'rol','password', 'is_active')
    search_fields = ('username', 'email', 'nombre', 'apellido')
    list_filter = ('rol', 'is_active')
    fields = ('username', 'nombre', 'apellido', 'telefono', 'email', 'rol','password','is_active')

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)
