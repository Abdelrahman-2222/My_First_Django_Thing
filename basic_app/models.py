from django.db import models
from django.utils import timezone
from django.urls import reverse
# from django import template


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Authorization of user
    title = models.CharField(max_length=200)
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    publication_date = models.DateTimeField(blank=True, null=True)  # null or blank

    def publish(self):
        self.publication_date = timezone.now()
        self.save()

    def approve_comments(self):
        # comments = related_name in Class Comment
        # approved_comments = approved_comments in Class Comment
        return self.comments.filter(approved_comments=True)

    # After I created a post, and I hit publication, go to post_detail
    # for the primary key u just created
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk': self.pk})

    # register = template.Library()
    #
    # @register.filter()
    # def range(min_num=5):
    #     return range(min_num)

    def __str__(self):
        return self.title


# For Fans Commenting on The author Original Post
class Comment(models.Model):
    post = models.ForeignKey('basic_app.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    approved_comments = models.BooleanField(default=False)

    def approve(self):
        self.approved_comments = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text
