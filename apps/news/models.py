from django.db import models


class NewsCategory(models.Model):
    name = models.CharField(max_length=100)


class News(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    thumbnail = models.URLField()
    content = models.TextField()
    # 多对一关系
    category = models.ForeignKey('NewsCategory', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('xfzauth.User', on_delete=models.DO_NOTHING, null=True)
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_time']

