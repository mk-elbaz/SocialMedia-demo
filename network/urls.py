
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("network/newPost", views.newPost, name="newPost"),
    path("network/followersPosts", views.followersPosts, name="followersPosts"),
    path("<int:user_id>", views.viewProfile, name="viewProfile"),
    path("changeFollow/<int:user_id>", views.changeFollow, name="changeFollow"),
    path("editPost", views.editPost, name="editPost"),
    path("changeLike", views.changeLike, name="changeLike"),

]
