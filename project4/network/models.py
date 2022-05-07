from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        db_table = 'user'
        app_label = 'network'

    bio = models.CharField(max_length=255)


class Follow(models.Model):
    class Meta:
        db_table = 'follow'
        app_label = 'network'
        unique_together = ('following', 'followers')

    following = models.ForeignKey(User, on_delete=models.CASCADE, db_column='following', related_name='following')
    followers = models.ForeignKey(User, on_delete=models.CASCADE, db_column='followers', related_name='followers')


class Posts(models.Model):
    class Meta:
        db_table = 'posts'
        app_label = 'network'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')
    content = models.CharField(max_length=255)
    num_of_likes = models.IntegerField(default=0, db_column='number_of_likes')
    date_created = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        comments_data = Comments.objects.filter(post_id=self.id).order_by('-date_created')
        comments = [comment.serialize() for comment in comments_data]

        return {
                'post_id': self.id,
                'username': self.user.username,
                'content': self.content,
                'number_of_likes': self.num_of_likes if self.num_of_likes != 0 else 'Be the first to like',
                "date_created": self.date_created.strftime("%b %d %Y, %I:%M %p"),
                "date_created_exact": self.date_created.strftime('%Y %-m %-d %-H %-M %-S %f'),
                'number_of_comments': Comments.objects.filter(post_id=self.id).count(),
                'comments': comments
                }


class Likes(models.Model):
    class Meta:
        db_table = 'likes'
        app_label = 'network'
        unique_together = ('post', 'user')

    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='likes_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')


class Comments(models.Model):
    class Meta:
        db_table = 'comments'
        app_label = 'network'

    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    content = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
                'comment_id': self.id,
                'post_id': self.post.id,
                'username': self.user.username,
                'content': self.content,
                "date_created": self.date_created.strftime("%b %d %Y, %I:%M %p"),
                'number_of_comments': Comments.objects.filter(post_id=self.post.id).count(),
                }
