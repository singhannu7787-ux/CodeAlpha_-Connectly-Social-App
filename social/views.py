from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'social/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'social/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/login/')

@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'social/home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        Post.objects.create(author=request.user, content=content)
        return redirect('/')
    return render(request, 'social/create_post.html')

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        text = request.POST.get('text')
        Comment.objects.create(post=post, user=request.user, text=text)
        return redirect('post_detail', pk=pk)
    return render(request, 'social/post_detail.html', {'post': post, 'comments': comments})
