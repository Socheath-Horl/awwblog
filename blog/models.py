from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


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


  def get_absolute_url(self):
    return reverse(viewname='blog:post_detail', args=[self.slug])
