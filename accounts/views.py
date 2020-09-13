from audioop import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from accounts.forms import PaymentsForm, ProfileForm, MyUserForm
from accounts.models import Payments


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            return HttpResponseRedirect(reverse('cms:Cmspost_list'))

        else:
            context = {
                'username': username,
                'error': 'كاربري با اين مشخصات يافت نشد'
            }
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('cms:Cmspost_list'))
        context = {}
    return render(request, 'accounts/login.html', {})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))


def profile_details(request):
    profile = request.user.profile
    context = {
        'profile': profile
    }
    return render(request, 'accounts/profile_details.html', context)


@login_required
def Payments_list(request):
    payment = Payments.objects.filter(profile=request.user.profile).order_by('-transaction_time')
    context = {
        'payment': payment
    }
    return render(request, 'accounts/payments_list.html', context)


@login_required
def Payments_create(request):
    if request.method == 'POST':
        payments_form = PaymentsForm(request.POST)
        if payments_form.is_valid():
            payments = payments_form.save(commit=False)
            payments.profile = request.user.profile
            payments.save()
            request.user.profile.deposit(payments.amount)
            return HttpResponseRedirect(reverse('accounts:payments_list'))
    else:
        payments_form = PaymentsForm()
    context = {
        'payments_form': payments_form
    }
    return render(request, 'accounts/payments_create.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, files=request.FILES, instance=request.user.profile)
        user_form = MyUserForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return HttpResponseRedirect(reverse('accounts:profile_details'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        user_form = MyUserForm(instance=request.user)

    context = {
        'profile_form': profile_form,
        'user_form': user_form
    }
    return render(request, 'accounts/profile_edit.html', context)
