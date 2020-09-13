from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/details', views.profile_details, name='profile_details'),
    path('payments/list', views.Payments_list, name='payments_list'),
    path('payments/create', views.Payments_create, name='payments_create'),
    path('profile/edit', views.profile_edit, name='profile_edit'),

]
