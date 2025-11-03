from django.shortcuts import render
from models import Usuario
from django.http import JsonResponse

# Create your views here.

def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})
    data = []
    for usuario in usuarios:
        data.append({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'email': usuario.email,
            'equipo': usuario.equipo.nombre
        })
    return JsonResponse(data, safe=False)