from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to = 'profile_pics')
    

    def __str__(self):
        return f'{self.user.username} Profile'




class BlogPost(models.Model):
    blog_title = models.CharField(max_length = 50)
    blog_text = models.TextField()
    blog_date = models.DateTimeField(default = timezone.now)
    blog_author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = "BlogEntry"

    def __str__(self):
        return f'{self.blog_title}'

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk':self.pk})

