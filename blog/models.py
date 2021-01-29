from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinValueValidator

from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from tinymce.models import HTMLField

import uuid



# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
	order = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)

	class Meta:
		verbose_name = 'category'
		verbose_name_plural = 'categories'


	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('category', args=[self.slug])

	def confirmed_post(self):
		posts = Post.publishee.filter(category=self)
		return posts


class PublishManager(models.Manager):
	def get_queryset(self):
		return super(PublishManager,self).get_queryset().filter(status='published', poster__confirm=True)



class Post(models.Model):
	status_choices = (
		('draft', 'Drafted'),
		('published', 'Published'),
		)

	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique_for_date='publish')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
	body = RichTextUploadingField()
	image = models.ImageField(upload_to='post/%Y-%m-%d', blank=True, null=True)

	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	status = models.CharField(max_length=12, choices=status_choices, default='draft')

	view_count = models.IntegerField(default=0)
	comment_count = models.IntegerField(default=0)
	previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
	next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

	objects = models.Manager()
	publishee = PublishManager()
	tags = TaggableManager()

	featured = models.BooleanField(default=False)
	breaking = models.BooleanField(default=False)
	editor_pick = models.BooleanField(default=False)
	popular  = models.BooleanField(default=False)
	trending = models.BooleanField(default=False)

	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		post_time = timezone.localtime(self.publish)
		return reverse('detail', args=[self.slug, post_time.year, post_time.month, post_time.day])


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	#updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('created',)

	def __str__(self):
		return "Comment by {} on {}".format(self.name, self.post)


class Subscriber(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField()
	preferences = models.ManyToManyField(Category, related_name='subscribers')
	last_seen = models.DateTimeField(default=timezone.now)
	code = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	subscribe = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('unsubscribe', args=[self.code])


class Poster(models.Model):
	post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='poster')
	confirm = models.BooleanField(default=False)

	def __str__(self):
		return self.post.title