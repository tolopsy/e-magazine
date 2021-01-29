from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import  Category, Post, Subscriber
from .forms import CommentForm, SubscriberForm
from django.contrib import messages
from blogman.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404, HttpResponse


# Create your views here.
def home(request):
	featured_post = Post.publishee.filter(featured=True).order_by('order','-publish').distinct()
	most_featured = featured_post.first
	fair_featured = featured_post[1:3]
	least_featured = featured_post[3:]
	category_list = Category.objects.all()
	context = {
		'most_featured': most_featured,
		'fair_featured': fair_featured,
		'least_featured': least_featured,
	}

	if request.method == 'POST':
		subscriber = SubscriberForm(request.POST or None)
		name = str(request.POST['name'])
		if subscriber.is_valid:
			subscriber.save()
			messages.success(request, "You can now get your preferred news sent directly to your mail. Thank you, " + name + " for subscribing.")
	return render(request, 'index.html', context)


def post_detail(request, post_slug, year, month, day):
	post = Post.publishee.get(slug=post_slug, status='published', publish__year=year, publish__month=month, publish__day=day)
	# post = get_object_or_404(Post, slug=post_slug, status='published', publish__year=year, publish__month=month, publish__day=day)
	post.view_count += 1
	post.save()
	featured_post = Post.publishee.filter(featured=True).exclude(id=post.id).order_by('order','-publish').distinct()
	
	tag = post.tags.values_list('id', flat=True)
	similar_post = Post.publishee.filter(tags__in=tag).exclude(id=post.id)
	similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags')[:5]
	comment_list = post.comments.filter(active=True)

	new_comment = None
	#new_form = CommentForm()

	if request.method == 'POST':
		if 'submit' in request.POST:
			comment_form = CommentForm(request.POST or None)
			if comment_form.is_valid():
				new_comment = comment_form.save(commit=False)
				post.comment_count += 1
				post.save()
				new_comment.post = post
				new_comment.save()
			else:
				print('error somewhere')
		elif 'subscribe' in request.POST:
			subscriber = SubscriberForm(request.POST or None)
			name = str(request.POST['name'])
			if subscriber.is_valid:
				subscriber.save()
				messages.success(request, "You can now get your preferred news sent directly to your mail. Thank you, " + name + " for subscribing.")

	context = {
		'post': post,
		'comments': comment_list,
		'new_comment': new_comment,
		#'comment_form': new_form,
		'similar_post': similar_post,
		'featured_post':  featured_post,

	}
	return render(request, 'detail.html', context)


def category(request, slug):
	category = get_object_or_404(Category, slug=slug)
	featured_post = Post.publishee.filter(featured=True).order_by('order','-publish').distinct()

	context = {
		'category': category,
		'featured_post': featured_post,
	}
	if request.method == 'POST':
		subscriber = SubscriberForm(request.POST or None)
		name = str(request.POST['name'])
		if subscriber.is_valid:
			subscriber.save()
			messages.success(request, "You can now get your preferred news sent directly to your mail. Thank you, " + name + " for subscribing.")
	return render(request, 'category.html', context)


def contact(request):
	if request.method == 'POST':
		subject = str(request.POST['subject']) + ' by ' + str(request.POST['email'])
		recipient = 'betolufied@gmail.com'
		name = str(request.POST['name'])
		message = name + ' says: \n' + str(request.POST['message'])
		try:
			send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=True)
			messages.info(request,  "Thank you " + name + '. Your message has been received. We will get back to you.')
		except:
			messages.error(request, "Hi %s, your message was not sent due to bad internet connection. Please, try again or use our contact information in this page to reach us. Thank you.")
	return render(request, 'contact.html')


def search(request):
    search_bin = Post.publishee.all()
    search_word = request.GET.get('search')
    featured_post = Post.publishee.filter(featured=True).order_by('order','-publish').distinct()
    if search_word:
        search_bin = search_bin.filter(Q(title__icontains=search_word) | Q(body__icontains=search_word)).distinct()
    
    context = {
        'post_list': search_bin,
        'search': search_word,
        'featured_post': featured_post,
    }
    if request.method == 'POST':
    	subscriber = SubscriberForm(request.POST or None)
    	name = str(request.POST['name'])
    	if subscriber.is_valid:
    		subscriber.save()
    		messages.success(request, "You can now get your preferred news sent directly to your mail. Thank you, " + name + " for subscribing.")
   
    return render(request, 'search.html', context)


def privacy(request):
	return render(request, 'privacy.html')

def newsmail(request):
	subscriber = Subscriber.objects.get(id=1)
	news = Post.publishee.all()
	context = {'news': news, 'subscriber': subscriber}
	return render(request, 'newsmail.html', context)

def unsubscribe(request, code):
	try:
		subscriber = get_object_or_404(Subscriber, code=code)
		subscriber.subscribe = False
		subscriber.save()
	except Http404:
		context = {'info': 'The link seems broken. \nTo unsubscribe from our newsletter, use the unsubscribe link at the bottom of any of the newsletter emails we have sent to you'}
		return render(request, 'unsubscribe.html', context)

	context = {
	'info': 'You have successfully unsubscribe from our newletter.\nYou will no longer receive newsletter emails from us.',
	'inform': True,
	}
	return render(request, 'unsubscribe.html', context)

'''
def populate(request):
    obj = Post.objects.all()
    for each in obj:
        each.body_i = each.body
        each.save()
    return HttpResponse('Done')
'''