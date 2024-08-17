from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import CustomLoginForm
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db.models import ProtectedError
from .models import Usuario
from django.core.exceptions import PermissionDenied
from .utils import role_required
from django.db.models.deletion import ProtectedError



#------------Ver  el index---------
def verIndex(request):
    return render(request, 'productos/index.html')


#-------------------Repuestos--------------------
@role_required(allowed_roles=['MECANICO','ADMINISTRADOR'])
def verRepuesto(request):
        repuestoBdd=Repuesto.objects.all()
        return render(request, 'repuesto.html',{'repuesto':repuestoBdd})





def guardarRepuesto(request):
    if request.method == 'POST':
        # Obtener y limpiar los datos del formulario
        id_rep = request.POST.get("id_rep", "").strip().upper()
        nombre_rep = request.POST.get("nombre_rep", "").strip().upper()
        precio_rep = request.POST.get("precio_rep", "").strip()  # Aunque no estás validando el precio, también se limpia
        marca_rep = request.POST.get("marca_rep", "").strip().upper()
        descripcion_rep = request.POST.get("descripcion_rep", "").strip().upper()
        proveedor_rep = request.FILES.get("proveedor_rep")
        if Repuesto.objects.filter(id_rep=id_rep).exists() or Repuesto.objects.filter(nombre_rep=nombre_rep).exists():
            messages.error(request, 'El repuesto con el mismo nombre o código ya existe.')
            return redirect('agRepuesto')  # Redirigir al formulario para corregir el error
        nuevoRepuesto = Repuesto.objects.create(
            id_rep=id_rep,
            nombre_rep=nombre_rep,
            precio_rep=precio_rep,
            marca_rep=marca_rep,
            descripcion_rep=descripcion_rep,
            proveedor_rep=proveedor_rep)
        messages.success(request, 'Repuesto guardado exitosamente.')
        return redirect('verRepuesto')  # Redirigir a la vista de repuestos







# Eliminando un registro
@role_required(allowed_roles=['MECANICO','ADMINISTRADOR'])
def eliminarRepuesto(request, id_rep):
    try:
        repuestoEliminar = get_object_or_404(Repuesto, id_rep=id_rep)
        repuestoEliminar.delete()
        messages.success(request, 'Repuesto eliminado correctamente')
    except ProtectedError:
        messages.error(request, 'No se puede eliminar el repuesto porque está vinculado a un detalle.')

    return redirect('/verRepuesto')
@role_required(allowed_roles=['ADMINISTRADOR','MECANICO'])
def editarRepuesto(request, id_rep):
    repuestoEditar=Repuesto.objects.get(id_rep=id_rep)
    return render(request, 'editarRepuesto.html', {'repuesto': repuestoEditar})

@role_required(allowed_roles=['MECANICO','ADMINISTRADOR'])
def actRepuesto(request):
    id_rep=request.POST["id_rep"]
    nombre_rep=request.POST["nombre_rep"].upper()
    precio_rep=request.POST["precio_rep"]
    marca_rep=request.POST["marca_rep"].upper()
    descripcion_rep =request.POST["descripcion_rep"].upper()
    repuestoEditar=Repuesto.objects.get(id_rep=id_rep)
    repuestoEditar.nombre_rep=nombre_rep
    repuestoEditar.precio_rep=precio_rep
    repuestoEditar.marca_rep=marca_rep
    repuestoEditar.descripcion_rep=descripcion_rep
    repuestoEditar.save()
    messages.success(request,
      'Repuesto ACTUALIZADO Exitosamente')
    return redirect('/verRepuesto')

@role_required(allowed_roles=['MECANICO','ADMINISTRADOR'])
def agRepuesto(request):
    repuestoBdd=Repuesto.objects.all()
    return render(request, 'agRepuesto.html',{'repuesto':repuestoBdd})


@receiver(pre_delete, sender=Repuesto)
def protect_repuesto_from_delete(sender, instance, **kwargs):
    if instance.detalle_set.exists():
        raise ProtectedError("No se puede eliminar el repuesto porque está vinculado a un detalle.", instance)

#--------------------Clientes-------------------
@role_required(allowed_roles=['ADMINISTRADOR', 'MECANICO'])
def verClientes(request):
    clientes = Clientes.objects.filter(is_deleted=False)
    return render(request, 'clientes.html', {'clientes': clientes})


@role_required(allowed_roles=['ADMINISTRADOR'])
def agCliente(request):
    clientes=Clientes.objects.all()
    return  render(request, 'agCliente.html',{'clientes':clientes})


