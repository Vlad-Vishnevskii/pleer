# -*- coding: utf-8 -*-
import json

from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView

from .models import *
from .services import open_file
from .forms import AuthUserForm, RegisterUserForm
from django.views import View
from django.db import transaction
import random
from datetime import datetime

from django.db.models.functions import Now
import os
from django.views.decorators.csrf import ensure_csrf_cookie
import math
from PIL import Image
import numpy
import moviepy.editor as mp
from moviepy.editor import *



def get_list_video(request):
    # video_list = Video.objects.order_by('-likes')[:10]
    random_items = list(Video.objects.all())
    #if len(random_items) > 1:
    video_list = random.sample(random_items, 1)
    #elif len(random_items) > 5:
        #video_list = random.sample(random_items, 5)
   

    context = {
        'video_list': video_list
    }

    return render(request, 'video_hosting/test_home.html', context)

    
    



def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response
    
class CustomSuccessMessageMixin:
    
    @property
    def success_msg(self):
        return False
    
    def form_valid(self,form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)
        
    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)
        
        
# view profile

        


class MyprojectLoginView(LoginView):
    template_name = 'video_hosting/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('createmusic')
    def get_success_url(self):
        return self.success_url
    
class RegisterUserView(CreateView):
    model = User
    template_name = 'video_hosting/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('createmusic')
    success_msg = 'Пользователь успешно создан'
    
    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        create_wallet(username)
        return form_valid
        

class MyprojectLogoutView(LogoutView):
    next_page = reverse_lazy('home')
    
class AddLike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        post = Video.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break


        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        return HttpResponseRedirect(reverse('videomain', args=[str(pk)]))



class AddDislike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        post = Video.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)



        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        return HttpResponseRedirect(reverse('videomain', args=[str(pk)]))
        




