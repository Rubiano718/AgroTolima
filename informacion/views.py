from django.shortcuts import render
from informacion.models import Post

def informacion(request):

    posts = Post.objects.all()

    return render(request, "informacion/informacion.html", {"posts": posts})

