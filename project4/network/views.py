import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from .models import User, Posts, Comments, Follow, Likes
from .forms import NewPost


def index(request):
    new_post_form = NewPost(request.POST or None)
    posts_data = Posts.objects.all().order_by('-date_created')
    posts_objects = [post.serialize() for post in posts_data]
    paginator = Paginator(posts_objects, 10)

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    page_numbers = list()

    if page_number is None:
        page_number = 1

    for number in range(1, paginator.num_pages + 1):
        page_numbers.append(number)

    difference = paginator.num_pages + 1 - int(page_number)
    if difference > 3:
        start = int(page_number) - 1
        end = (int(page_number) + 3)
        page_numbers = page_numbers[start:end]

    return render(request, "network/index.html", context={'posts': posts, 'page_numbers': page_numbers,
                                                          'new_post_form': new_post_form})


def profile(request, username):
    profile_username = User.objects.get(username=username)
    num_of_followers = Follow.objects.filter(following=profile_username).count()
    num_of_following = Follow.objects.filter(followers=profile_username).count()
    bio = profile_username.bio
    posts_data = Posts.objects.filter(user=profile_username.id).order_by('-date_created')
    is_follower: bool = False

    if request.user.is_authenticated:
        if username != request.user.username:
            try:
                is_follower: bool = True
                Follow.objects.get(following=profile_username, followers=request.user)
            except Follow.DoesNotExist:
                is_follower: bool = False

    posts = [post.serialize() for post in posts_data]
    context = {'username': username, 'number_of_followers': num_of_followers, 'number_of_following': num_of_following,
               'bio': bio, 'posts': posts, 'is_follower': is_follower}
    return render(request, 'network/profile.html', context)


@login_required
def following_posts(request):
    user = User.objects.get(pk=request.user.id)
    followings = Follow.objects.filter(followers=user)
    posts_data = Posts.objects.filter(user__in=followings.values('following_id')).order_by('-date_created')
    posts = [post.serialize() for post in posts_data]
    context = {'posts': posts}

    return render(request, 'network/following_posts.html', context)


@login_required
def update_or_new_post(request):
    if request.method == "POST":
        received_data = json.loads(request.body)
        post_content = received_data['new_content']
        Posts.objects.create(user=request.user, content=post_content).save()
        return JsonResponse({'message': 'Post has been created'}, status=201)

    if request.method == 'PUT':
        received_data = json.loads(request.body)
        new_post_content = received_data['new_content']
        old_post_content = received_data['old_content']
        post_id = received_data['post_id']
        if old_post_content != new_post_content:
            post = Posts.objects.get(pk=post_id)
            post.content = new_post_content
            post.save()

            return JsonResponse({'message': 'Post has been updated'}, status=201)
        else:
            return JsonResponse({'message': 'You did not change the post'}, status=201)

    return JsonResponse({'message': 'Incorrect Data: Please don\'t enter an empty post'}, status=400)


@login_required
def update_follower(request):
    if request.method == 'PUT':
        received_data = json.loads(request.body)
        follower_username = received_data['follower']
        status = received_data['status']

        profile_username = User.objects.get(username=follower_username)

        try:
            if status == 'Follow':
                Follow.objects.create(following=profile_username, followers=request.user)
            elif status == 'Unfollow':
                Follow.objects.get(following=profile_username, followers=request.user).delete()
            else:
                return JsonResponse({'message': 'Unknown status'}, status=400)
        except IntegrityError as e:
            return JsonResponse({'message': e}, status=400)

        update_num_of_followers = Follow.objects.filter(following=profile_username).count()
        update_num_of_following = Follow.objects.filter(followers=profile_username).count()

        return JsonResponse({'message': 'Updated', 'number_of_following': str(update_num_of_following),
                             'number_of_followers': str(update_num_of_followers)}, status=201)

    return JsonResponse({'message': 'Incorrect method'}, status=400)


@login_required
def update_likes(request):
    if request.method == 'PUT':
        received_data = json.loads(request.body)
        post_id = received_data['post_id']
        post = Posts.objects.get(pk=post_id)
        status = 'Increased'

        try:
            Likes.objects.create(post=post, user=request.user)
            post.num_of_likes += 1
        except IntegrityError:
            Likes.objects.get(post=post, user=request.user).delete()
            post.num_of_likes -= 1
            status = 'Decreased'

        post.save()

        number_of_likes = post.num_of_likes if post.num_of_likes != 0 else 'Be the first to like'
        return JsonResponse({'message': 'Number of likes has been updated',
                             'number_of_likes': number_of_likes, 'status': status}, status=201)

    return render(request, 'network/login.html')


@login_required
def check_likes(request):
    if request.method == "GET":
        posts_liked = Likes.objects.filter(user=request.user)
        posts_id = [post['post_id'] for post in list(posts_liked.values())]
        return JsonResponse({'message': 'Success', 'posts_id': posts_id}, status=201)

    return JsonResponse({'message': 'Incorrect method'}, status=400)


def get_last_comment(request, post_id):
    if request.method == 'GET':
        post = Posts.objects.get(pk=post_id)
        comment = Comments.objects.filter(post=post).order_by('-date_created')
        return JsonResponse({'message': 'Comment sent', 'comment': comment[0].serialize()}, status=201)

    return JsonResponse({'message': 'Incorrect method'}, status=400)


@login_required
def add_comment(request):
    if request.method == 'POST':
        received_data = json.loads(request.body)
        comment_content = received_data['comment_content']
        post = Posts.objects.get(pk=received_data['post_id'])
        try:
            Comments.objects.create(post=post, content=comment_content, user=request.user)
            return JsonResponse({'message': 'Success Comment Added'}, status=201)
        except IntegrityError as e:
            return JsonResponse({'message': e}, status=400)

    return JsonResponse({'message': 'Incorrect method'}, status=400)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect('network:index')
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return redirect('network:index')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect('network:index')
    else:
        return render(request, "network/register.html")