def guardarCliente(request):
    if request.method == 'POST':
        id_cli = request.POST["id_cli"]
        nombre_cli = request.POST["nombre_cli"].upper()
        correo_cli = request.POST["correo_cli"].upper()
        direccion_cli = request.POST["direccion_cli"]
        estatura_cli = request.POST["estatura_cli"]
        fono = request.POST["fono"]
        # Buscar cliente activo con la cédula proporcionada
        cliente_existente = Clientes.objects.filter(id_cli=id_cli).first()

        if cliente_existente:
            if cliente_existente.is_deleted:
                # Restaurar cliente eliminado lógicamente
                cliente_existente.nombre_cli = nombre_cli
                cliente_existente.correo_cli = correo_cli
                cliente_existente.direccion_cli = direccion_cli
                cliente_existente.estatura_cli = estatura_cli
                cliente_existente.fono = fono
                cliente_existente.restaurar()
                messages.success(request, 'Cliente restaurado exitosamente.')
            else:
                messages.error(request, 'El cliente ya existe y está activo.')
        else:
            # Crear un nuevo cliente si no existe ninguno con el ID proporcionado
            Clientes.objects.create(
                id_cli=id_cli,
                nombre_cli=nombre_cli,
                correo_cli=correo_cli,
                direccion_cli=direccion_cli,
                estatura_cli=estatura_cli,
                fono=fono)
            messages.success(request, 'Cliente guardado exitosamente.')
        return redirect('clientes')
    messages.error(request, 'Método no permitido')
    return redirect('clientes')


@role_required(allowed_roles=['ADMINISTRADOR'])
def eliminarCliente(request, id_cli):
    try:
        cliEliminar = get_object_or_404(Clientes, id_cli=id_cli)
        if Bicicleta.objects.filter(cliente=cliEliminar).exists():
            messages.error(request, 'No se puede eliminar el cliente porque está asociado a una bicicleta.')
        else:
            # Realizar eliminación lógica
            cliEliminar.eliminar_logicamente()
            messages.success(request, 'Cliente eliminado correctamente')
    except Clientes.DoesNotExist:
        messages.error(request, 'Cliente no encontrado.')
    except ProtectedError:
        messages.error(request, 'No se puede eliminar el cliente porque está vinculado a una orden.')
    return redirect('clientes')



@role_required(allowed_roles=['ADMINISTRADOR'])
def editarCliente(request,id_cli):
    clientes=Clientes.objects.get(id_cli=id_cli)
    return  render(request, 'editarCliente.html',{'clientes':clientes})

@role_required(allowed_roles=['ADMINISTRADOR'])
def actCliente(request):
    if request.method == 'POST':
        id_cli_actual = request.POST["id_cli"]
        nuevo_id_cli = request.POST["nuevo_id_cli"]
        nombre_cli = request.POST["nombre_cli"].upper()
        correo_cli = request.POST["correo_cli"]
        direccion_cli = request.POST["direccion_cli"].upper()
        estatura_cli = request.POST["estatura_cli"]
        fono = request.POST["fono"]
        estatura_cli = estatura_cli.replace(',', '.')
        estatura_cli = float(estatura_cli)

        # Buscar el cliente por su id actual
        try:
            cliEditar = Clientes.objects.get(id_cli=id_cli_actual)
        except Clientes.DoesNotExist:
            messages.error(request, 'Cliente no encontrado.')
            return redirect('clientes')

        # Actualizar los campos del cliente
        cliEditar.id_cli = nuevo_id_cli
        cliEditar.nombre_cli = nombre_cli
        cliEditar.correo_cli = correo_cli
        cliEditar.direccion_cli = direccion_cli
        cliEditar.estatura_cli = estatura_cli
        cliEditar.fono = fono

        # Guardar los cambios
        cliEditar.save()

        messages.success(request, 'Cliente Actualizado Exitosamente')
        return redirect('clientes')
    else:
        messages.error(request, 'Método de solicitud no permitido.')
        return redirect('clientes')





#----------------------------Mecanico---------------
@role_required(allowed_roles=['ADMINISTRADOR'])
def verMecanico(request):
     mecanicos = Usuario.objects.filter(rol=Usuario.MECANICO)
     return  render(request, 'mecanico.html',{'mecanicos':mecanicos})
@role_required
def agMecanico(request):
    user = Usuario.objects.get(id=request.session['user_id'])
    mecanicos=Mecanico.objects.all()
    return  render(request, 'agMecanico.html',{'mecanicos':mecanicos,})


