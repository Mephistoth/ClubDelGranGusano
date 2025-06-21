from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Comentario
from .forms import BlogForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ComentarioForm
from django.contrib.auth.models import User
from .models import EmailBloqueado  
from django.core.mail import send_mail
from django.conf import settings

@user_passes_test(lambda u: u.is_staff or u.groups.filter(name='educador').exists())
def correos_bloqueados(request):
    correos = EmailBloqueado.objects.all().order_by('email')
    return render(request, 'blogs/correos_bloqueados.html', {'correos': correos})

@user_passes_test(lambda u: u.is_staff or u.groups.filter(name='educador').exists())
def expulsar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if usuario.is_superuser:
        return redirect('moderar_usuarios')
    username = usuario.username
    email = usuario.email

    #  Enviar correo antes de eliminar
    send_mail(
        'Has sido expulsado de la comunidad',
        (
            f'Hola {username},\n\n'
            'Te notificamos que tu cuenta en esta comunidad ha sido expulsada.\n'
            'Si deseas más detalles, contáctanos.\n\n'
            'Saludos, El Equipo de Moderación.'
        ),
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

    # Guardamos en la lista negra
    EmailBloqueado.objects.get_or_create(email=email)

    usuario.delete()
    return redirect('moderar_usuarios')

def home(request):
    ultimas_publicaciones = Blog.objects.filter(aprobado=True).order_by('-fecha_creacion')[:5]
    return render(request, 'account/home.html', {'ultimas_publicaciones': ultimas_publicaciones})



@user_passes_test(lambda u: u.is_staff or u.groups.filter(name='educador').exists())
def eliminar_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        blog.delete()
        return redirect('lista_blogs')
    return redirect('detalle_blog', blog_id=blog.id)

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


@user_passes_test(lambda u: u.is_staff or u.groups.filter(name='educador').exists())
def moderar_usuarios(request):
    query = request.GET.get('q', '')
    query_email = request.GET.get('q_email', '')

    if query:
        usuarios = User.objects.filter(username__icontains=query)
    else:
        usuarios = User.objects.all()

    if query_email:
        correos_bloqueados = EmailBloqueado.objects.filter(email__icontains=query_email).order_by('email')
    else:
        correos_bloqueados = EmailBloqueado.objects.all().order_by('email')

    total_usuarios = usuarios.count()
    usuarios_activos = usuarios.filter(is_active=True).count()

    return render(request, 'blogs/moderar_usuarios.html', {
        'usuarios': usuarios,
        'total_usuarios': total_usuarios,
        'usuarios_activos': usuarios_activos,
        'correos_bloqueados': correos_bloqueados,
        'query': query,
        'query_email': query_email,
    })
@user_passes_test(lambda u: u.is_staff or u.groups.filter(name='educador').exists())
def desbloquear_email(request, correo_id):
    correo = get_object_or_404(EmailBloqueado, id=correo_id)
    correo.delete()
    return redirect('moderar_usuarios')