from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from .models import Prestamo
from .forms import PrestamoForm
from django.contrib.auth.forms import AuthenticationForm
from appejemplares.models import Libro
from appejemplares import views
from appusuarios.models import Usuario
from django.dispatch import receiver
from django.db.models.signals import pre_save
from datetime import date, timedelta


@login_required
def prestamos(request):
    """
    Vista para mostrar la lista de préstamos y filtrar por búsqueda.

    Parameters:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: La respuesta HTTP que muestra la lista de préstamos.
    """

    busqueda = request.GET.get("buscar_prestamo")
    prestamos = Prestamo.objects.all()

   #Querys con la busqueda, que se obtiene del input name del index.html
    if busqueda:
        prestamos = Prestamo.objects.filter( 
            Q(isbn = busqueda) |
            Q(rut_usuario = busqueda) |
            Q(estado_prestamo__icontains = busqueda) 
    ) 
    
    return render(request, 'prestamos/index.html', {'prestamos': prestamos})

def nuevo_prestamo(request):
    """
    Vista para crear un nuevo préstamo.

    Parameters:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: La respuesta HTTP que muestra el formulario para un nuevo préstamo.
    """

    formulario = PrestamoForm(request.POST or None, request.FILES or None)
    
    if formulario.is_valid():
        formulario.save()
        return redirect('prestamos')
    return render(request, 'prestamos/nuevo_prestamo.html', {'formulario': formulario,'mensaje':'OK'})

def editar_prestamo(request, id_prestamo):
    """
    Vista para editar un préstamo existente.

    Parameters:
        request (HttpRequest): La solicitud HTTP recibida.
        id_prestamo (int): El ID del préstamo a editar.

    Returns:
        HttpResponse: La respuesta HTTP que muestra el formulario para editar el préstamo.
    """

    # Obtener el préstamo
    prestamo = Prestamo.objects.get(id_prestamo=id_prestamo)
    
    # Formatear las fechas
    fecha_devolucion_calculada = prestamo.fecha_devolucion_calculada.strftime("%Y-%m-%d")
    fecha_prestamo = prestamo.fecha_prestamo.strftime("%Y-%m-%d")

    # Establecer los valores originales del préstamo en el formulario
    formulario = PrestamoForm(
        request.POST or None,
        request.FILES or None,
        instance=prestamo,
        initial={
            'fecha_devolucion_calculada': fecha_devolucion_calculada,
            'fecha_prestamo': fecha_prestamo,
        }
    )
    # Deshabilitar la edición de los campos
    formulario.fields['isbn'].widget.attrs['disabled'] = True
    formulario.fields['rut_usuario'].widget.attrs['disabled'] = True
    formulario.fields['fecha_prestamo'].widget.attrs['disabled'] = True


    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('prestamos')
    return render(request, 'prestamos/editar_prestamo.html', {'formulario':formulario})

def eliminar_prestamo(request, id_prestamo):
    """
    Vista para eliminar un préstamo existente.

    Parameters:
        request (HttpRequest): La solicitud HTTP recibida.
        id_prestamo (int): El ID del préstamo a eliminar.

    Returns:
        HttpResponse: La respuesta HTTP que redirige a la lista de préstamos después de la eliminación.
    """
    
    prestamo = Prestamo.objects.get(id_prestamo=id_prestamo)
    prestamo.delete()
    return redirect('prestamos')

