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


class Comment(models.Model):
    # 新闻评论
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey("News", related_name='comments',
                             on_delete=models.CASCADE)
    author = models.ForeignKey("xfzauth.User", related_name='comments',
                               on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.news_id}: {self.content}"

    class Meta:
        ordering = ('-pub_time',)
