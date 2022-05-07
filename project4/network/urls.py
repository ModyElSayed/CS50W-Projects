from django.urls import path, include

from . import views

app_name = 'network'

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following_posts/", views.following_posts, name="following_posts"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    # API Routes
    path('update_or_new_post/', views.update_or_new_post, name='update_or_new_post'),
    path('update_follower/', views.update_follower, name='update_follower'),
    path('update_likes/', views.update_likes, name='update_likes'),
    path('check_likes/', views.check_likes, name='check_likes'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('get_last_comment/<int:post_id>', views.get_last_comment, name='get_last_comment'),
]
