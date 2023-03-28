from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Gadget
from .forms import GadgetForm,  RegistrationForm, LoginForm, ContactForm
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from django.core.mail import send_mail

from .serializers import GadgetSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
# Create your views here.

menu = {'Главная': 'index', 'Магазин': 'shop', 'Авторизация': 'log in',
        'Регистрация': 'regis', 'Добавить': 'addgadget', 'Выйти':'log out', 'Корзина':'basket',
        'Обратная связь':'contact_email'}


def index(request):
    cont = {}
    cont['menu'] = menu
    return render(request, 'index.html', context=cont)


class Iphones(ListView):
    model = Gadget
    paginate_by = 4
    template_name = 'shop/shop.html'
    context_object_name = 'phones'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

    def get_queryset(self):
        return Gadget.objects.filter(exist=True)


class MoreInfo(DetailView):
    model = Gadget
    template_name = 'shop/detail.html'
    context_object_name = 'phone'
    pk_url_kwarg = 'key'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context
    

class GadgetAdd(CreateView):
    model = Gadget
    # Определение формы для взаимодействия
    form_class = GadgetForm
    template_name = 'shop/gadget-add.html'
    context_object_name = 'form'  # Переопределение ключа формы
    success_url = reverse_lazy('shop')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context
    
    @method_decorator(permission_required('appltech.add_Gadget'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class GadgetUpdateView(UpdateView):
    model = Gadget
    form_class = GadgetForm
    template_name = 'shop/gadget-edit.html'
    context_object_name = 'form'
    pk_url_kwarg = 'key'
    success_url = reverse_lazy('shop')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context
    
    @method_decorator(permission_required('appltech.change_Gadget'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class GadgetDeleteView(DeleteView):
    model = Gadget
    success_url = reverse_lazy('shop')
    template_name = 'shop/gadget-delete.html'
    context_object_name = 'phone'
    pk_url_kwarg = 'key'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context
    
    @method_decorator(permission_required('appltech.delete_Gadget'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def user_registration(request):
    context = {}
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop')
    else:
        form = RegistrationForm()
        context['form'] = form
        context['menu'] = menu
    return render(request, 'users/registration.html', context=context)


def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('shop')
        else:
            return redirect('log in')
    else:
        form = LoginForm()
        context = {}
        context['form'] = form
        context['menu'] = menu
    return render(request, 'users/login.html', context=context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('log in')


def contact_email(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                settings.EMAIL_HOST_USER,
                ['v.ledovskikh@internet.ru'],
                fail_silently=False
            )
            if mail:
                return redirect('index')
    else:
        form = ContactForm()
        context = {}
        context['form'] = form
        context['menu'] = menu
    return render(request, 'users/email.html', context=context)


@api_view(['GET', 'POST'])
def gadget_api_list(request):
    if request.method == "GET":
        gadget_list = Gadget.objects.all()
        serializer = GadgetSerializer(gadget_list, many=True)
        return Response({'gadget_list': serializer.data})
    elif request.method == "POST":
        serializer = GadgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def gadget_api_detail(request, pk, format=None):
    phone = get_object_or_404(Gadget, pk=pk)
    if phone.exist:
        if request.method == 'GET':
            serializer = GadgetSerializer(phone)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = GadgetSerializer(phone, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Данные успешно изменены', 'phone': serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            phone.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)