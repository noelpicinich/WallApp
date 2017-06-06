# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Post
from .forms import PostForm, SignUpForm

def signup(request):
    """
    This method is from https://simpleisbetterthancomplex.com/tutorial/
    2017/02/18/how-to-create-user-sign-up-view.html
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            subject = 'Welcome to The Wall!'
            message = render_to_string('wall/welcome_email.html', {'user': user,})
            user.email_user(subject, message)
            return redirect('../home')
    else:
        form = SignUpForm()
    return render(request, 'wall/signup.html', {'form': form})


def home(request):
    return render(request, 'wall/home.html')

def post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('../home')
    else:
        form = PostForm()
    return render(request, 'wall/newpost.html', {'form': form})


class IndexView(generic.ListView):
    template_name = 'wall/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Post.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Post
    template_name = 'wall/detail.html'

    def get_queryset(self):
        """
        Excludes any posts that aren't published yet.
        """
        return Post.objects.filter(pub_date__lte=timezone.now())
