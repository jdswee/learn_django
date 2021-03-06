from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
import markdown
from django.utils.html import strip_tags

# 分类
@python_2_unicode_compatible
class Category(models.Model):
  name = models.CharField(max_length=100)
  def __str__(self):
    return self.name

# 标签 
@python_2_unicode_compatible
class Tag(models.Model):
  name = models.CharField(max_length=100)
  def __str__(self):
    return self.name

# 文章
@python_2_unicode_compatible
class Post(models.Model):
  # 文章标题
  title = models.CharField(max_length=70)
  # 文章正文
  body = models.TextField()
  # 文章创建时间和修改时间
  created_time = models.DateTimeField()
  modified_time = models.DateTimeField()
  # 文章摘要，可以没有摘要，允许空值
  excerpt = models.CharField(max_length=200, blank=True)
  # 把文章对应的数据库表和分类、标签对应的数据库表关联起来
  category = models.ForeignKey(Category)
  tags = models.ManyToManyField(Tag, blank=True)
  # 文章作者
  author = models.ForeignKey(User)
  def __str__(self):
    return self.title
  def get_absolute_url(self):
    return reverse('blog:detail', kwargs={'pk': self.pk})
  class Meta:
    ordering = ['-created_time']
  
  # 阅读量  
  views = models.PositiveIntegerField(default=0)
  
  def increase_views(self):
    self.views += 1
    self.save(update_fields=['views'])
  
  def save(self, *args, **kwargs):
      # 如果没有填写摘要
      if not self.excerpt:
        md = markdown.Markdown(extensions=[
          'markdown.extensions.extra',
          'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
      super(Post, self).save(*args, **kwargs)

