from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Comentario
from .forms import BlogForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ComentarioForm

# Vista privada: solo usuarios con permisos ven blogs no aprobados
@user_passes_test(lambda u: u.is_staff or u.groups.filter(name='educador').exists())
def moderar_blogs(request):
    blogs_pendientes = Blog.objects.filter(aprobado=False).order_by('-fecha_creacion')
    return render(request, 'blogs/moderar_blogs.html', {
        'blogs_pendientes': blogs_pendientes
    })

# Acción: aprobar blog
@user_passes_test(lambda u: u.is_staff or u.groups.filter(name='educador').exists())
def aprobar_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.aprobado = True
    blog.save()
    return redirect('moderar_blogs')

# Acción: rechazar blog (opcional, puedes borrarlo o dejarlo sin mostrar)
@user_passes_test(lambda u: u.is_staff or u.groups.filter(name='educador').exists())
def rechazar_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()  # O si prefieres marcar como rechazado, agrega un campo `rechazado`
    return redirect('moderar_blogs')

def detalle_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comentarios = Comentario.objects.filter(blog=blog, respuesta_a=None).prefetch_related('respuestas')

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.blog = blog
            nuevo_comentario.autor = request.user
            # Revisamos si es una respuesta
            respuesta_id = request.POST.get('respuesta_a')
            if respuesta_id:
                nuevo_comentario.respuesta_a_id = respuesta_id
            nuevo_comentario.save()
            return redirect('detalle_blog', blog_id=blog.id)
    else:
        form = ComentarioForm()

    return render(request, 'blogs/detalle_blog.html', {
        'blog': blog,
        'comentarios': comentarios,
        'form': form
    })


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