from django import forms

from .models import Comment, Subscriber, Category


class  CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['name', 'email', 'body']


class SubscriberForm(forms.ModelForm):
	class Meta:
		model = Subscriber
		fields = ['name', 'email', 'preferences']