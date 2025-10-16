from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Profile
from django.db.models import Q

# -----------------------------------------------------------
# User Registration
# -----------------------------------------------------------
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password == confirm:
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error': 'Username already taken'})
            user = User.objects.create_user(username=username, email=email, password=password)
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    return render(request, 'register.html')

# -----------------------------------------------------------
# Home Page / Feed
# -----------------------------------------------------------
@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

# -----------------------------------------------------------
# Create Post
# -----------------------------------------------------------
@login_required
def create_post(request):
    if request.method == 'POST':
        caption = request.POST.get('caption')
        image = request.FILES.get('image')
        Post.objects.create(user=request.user, caption=caption, image=image)
        return redirect('home')
    return render(request, 'create_post.html')

# -----------------------------------------------------------
# Like Post
# -----------------------------------------------------------
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('home')

# -----------------------------------------------------------
# Follow User
# -----------------------------------------------------------
@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile = user_to_follow.profile

    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)
    return redirect('profile', username=username)

# -----------------------------------------------------------
# View Profile
# -----------------------------------------------------------
@login_required
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user_profile)
    followers_count = user_profile.profile.followers.count()
    following_count = user_profile.following.count()
    is_following = False
    if request.user in user_profile.profile.followers.all():
        is_following = True

    context = {
        'user_profile': user_profile,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    }
    return render(request, 'profile.html', context)
