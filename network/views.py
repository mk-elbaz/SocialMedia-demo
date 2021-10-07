from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import fields
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django import forms


from .models import *

#https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/#overriding-the-default-fields
class newPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        labels = {
            'text' : _('Enter your post here')
            }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control','style' : 'margin-top: 10px' }),
        }


# reference to project 3 and 2 down

def index(req):
    post = Post.objects.all().order_by("-timestamp")
    pageNum = req.GET.get("page", 1)
    paginator = Paginator(post, 10)
    posts = paginator.get_page(pageNum)
    return render(req, "network/index.html", {
        "posts": posts,
        "numOfPages": range(posts.paginator.num_pages),
        "currentPage": pageNum
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
                "message": "username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def newPost(req):
    if req.method == "POST":
        author = User.objects.get(id=req.user.id)
        form = newPostForm(req.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = author
            form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(req, "network/newPost.html", {
                "form": form
            })
    else:
        return render(req, "network/newPost.html", {
            "form": newPostForm()
        })


@login_required
def editPost(req):
    # post = Post.objects.get(id = post_id)
    # form = newPostForm()
    # form.fields['text'].initial = post.text
    # post.delete()
    # return render(req , "network/newPost.html",{
    #     "form" : form
    # })
    if req.method == 'POST':
        body = json.loads(req.body)  
        post_id = int(body['post_id'])
        newText = body['newText']
        post = Post.objects.get(id = post_id)
        post.text = newText
        post.save()
    #https://stackoverflow.com/questions/44859690/reload-page-automatically-without-needing-to-re-enter-url-again-django
    return redirect('index')

@login_required
def followersPosts(req):
    user = User.objects.get(id=req.user.id)
    follow = user.following.all()
    followers = [f.user for f in follow]

    post = Post.objects.filter(author__in=followers).order_by("-timestamp")
    paginator = Paginator(post, 10)
    pageNum = req.GET.get("page", 1)
    posts = paginator.get_page(pageNum)
    return render(req, "network/following.html", {  # html..................
        "posts": posts,
        "numOfPages": range(posts.paginator.num_pages),
        "currentPage": pageNum
    })


# https://stackoverflow.com/questions/1941212/correct-way-to-use-get-or-create
def viewProfile(req, user_id):
    if not User.objects.filter(id = req.user.id).exists():
        return redirect('register')
    profile = User.objects.get(id = user_id)
    followedUser, _ = Following.objects.get_or_create(user=profile)
    followingBool = req.user in followedUser.followers.all()

    followersNum = followedUser.followers.count()
    followingNum = profile.following.count()

    post = Post.objects.filter(author=profile).order_by("-timestamp")
    paginator = Paginator(post, 10)
    pageNum = req.GET.get("page", 1)
    posts = paginator.get_page(pageNum)

    return render(req, "network/profile.html", {  # html..................
        "username": profile,
        "following": followingBool,
        "followersNum": followersNum,
        "followingNum": followingNum,
        "posts": posts,
        "numOfPages": range(posts.paginator.num_pages),
        "currentPage": pageNum
    })


@login_required
def changeLike(req):
    if req.method == "POST":
        body = json.loads(req.body)
        likeAuthor = body['likeAuthor']
        post_id = body['post_id']

        user = User.objects.get(id = req.user.id)
        post = Post.objects.get(id=post_id)
        if user in post.likes.all():
            like = False
            post.likes.remove(user)
        else:
            like = True
            post.likes.add(user)
        post.save()
        likesCount = post.getLikesCount
    return HttpResponse(json.dumps(
            {'likesCount': likesCount, 'like' : like}
        ))

@login_required
def changeFollow(req, user_id):
    target = User.objects.get(id = user_id)
    if req.user == target:
        return JsonResponse({"message": "Can't follow yourself!"}, status=400)
    
    followed, _ = Following.objects.get_or_create(user=target)
    if req.user in followed.followers.all():
        followed.followers.remove(req.user)
    else:
        followed.followers.add(req.user)
    followed.save()
    return HttpResponseRedirect(reverse("viewProfile", kwargs={"user_id" : target.id}))
