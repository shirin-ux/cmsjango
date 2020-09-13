from django.urls import path
from cms import views

app_name = 'cms'
urlpatterns = [

    path('Cmspost/list/', views.cmspost_list, name='Cmspost_list'),

    path('Cmspost/details/<int:post_id>/', views.cmspost_details, name='Cmspost_details'),

    path('Cmscomment/list/', views.cmscomment_list, name='Cmscomment_list'),

    path('Cmscomment/details/<int:comment_id>/', views.cmscomment_details, name='Cmscomment_details'),

    path('Shopping/list/', views.shopping_list, name='shopping_list'),

    path('Shopping/datials/<int:shopping_id>/', views.shopping_details, name='shopping_details'),

]
