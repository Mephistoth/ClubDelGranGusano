from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from .forms import BlogForm
from django.contrib.auth.decorators import login_required

def lista_blogs(request):
    blogs = Blog.objects.filter(aprobado=True).order_by('-fecha_creacion')
    return render(request, 'blogs/lista_blogs.html', {'blogs': blogs})

@login_required
def crear_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.autor = request.user
            blog.aprobado = False  # Requiere moderación
            blog.save()
            return redirect('lista_blogs')
    else:
        form = BlogForm()
    return render(request, 'blogs/crear_blog.html', {'form': form})