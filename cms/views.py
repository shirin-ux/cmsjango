from django.contrib.auth.decorators import login_required
from django.db.models import ForeignKey
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from cms.forms import CmspostSearchForm
from cms.models import Cmspost, Cmscomment, Shopping
from django.urls import reverse


def cmspost_list(request):
    search_form = CmspostSearchForm(request.GET)
    posts = Cmspost.objects.all()
    if search_form.is_valid():
        posts = posts.filter(name_post__contains=search_form.cleaned_data['name_post'])
        if search_form.cleaned_data['sale_is_open']:
            posts = posts.filter(status=Cmspost.SALE_OPEN)

        min_price, max_price = search_form.get_price_boundries()
        if min_price is not None:
            posts = posts.filter(price_post__gte=min_price)
        if max_price is not None:
            posts = posts.filter(price_post__lte=max_price)

    posts = posts.order_by('date_post')
    count = len(posts)
    context = {
        'post_list': posts,
        'search_form': search_form,
        'post_count': count,

    }
    return render(request, 'cms/post-list.html', context)


def cmscomment_list(request):
    comments = Cmscomment.objects.all()
    context = {
        'comments': comments,
    }
    return render(request, 'cms/comment_list.html', context)


def cmspost_details(request, post_id):
    posts = get_object_or_404(Cmspost, pk=post_id)
    context = {
        'posts': posts,
    }
    if request.method == 'POST':
        try:
            shop_count = int(request.POST['shop_count'])
            assert posts.status == Cmspost.SALE_OPEN, 'فروش اين محصول ممكن نيست '
            assert posts.sales_post >= shop_count, 'كمبود موجودي محصول '
            total_price = posts.price_post * shop_count
            assert request.user.profile.spend(total_price), 'اعتبار شما كافي نيست'
            posts.reserve_shop(shop_count)
            shop = Shopping.objects.create(product=posts, customer=request.user.profile, shop_count=shop_count)
            posts.total_price(total_price)
        except Exception as e:
            context['error'] = str(e)
        else:
            return HttpResponseRedirect(reverse('cms:shopping_list'))

    return render(request, 'cms/post_details.html', context)


def cmscomment_details(request, comment_id):
    comments = get_object_or_404(Cmscomment, pk=comment_id)

    context = {
        'comments': comments,

    }
    return render(request, 'cms/comment_details.html', context)


@login_required
def shopping_list(request):
    shoppings = Shopping.objects.filter(customer=request.user.profile).order_by('-order_time')

    context = {
        'shoppings': shoppings,
    }
    return render(request, 'cms/shopping_list.html', context)


@login_required
def shopping_details(request, shopping_id):
    shopping = Shopping.objects.get(pk=shopping_id)
    context = {
        'shopping': shopping
    }
    return render(request, 'cms/shopping_details.html', context)


