from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
  def get_queryset(self):
    return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
  DRAFT = 'draft'
  PUBLISHED = 'published'
  STATUS_CHOICES =(
    (DRAFT, 'Draft'),
    (PUBLISHED, 'Published'),
  )

  title = models.CharField(max_length=250)
  slug = models.SlugField(max_length=250, unique_for_date='publish')
  image = models.ImageField(upload_to='featured_image/%Y/%m/%d/')
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
  body = RichTextUploadingField()
  publish = models.DateTimeField(default=timezone.now)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)


  class Meta:
    ordering = ('-publish',)

  
  def __str__(self) -> str:
    return self.title

  
  object = models.Manager()
  published = PublishedManager()

  tags = TaggableManager()


  def get_absolute_url(self):
    return reverse(viewname='blog:post_detail', args=[self.slug])

  def get_comments(self):
    return self.comments.filter(parent=None).filter(active=True)


class Comment(models.Model):
  post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
  name=models.CharField(max_length=50)
  email=models.EmailField()
  parent=models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
  body = models.TextField()
  
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  active = models.BooleanField(default=True)
  class Meta:
      ordering = ('created',)
  
  def __str__(self):
      return self.body
  def get_comments(self):
      return Comment.objects.filter(parent=self).filter(active=True)