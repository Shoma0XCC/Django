from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title


class Info(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    headline = models.CharField(max_length=100)
    text = models.TextField()
    pub_date = models.DateTimeField()
    mod_date = models.DateTimeField()
    user = models.ManyToManyField(User)
    count_comments = models.IntegerField(default=0)
    count_likes = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)


    def __str__(self):
        return self.headline