@role_required(allowed_roles=['ADMINISTRADOR'])
def guardarMecanico(request):
    if request.method == 'POST':
        id_mec = request.POST.get("id_mec")
        nombre_mec = request.POST.get("nombre_mec").upper()
        correo_mec = request.POST.get("correo_mec").upper()
        direc_mec = request.POST.get("direc_mec").upper()
        expdf_mec = request.FILES.get("expdf_mec")
        if Mecanico.objects.filter(id_mec=id_mec).exists():
            return JsonResponse({'success': False, 'message': 'El mecánico con este número de cédula ya existe.'})
        nuevoMecanico = Mecanico(
            id_mec=id_mec,
            nombre_mec=nombre_mec,
            correo_mec=correo_mec,
            direc_mec=direc_mec,
            expdf_mec=expdf_mec,
        )
        try:
            nuevoMecanico.save()
            messages.success(request, 'Mecánico guardado exitosamente.')
            return JsonResponse({'success': True})
        except Exception as e:
            messages.error(request, f'Error al guardar el mecánico: {str(e)}')
            return JsonResponse({'success': False, 'message': 'Error al guardar el mecánico.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})



#Eliminar Clientes
@role_required(allowed_roles=['ADMINISTRADOR'])
def eliminarMecanico(request,id_mec):
    mecEliminar=Mecanico.objects.get(id_mec=id_mec)
    mecEliminar.delete()
    messages.success(request,'Mecanico Eliminado Exitosamente')
    return redirect('/mecanicos')


#MECANICOS CON USUARIO

@role_required(allowed_roles=['ADMINISTRADOR'])
def editar_mecanicos(request):
    mecanicos = Usuario.objects.filter(rol=Usuario.MECANICO)
    return render(request, 'editarMecanico.html', {'mecanicos': mecanicos})


@role_required(allowed_roles=['ADMINISTRADOR'])
def actMecanico(request, mecanico_id):
    mecanico = get_object_or_404(Usuario, id=mecanico_id)
    if request.method == 'POST':
        mecanico.username = request.POST['username']
        mecanico.nombre = request.POST['nombre'].upper()
        mecanico.apellido = request.POST['apellido'].upper()
        mecanico.telefono = request.POST['telefono']
        mecanico.email = request.POST['email'].upper()

        # Convertir el valor del formulario a un valor booleano
        is_active_value = request.POST['is_active'].lower() == 'true'
        mecanico.is_active = is_active_value

        if request.POST['password']:
            mecanico.set_password(request.POST['password'])

        mecanico.save()
        messages.success(request, 'Mecanico Actualizado Exitosamente')
        return redirect('mecanicos')

    return render(request, 'editarMecanico.html', {'mecanico': mecanico})




#-----------Ordenes-------------

#visualizar Ordenes

@role_required(allowed_roles=['ADMINISTRADOR','MECANICO'])
def verOrdenes(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user = Usuario.objects.get(id=request.session['user_id'])
    ordenes = Orden.objects.prefetch_related('bicicleta', 'mecanico', 'fkusuario', 'detalle_set__fkrepuestos').all()
    detalles = Detalle.objects.all()

    detalles_dict = {}
    for detalle in detalles:
        if detalle.orden_id not in detalles_dict:
            detalles_dict[detalle.orden_id] = []
        detalles_dict[detalle.orden_id].append(detalle)

    for orden in ordenes:
        orden.detalles = detalles_dict.get(orden.id_ord, [])
        orden.detalles_completos = all(detalle.detalles_completos() for detalle in orden.detalles)

    return render(request, 'ordenes.html', {
        'user': user,
        'ordenes': ordenes,
        'bicis': Bicicleta.objects.all(),
        'mecanicos': Mecanico.objects.all(),
        'detalles': detalles_dict,
    })





@role_required(allowed_roles=['MECANICO', 'ADMINISTRADOR'])
def agOrden(request):
    user = Usuario.objects.get(id=request.session['user_id'])
    ordenes = Orden.objects.all()
    bicis = Bicicleta.objects.filter(is_deleted=False)
    mecanicos = Mecanico.objects.all()
    detalles = Detalle.objects.all()
    return render(request, 'agOrden.html', {'bicis': bicis, 'mecanicos': mecanicos, 'detalles': detalles, 'ordenes': ordenes, 'user': user})





@role_required(allowed_roles=['MECANICO', 'ADMINISTRADOR'])
def guardarOrden(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        id_bic = request.POST.get("id_bic")
        fecha_ord = request.POST.get("fecha_ord")
        descripcion_ord = request.POST.get("descripcion_ord").upper()
        user = Usuario.objects.get(id=user_id)
        # Obtener la bicicleta seleccionada
        obtenerBicicleta = Bicicleta.objects.get(id_bic=id_bic)
        # Crear la nueva orden
        nuevoOrden = Orden.objects.create(
            fecha_ord=fecha_ord,
            descripcion_ord=descripcion_ord,
            mecanico=None,
            bicicleta=obtenerBicicleta,
            fkusuario=user)
        # Crear el detalle con estado "Iniciado"
        Detalle.objects.create(
            id_det=nuevoOrden.id_ord,
            orden=nuevoOrden,
            estado_det="Recibida"   # Establecer el estado en "Iniciado"
        )
        messages.success(request, 'Orden Guardada Exitosamente')
        return redirect('/ordenes')





@role_required(allowed_roles=[ 'ADMINISTRADOR'])
def eliminarOrden(request, id_ord):
    try:
        ordEliminar = Orden.objects.get(id_ord=id_ord)
        detalleEliminar = Detalle.objects.get(orden=ordEliminar)
        detalleEliminar.delete()
        ordEliminar.delete()
        messages.success(request, 'Orden y su detalle asociado eliminados correctamente.')
    except Orden.DoesNotExist:
        messages.error(request, 'La orden no existe.')
    except Detalle.DoesNotExist:
        ordEliminar.delete()  # Si el detalle no existe, eliminamos la orden de todas formas
        messages.success(request, 'Orden eliminada. No se encontró detalle asociado.')
    return redirect('/ordenes')

@role_required(allowed_roles=['MECANICO','ADMINISTRADOR'])
def editarOrden(request,id_ord):
    ordenes = Orden.objects.get(id_ord=id_ord)
    bicis=  Bicicleta.objects.all()
    mecanicos= Mecanico.objects.all()
    repuestos=Repuesto.objects.all()
    return render(request, 'editarOrden.html', {'bicis': bicis,'mecanicos':mecanicos,'repuestos':repuestos,'ordenes':ordenes})

@role_required(allowed_roles=['MECANICO', 'ADMINISTRADOR'])
def actOrden(request):
    id_bic = request.POST["id_bic"]
    obtenerBicicleta = Bicicleta.objects.get(id_bic=id_bic)
    id_ord = request.POST["id_ord"]
    fecha_ord = request.POST["fecha_ord"]
    descripcion_ord = request.POST["descripcion_ord"].upper()
    estado_det = request.POST["estado_det"]

    ordEditar = Orden.objects.get(id_ord=id_ord)
    ordEditar.fecha_ord = fecha_ord
    ordEditar.descripcion_ord = descripcion_ord
    ordEditar.bicicleta = obtenerBicicleta
    ordEditar.save()

    # Actualizar el estado del detalle
    detalleEditar = Detalle.objects.get(orden=ordEditar)
    estado_anterior = detalleEditar.estado_det
    detalleEditar.estado_det = estado_det
    detalleEditar.save()

    # Enviar correo si el estado cambia a "Lista para entregar"
    if estado_anterior != 'List_ent' and estado_det == 'List_ent':
        cliente = detalleEditar.orden.bicicleta.cliente
        send_mail(
            'Tu orden está lista para entregar',
            f'Hola {cliente.nombre_cli},\n\nTu orden con ID {detalleEditar.orden.id_ord} está lista para entregar.\n\nGracias por confiar en nosotros.',
            'ronalmena2020@gmail.com',  # Cambia esto al correo de origen
            [cliente.correo_cli],
            fail_silently=False,
        )

    messages.success(request, 'Orden y Detalle Actualizados Exitosamente')
    return redirect('/ordenes')



# ---------BICICLETAS----------------
@role_required(allowed_roles=['ADMINISTRADOR','MECANICO'])
def verBicicletas(request):
    biciBdd = Bicicleta.objects.filter(is_deleted=False)
    clientes = Clientes.objects.all()
    return render(request, 'bicicleta.html',{'bicicleta': biciBdd, 'cliente': clientes})

@role_required(allowed_roles=['ADMINISTRADOR','MECANICO'])
def agBicicleta(request):
    biciBdd = Bicicleta.objects.all()
    clientes = Clientes.objects.filter(is_deleted=False)
    return render(request, 'agBicicleta.html',{'bicicleta': biciBdd, 'cliente': clientes})
# capturando los valores del formulario por POST
@role_required(allowed_roles=['ADMINISTRADOR','MECANICO'])
def guardarBicicleta(request):
    if request.method == 'POST':
        id_bic = request.POST["id_bic"]
        cli = request.POST["cli"]
        cliSeleccionado = get_object_or_404(Clientes, id_cli=cli)
        color_bic = request.POST["color_bic"].upper()
        marca_bic = request.POST["marca_bic"].upper()
        descripcion_bic = request.POST["descripcion_bic"].upper()
        tipo_bic = request.POST["tipo_bic"].upper()
        fotografia = request.FILES.get("fotografia")
        # Buscar bicicleta existente con el ID proporcionado
        bicicleta_existente = Bicicleta.objects.filter(id_bic=id_bic).first()
        if bicicleta_existente:
            if bicicleta_existente.is_deleted:
                # Restaurar bicicleta eliminada lógicamente
                bicicleta_existente.color_bic = color_bic
                bicicleta_existente.marca_bic = marca_bic
                bicicleta_existente.descripcion_bic = descripcion_bic
                bicicleta_existente.tipo_bic = tipo_bic
                bicicleta_existente.fotografia = fotografia
                bicicleta_existente.cliente = cliSeleccionado
                bicicleta_existente.restaurar()
                messages.success(request, 'Bicicleta restaurada exitosamente.')
            else:
                messages.error(request, 'La bicicleta ya existe y está activa.')
        else:
            # Crear una nueva bicicleta si no existe ninguna con el ID proporcionado
            Bicicleta.objects.create(
                id_bic=id_bic,
                color_bic=color_bic,
                marca_bic=marca_bic,
                descripcion_bic=descripcion_bic,
                tipo_bic=tipo_bic,
                fotografia=fotografia,
                cliente=cliSeleccionado)
            messages.success(request, 'Bicicleta guardada exitosamente.')
        return redirect('/verBicicletas')
    messages.error(request, 'Método no permitido')
    return redirect('/verBicicletas')


@role_required(allowed_roles=['ADMINISTRADOR'])
def eliminarBicicleta(request, id_bic):
    try:
        bicicletaEliminar = get_object_or_404(Bicicleta, id_bic=id_bic)
        # Verificar si la bicicleta ya está eliminada lógicamente
        if bicicletaEliminar.is_deleted:
            messages.warning(request, 'La bicicleta ya está eliminada.')
        else:
            # Intentar realizar eliminación lógica
            bicicletaEliminar.eliminar_logicamente()
            messages.success(request, 'Bicicleta eliminada correctamente.')
    except ProtectedError:
        messages.error(request, 'No se puede eliminar la bicicleta porque está vinculada a una orden.')
    except Bicicleta.DoesNotExist:
        messages.error(request, 'Bicicleta no encontrada.')
    return redirect('/verBicicletas')

@role_required(allowed_roles=['ADMINISTRADOR'])
def editarBicicleta(request, id_bic):
    bicicletaEditar=Bicicleta.objects.get(id_bic=id_bic)
    clientes = Clientes.objects.filter(is_deleted=False)
    return render(request, 'editarBicicleta.html', {'bicicleta': bicicletaEditar, 'cliente': clientes})


@role_required(allowed_roles=['ADMINISTRADOR','MECANICO'])
def procesarActualizacionBicicleta(request):
    id_bic = request.POST["id_bic"]
    cli = request.POST["cli"]
    color_bic = request.POST["color_bic"].upper()
    marca_bic = request.POST["marca_bic"].upper()
    descripcion_bic = request.POST["descripcion_bic"].upper()
    tipo_bic = request.POST["tipo_bic"].upper()
    fotografia = request.FILES.get("fotografia")
    bicicletaEditar = Bicicleta.objects.get(id_bic=id_bic)
    cliSeleccionado = Clientes.objects.get(id_cli=cli)
    bicicletaEditar.cliente = cliSeleccionado
    bicicletaEditar.color_bic = color_bic
    bicicletaEditar.marca_bic = marca_bic
    bicicletaEditar.descripcion_bic = descripcion_bic
    bicicletaEditar.tipo_bic = tipo_bic
    if fotografia:
        bicicletaEditar.fotografia = fotografia
    bicicletaEditar.save()
    messages.success(request, 'Bicicleta actualizada exitosamente')
    return redirect('/verBicicletas')

# ------------------------- DETALLES ----------------------
@role_required(allowed_roles=['MECANICO','ADMINISTRADOR'])
def verDetalles(request):
    detaBdd = Detalle.objects.all()
    ordenes = Orden.objects.all()
    bicletas=Bicicleta.objects.all()
    repuestos=Repuesto.objects.all()
    return render(request, 'detalle.html',{'detalle': detaBdd, 'ordenes': ordenes,'bicletas':bicletas,'repuestos':repuestos})

@role_required(allowed_roles=['MECANICO','ADMINISTRADOR'])
def agDetalle(request):
    detaBdd = Detalle.objects.all()
    ordenes = Orden.objects.all()
    return render(request, 'agDetalle.html',{'detalle': detaBdd, 'orden': ordenes})
    ord = request.POST["ord"]
    ordSeleccionado=Orden.objects.get(id_ord=ord)
    entrega_det=request.POST["entrega_det"]
    metodoPago_det=request.POST["metodoPago_det"]
    estado_det=request.POST["estado_det"]
    total_det=request.POST["total_det"]
    nuevoDetalle=Detalle.objects.create(
    entrega_det=entrega_det,
    metodoPago_det=metodoPago_det,
    estado_det=estado_det,
    total_det=total_det,
    orden=ordSeleccionado)
    messages.success(request, 'Detalle Guardado exitosamente')
    return redirect('/verDetalles')

@role_required(allowed_roles=['MECANICO','ADMINISTRADOR'])
def guardarDetalle(request):
    if request.method == "POST":
        ord = request.POST["ord"]
        entrega_det = request.POST["entrega_det"]
        metodoPago_det = request.POST["metodoPago_det"]
        estado_det = request.POST["estado_det"]
        total_det = request.POST["total_det"]
        #insertando datos mediante el ORM de Django
        nuevoDetalle = Detalle.objects.create(
            entrega_det=entrega_det,
            metodoPago_det=metodoPago_det,
            estado_det=estado_det,
            total_det=total_det,
            orden_id=ord
        )
        messages.success(request, 'Detalle Guardado exitosamente')
        return redirect('/verDetalles')
    return render(request, 'editardetalle.html')
# Eliminando un registro



@role_required(allowed_roles=['MECANICO', 'ADMINISTRADOR'])
def eliminarDetalle(request, id_det):
    try:
        detalleEliminar = get_object_or_404(Detalle, id_det=id_det)
        detalleEliminar.delete()
        messages.success(request, 'Detalle eliminado correctamente.')
    except ProtectedError:
        messages.error(request, 'No se puede eliminar el detalle porque está vinculado a una orden.')
    except Detalle.DoesNotExist:
        messages.error(request, 'Detalle no encontrado.')
    return redirect('/verDetalles')



@role_required(allowed_roles=['MECANICO','ADMINISTRADOR'])
def editarDetalle(request, id_det):
    detalle = get_object_or_404(Detalle, id_det=id_det)
    repuestos = Repuesto.objects.all()
    repuestos_seleccionados = detalle.fkrepuestos.all().values_list('id_rep', flat=True)
    total = sum(float(repuesto.precio_rep) for repuesto in detalle.fkrepuestos.all())
    fecha_ingreso = detalle.orden.fecha_ord
    context = {
        'detalles': detalle,
        'repuestos': repuestos,
        'repuestos_seleccionados': list(repuestos_seleccionados),
        'total': total,
        'fecha_ingreso': fecha_ingreso
    }
    return render(request, 'editarDetalle.html', context)


@role_required(allowed_roles=['MECANICO', 'ADMINISTRADOR'])
def procesarActualizacionDetalle(request):
    id_det = request.POST["id_det"]
    entrega_det = request.POST["entrega_det"]
    metodoPago_det = request.POST["metodoPago_det"]
    estado_det = request.POST["estado_det"]
    id_reps = request.POST.getlist("id_rep")
    id_reps = [id_rep for id_rep in id_reps if id_rep]
    detalleEditar = Detalle.objects.get(id_det=id_det)
    estado_anterior = detalleEditar.estado_det  # Guardar el estado anterior
    detalleEditar.entrega_det = entrega_det
    detalleEditar.metodoPago_det = metodoPago_det
    detalleEditar.estado_det = estado_det
    total = 0
    detalleEditar.fkrepuestos.clear()
    for id_rep in id_reps:
        repuesto = Repuesto.objects.get(id_rep=id_rep)
        cantidad = int(request.POST.get(f"cantidad_{id_rep}", 1))
        total += float(repuesto.precio_rep) * cantidad
        detalleEditar.fkrepuestos.add(repuesto)

    detalleEditar.total_det = total
    detalleEditar.save()

    # Enviar correo si el estado cambia a "Lista para entregar"
    if estado_anterior != 'List_ent' and estado_det == 'List_ent':
        cliente = detalleEditar.orden.bicicleta.cliente
        send_mail(
            'Tu orden está lista para entregar',
            f'Hola {cliente.nombre_cli},\n\nTu orden con ID {detalleEditar.orden.id_ord} está lista para entregar.\n\nGracias por confiar en nosotros.',
            'ronalmena2020@gmail.com',  # Cambia esto al correo de origen
            [cliente.correo_cli],
            fail_silently=False,
        )

    messages.success(request, 'Detalle ACTUALIZADO Exitosamente')
    return redirect('/ordenes')

#-------------------Productos-------------


def verProducto(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'productos/producto.html', {'productos': productos,'categorias':categorias})
@role_required(allowed_roles=['ADMINISTRADOR'])
def verlisProductos(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'verproductos.html', {'productos': productos,'categorias':categorias})


@role_required(allowed_roles=['ADMINISTRADOR'])
def agProducto(request):
    productos=Producto.objects.all()
    categorias = Categoria.objects.all()
    return  render(request, 'agProducto.html',{'productos':productos,'categorias':categorias})


@role_required(allowed_roles=['ADMINISTRADOR'])
def guardarProducto(request):
    id_cat = request.POST.get("id_cat").strip()
    id_pro = request.POST.get("id_pro")
    nombre_pro = request.POST.get("nombre_pro", "").strip().upper()
    cantidad_pro = request.POST.get("cantidad_pro")
    descripcion_pro = request.POST.get("descripcion_pro", "").upper()
    ftprodu = request.FILES.get("ftprodu")
    # Verificar si ya existe un producto con el mismo nombre o código
    if Producto.objects.filter(nombre_pro=nombre_pro).exists():
        messages.error(request, 'Ya existe un producto con el mismo nombre.')
        return redirect('productosadmin')
    if Producto.objects.filter(id_pro=id_pro).exists():
        messages.error(request, 'Ya existe un producto con el mismo código.')
        return redirect('productosadmin')
    try:
        obtenerCategoria = Categoria.objects.get(id_cat=id_cat)
    except Categoria.DoesNotExist:
        messages.error(request, 'La categoría seleccionada no existe.')
        return redirect('productosadmin')
    Producto.objects.create(
        nombre_pro=nombre_pro,
        cantidad_pro=cantidad_pro,
        descripcion_pro=descripcion_pro,
        ftprodu=ftprodu,
        fkcategoria=obtenerCategoria,
        id_pro=id_pro)
    messages.success(request, 'Producto Guardado Exitosamente')
    return redirect('productosadmin')



@role_required(allowed_roles=['ADMINISTRADOR'])
def eliminarProducto(request,id_pro):
    proEliminar=Producto.objects.get(id_pro=id_pro)
    proEliminar.delete()
    messages.success(request,'Producto Eliminado Exitosamente')
    return redirect('productosadmin')

#Renderizar  Producto
@role_required(allowed_roles=['ADMINISTRADOR'])
def editarProducto(request,id_pro):
    productos=Producto.objects.get(id_pro=id_pro)
    categorias = Categoria.objects.all()
    return  render(request, 'editarProducto.html',{'productos':productos,'categorias':categorias})

@role_required(allowed_roles=['ADMINISTRADOR'])
def actProducto(request):
    id_pro = request.POST["id_pro"]
    id_cat = request.POST["id_cat"]
    obtenerCategoria=Categoria.objects.get(id_cat=id_cat)
    nombre_pro = request.POST["nombre_pro"].upper()
    cantidad_pro = request.POST["cantidad_pro"].replace(',', '.')
    descripcion_pro = request.POST["descripcion_pro"].upper()
    ftprodu = request.FILES.get("ftprodu")
    producto_editar = Producto.objects.get(id_pro=id_pro)
    producto_editar.nombre_pro = nombre_pro
    producto_editar.cantidad_pro = cantidad_pro
    producto_editar.descripcion_pro = descripcion_pro
    producto_editar.fkcategoria = obtenerCategoria
    if ftprodu:
        if producto_editar.ftprodu:
            default_storage.delete(producto_editar.ftprodu.path)
        producto_editar.ftprodu = ftprodu
    producto_editar.producto = ftprodu
    producto_editar.save()
    messages.success(request, 'Producto actualizado exitosamente')
    return redirect('productosadmin')




#---------------------Categoria--------------------------------
@role_required(allowed_roles=['ADMINISTRADOR'])
def verCategoria(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria.html', {'categorias': categorias})

@role_required(allowed_roles=['ADMINISTRADOR'])
def agCategoria(request):
    categorias=Categoria.objects.all()
    return  render(request, 'agCategoria.html',{'categorias':categorias})

@role_required(allowed_roles=['ADMINISTRADOR'])
def guardarCategoria(request):
    tipo_cat = request.POST["tipo_cat"].strip().upper()
    # Verificar si la categoría ya existe
    if Categoria.objects.filter(tipo_cat=tipo_cat).exists():
        messages.error(request, 'La categoría ya existe.')
        return redirect('/agCategoria', id_cat=request.POST.get("id_cat"))
    # Crear nueva categoría si no existe
    Categoria.objects.create(tipo_cat=tipo_cat)
    messages.success(request, 'Categoría guardada exitosamente.')
    return redirect('categorias')












@role_required(allowed_roles=['ADMINISTRADOR'])
def eliminarCategoria(request, id_cat):
    # Obtén la categoría que deseas eliminar
    categoria = get_object_or_404(Categoria, id_cat=id_cat)
    # Verifica si la categoría está asociada a algún producto
    if Producto.objects.filter(fkcategoria=categoria).exists():
        messages.error(request, 'No se puede eliminar la categoría porque está asociada a uno o más productos.')
        return redirect('/categorias')
    # Si no hay productos asociados, elimina la categoría
    categoria.delete()
    messages.success(request, 'Categoría eliminada exitosamente.')
    return redirect('/categorias')


@role_required(allowed_roles=['ADMINISTRADOR'])
def editarCategoria(request,id_cat):
    categorias=Categoria.objects.get(id_cat=id_cat)
    return  render(request, 'editarCategoria.html',{'categorias':categorias})

@role_required(allowed_roles=['ADMINISTRADOR'])
def actCategoria(request):
    id_cat = request.POST["id_cat"]
    tipo_cat = request.POST["tipo_cat"].upper()
    categoria_editar = Categoria.objects.get(id_cat=id_cat)
    categoria_editar.tipo_cat = tipo_cat
    categoria_editar.save()
    messages.success(request, 'Categoria actualizado exitosamente')
    return redirect('/categorias')


#------Productos-------




# views.py
def obtener_producto(request, id_pro):
    try:
        producto = Producto.objects.get(id_pro=id_pro)
        data = {
            'nombre_pro': producto.nombre_pro,
            'cantidad_pro': producto.cantidad_pro,
            'descripcion_pro': producto.descripcion_pro,
            'ftprodu': producto.ftprodu.url if producto.ftprodu else None,
            'fkcategoria': producto.fkcategoria.tipo_cat
        }
        return JsonResponse(data)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

#-------------Calendario----------
    detalles_recibidos = Detalle.objects.filter(estado_det='Recibida')
    detalles_iniciados = Detalle.objects.filter(estado_det='Iniciado')
    detalles_iniciados = Detalle.objects.filter(estado_det='List_ent')
    detalles_ordenes = detalles_recibidos | detalles_iniciados
    context = {
        'detalles_ordenes': detalles_ordenes
    }
    return render(request, 'calendario.html', context)



@role_required(allowed_roles=['MECANICO','ADMINISTRADOR'])
def vista_calendario(request):
    detalles_ordenes = Detalle.objects.filter(estado_det__in=['Recibida', 'Iniciado', 'List_ent']).select_related('orden')
    return render(request, 'calendario.html', {'detalles_ordenes': detalles_ordenes})


#--------------------------Usuarios------------------------------------------------
@role_required(allowed_roles=['ADMINISTRADOR'])
def verUsuarios(request):
    usuarios = Usuarios.objects.all()
    mecanicos = Mecanico.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios,'mecanicos':mecanicos})

@role_required(allowed_roles=['ADMINISTRADOR'])
def guardarUsuario(request):
    id_mec = request.POST["id_mec"]
    obtenerMecanico=Mecanico.objects.get(id_mec=id_mec)
    tipo_us = request.POST["tipo_us"]
    usuario = request.POST["usuario"]
    contrasena = request.POST["contrasena"]
    estado_us = request.POST["estado_us"]
    nuevoUsuario = Usuarios.objects.create(
    tipo_us=tipo_us,
    usuario=usuario,
    contrasena=contrasena,
    estado_us=estado_us,
    fkmecanicos=obtenerMecanico
    );
    messages.success(request,'Usuario Guardado Exitosamente')
    return redirect('/usuarios')



def editarUsuario(request,id_us):
    usuarios=Usuario.objects.get(id_us=id_us)
    return  render(request, 'editarUsuario.html',{'usuarios':usuarios})

def actUsuario(request):
    id_us = request.POST["id_us"]
    tipo_us = request.POST["tipo_us"]
    usuario = request.POST["usuario"]
    contrasena = request.POST["contrasena"]
    estado_us = request.POST["estado_us"]
    usuario_editar = Usuario.objects.get(id_us=id_us)
    usuario_editar.tipo_us = tipo_us
    usuario_editar.usuario = usuario
    usuario_editar.contrasena = contrasena
    usuario_editar.estado_us = estado_us
    usuario_editar.save()
    messages.success(request, 'Usuadio actualizado exitosamente')
    return redirect('')







#----------------Ver estado de la bici-------
def verEstadobici(request):
    id_cli = request.GET.get('id_cli')
    bicicletas = []
    ordenes = []
    clientes = []
    detalles = []

    if id_cli:
        bicicletas = Bicicleta.objects.filter(cliente__id_cli=id_cli)
        ordenes = Orden.objects.filter(bicicleta__cliente__id_cli=id_cli)
        clientes = Clientes.objects.filter(id_cli=id_cli)
        detalles = Detalle.objects.filter(orden__bicicleta__cliente__id_cli=id_cli)

    return render(request, 'productos/verEstado.html', {
        'bicicletas': bicicletas,
        'ordenes': ordenes,
        'clientes': clientes,
        'detalles': detalles,
        'id_cli': id_cli
    })


#----------------Logins por Roles-----------

# Función de inicio de sesión


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = Usuario.objects.get(username=username)
            if user.check_password(password):
                if user.is_active:
                    request.session['user_id'] = user.id
                    messages.success(request, 'Inicio de sesión exitoso')
                    # Redirigir basado en el rol del usuario
                    if user.rol == 'ADMINISTRADOR':
                        return redirect('menuadmin')
                    elif user.rol == 'MECANICO':
                        return redirect('menuadmin')
                else:
                    messages.error(request, 'Cuenta inactiva. Contacta al administrador.')
                    return redirect('login')
            else:
                messages.error(request, 'Contraseña incorrecta')
                return redirect('login')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
            return redirect('login')
    return render(request, 'login.html')


# Función de cierre de sesión

def logout_view(request):
    if request.user.is_authenticated:
        try:
            session = Session.objects.get(session_key=request.session.session_key)
            UserSession.objects.filter(session=session).delete()
        except Session.DoesNotExist:
            pass
        logout(request)
    return redirect('login')


# Vista de registro de usuario
# Vista de registro de usuario
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email'].lower()
        nombre = request.POST['nombre'].upper()
        apellido = request.POST['apellido'].upper()
        telefono = request.POST['telefono']
        ci_us = request.POST['ci_us']
        rol = request.POST['rol'].upper()

        # Verificar si ya existe un usuario con el mismo username
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe. Por favor, elija un nombre de usuario diferente.')
            return render(request, 'register.html', {
                'username': username,
                'email': email,
                'nombre': nombre,
                'apellido': apellido,
                'telefono': telefono,
                'ci_us': ci_us,
                'rol': rol
            })

        # Verificar si ya existe un usuario con el mismo email
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado. Por favor, use un correo diferente.')
            return render(request, 'register.html', {
                'username': username,
                'email': email,
                'nombre': nombre,
                'apellido': apellido,
                'telefono': telefono,
                'ci_us': ci_us,
                'rol': rol
            })

        # Verificar si ya existe un usuario con el mismo ci_us
        if Usuario.objects.filter(ci_us=ci_us).exists():
            messages.error(request, 'La cédula ya está registrada. Por favor, use una cédula diferente.')
            return render(request, 'register.html', {
                'username': username,
                'email': email,
                'nombre': nombre,
                'apellido': apellido,
                'telefono': telefono,
                'ci_us': ci_us,
                'rol': rol
            })

        user = Usuario(
            username=username,
            email=email,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            ci_us=ci_us,
            rol=rol)
        user.set_password(password)  # Hashear la contraseña
        user.save()
        messages.success(request, 'Usuario registrado exitosamente')
        return redirect('mecanicos')
    return render(request, 'register.html')
# Vista de permiso denegado

def permission_denied_view(request):
    messages.error(request, 'No tienes permiso para realizar esta acción.')
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)
# Vista para el administrador



#------------Error de urls no existentes-------

def custom_404(request, exception):
    return render(request, '404.html', {}, status=404)



#Menu inicio despues del login Admin
def menuAdmin(request):
    user = Usuario.objects.get(id=request.session['user_id'])

    return render(request, 'menuadmin.html')

#------------------Reportes de orden --------------------




def lista_ordenes(request):
    estado = request.GET.get('estado')
    if estado:
        ordenes = Orden.objects.filter(estado=estado)
    else:
        ordenes = Orden.objects.all()

    context = {
        'ordenes': ordenes,
        'estado_seleccionado': estado,
    }
    return render(request, 'ordenes.html', context)








def verPlan(request):
        return render(request, 'plant2.html')



#Reportes de las ordenes

def detalle_orden(request, orden_id):
    error_message = None
    try:
        orden = Orden.objects.get(id_ord=orden_id)
        detalles = Detalle.objects.filter(orden=orden)
    except Orden.DoesNotExist:
        error_message = "Orden no encontrada."
    except Exception as e:
        error_message = "Ocurrió un error al generar el reporte."

    context = {
        'orden': orden,
        'detalles': detalles,
        'error_message': error_message
    }
    return render(request, 'reporte.html', context)
