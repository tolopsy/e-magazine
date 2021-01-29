from django.contrib import admin
from .models import Category, Post, Comment, Subscriber, Poster
from blogman.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import render_to_string
from django.contrib.admin.models import LogEntry

# Admin actions
def send_newsletter(modeladmin, request, queryset):
    choser = queryset.filter(subscribe=True)
    subject = 'News Updates from Tidings'
    for chosen in choser:
    	choice = chosen.preferences.values_list('id', flat=True)
    	category = Category.objects.filter(id__in=choice).values_list('posts', flat=True)
    	news = Post.objects.filter(id__in=category, publish__gte=chosen.last_seen)
    	if news:
    		message = 'Hello ' + chosen.name + '. Here are your favorite news for today. Stay Updated!'
	    	for each in news:
	    		message += '\n https://tidings.herokuapp.com' + each.get_absolute_url()
	    	recipient = chosen.email
	    	html_message = render_to_string('newsmailer.html', {'news': news, 'subscriber': chosen})
	    	send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=False, html_message=html_message)
	    	chosen.last_seen = timezone.now()
	    	chosen.save()
	    	
    	else:
	    	chosen.last_seen = timezone.now()
	    	chosen.save()

send_newsletter.short_description = 'Send mail to selected'

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'parent', 'order')
	list_filter = ('parent',)
	list_editable = ('order',)
	search_fields = ('name','parent__name', 'slug')
	prepopulated_fields = {'slug': ('name',)}

class PosterInline(admin.TabularInline):
	model = Poster

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'publish', 'status', 'featured', 'breaking', 'editor_pick', 'popular', 'trending', 'order')
	list_filter = ('author', 'status', 'publish', 'created', 'featured', 'breaking', 'editor_pick', 'popular', 'trending')
	list_editable = ('featured', 'breaking', 'editor_pick', 'popular', 'trending', 'order', 'status')
	search_fields =  ('title', 'body', 'category__name')
	prepopulated_fields = {'slug': ('title',)}
	#raw_id_fields = ('author',)
	date_hierarchy = 'publish'
	autocomplete_fields = ('tags', 'author')
	inlines = [PosterInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'post', 'created', 'active')
	list_filter = ('active', 'created')
	search_fields = ('name', 'email', 'body', 'post__title')


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'last_seen', 'code', 'subscribe')
	list_filter = ('subscribe',)
	search_fields = ('name', 'email', 'preferences')
	list_editable = ('last_seen',)
	actions = [send_newsletter]


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
	date_hierarchy = 'action_time'
	list_filter = ('user', 'content_type', 'action_flag')
	search_fields = ('object_repr', 'change_message')
	list_display = ('action_time', 'user', 'content_type', 'action_flag')


admin.site.site_header = "Tidings News Administration"
admin.site.index_title = "Tidings Admin"
admin.site.site_title = "Your Everything News"