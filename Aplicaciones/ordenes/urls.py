from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler404
from . import views

# Configura el manejador de error 404
handler404 = views.error_404


urlpatterns=[
path('',views.verIndex,name="index"),
path('productos',views.verProducto,name="productos"),
# Vista de Repuestos
path('verRepuesto',views.verRepuesto, name='verRepuesto'),
path('guardarRepuesto/',views.guardarRepuesto),
path('eliminarRepuesto/<id_rep>', views.eliminarRepuesto, name='eliminarRepuesto'),

path('editarRepuesto/<id_rep>',views.editarRepuesto),
path('actRepuesto/',views.actRepuesto),
path('eliminarRepuesto/<id_rep>',views.eliminarRepuesto),
path('agRepuesto',views.agRepuesto,name="agRepuesto"),

#---------------Clientes--------------------
path('clientes',views.verClientes,name="clientes"),
path('guardarCliente/',views.guardarCliente),
path('eliminarCliente/<id_cli>',views.eliminarCliente),
path('editarCliente/<id_cli>',views.editarCliente),
path('actCliente/',views.actCliente),
path('agCliente',views.agCliente,name="agCliente"),

#---------------------Mecanicos------------
path('mecanicos',views.verMecanico,name="mecanicos"),
path('guardarMecanico/',views.guardarMecanico),
path('eliminarMecanico/<id_mec>',views.eliminarMecanico),
path('agMecanico',views.agMecanico,name="agMecanico"),
 path('editar_mecanicos/', views.editar_mecanicos, name='editar_mecanicos'),
path('editar_mecanico/<int:mecanico_id>/', views.actMecanico, name='editar_mecanico'),

#---------------------Ordenes--------------------
path('ordenes',views.verOrdenes,name="ordenes"),
path('guardarOrden/',views.guardarOrden),
path('eliminarOrden/<id_ord>',views.eliminarOrden),
path('editarOrden/<id_ord>',views.editarOrden),
path('actOrden/',views.actOrden),
path('agOrden',views.agOrden,name="agOrden"),


# ---------------BICICLETAS------------------------
path('verBicicletas',views.verBicicletas,name="verBicicletas"),
path('guardarBicicleta/',views.guardarBicicleta),
path('eliminarBicicleta/<id_bic>',views.eliminarBicicleta),
path('editarBicicleta/<id_bic>',views.editarBicicleta),
path('procesarActualizacionBicicleta/',views.procesarActualizacionBicicleta),
path('agBicicleta',views.agBicicleta,name="agBicicleta"),

# -----------------DETALLES--------------------------------

path('guardarDetalle/',views.guardarDetalle),
path('eliminarDetalle/<id_det>',views.eliminarDetalle),
path('editarDetalle/<id_det>',views.editarDetalle),
path('procesarActualizacionDetalle/',views.procesarActualizacionDetalle),
path('agDetalle/',views.agDetalle, name= 'agDetalle'),
path('verDetalles/',views.verDetalles, name= 'verDetalles'),


# -----------------Productos---------------------------------
path('productos',views.verProducto,name="productos"),
path('productosadmin',views.verlisProductos,name="productosadmin"),
path('guardarProducto/',views.guardarProducto),
path('eliminarProducto/<id_pro>',views.eliminarProducto),
path('editarProducto/<id_pro>',views.editarProducto),
path('actProducto/',views.actProducto),
path('agProducto',views.agProducto,name="agProducto"),

#--------------------Categorias-------------------
path('categorias',views.verCategoria,name="categorias"),
path('guardarCategoria/',views.guardarCategoria),
path('eliminarCategoria/<id_cat>',views.eliminarCategoria),
path('editarCategoria/<id_cat>',views.editarCategoria),
path('actCategoria/',views.actCategoria),
path('agCategoria',views.agCategoria,name="agCategoria"),

#Modal de ventas de productos en especificos
 path('obtenerProducto/<int:id_pro>/', obtener_producto, name='obtener_producto'),
 path('calendario',views.vista_calendario,name="calendario"),
 #



#--------------------Usuarios-------------------
path('usuarios',views.verUsuarios,name="usuarios"),
path('guardarUsuario/',views.guardarUsuario),
path('editarUsuario/<id_us>',views.editarUsuario),
path('actUsuario/',views.actUsuario),




#-----------------ver estado de la bici desde la pag web------
 path('estado/', verEstadobici, name='estado'),


#Login por tipo de usuario
 path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('403/', views.permission_denied_view, name='permission_denied'),
    path('clientes/', views.verClientes, name='clientes'),
    path('ordenes/', views.verOrdenes, name='ordenes'),



#Menu inicio despues del login Admin
path('menuadmin',views.menuAdmin,name="menuadmin"),

#Reportes de ordenes
path('reporte/<int:orden_id>/', detalle_orden, name='detalle_orden'),


path('plant',views.verPlan,name="plant"),

 path('lista_ordenes/', views.lista_ordenes, name='lista_ordenes'),

 path('productos/<str:producto_id>/', views.detalle_producto, name='detalle_producto'),



]
