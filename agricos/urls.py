from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='home'),
    path('crop_recommend/',views.crop_recommend,name='crop_recommend'),
    path('fertilizer_recommend/',views.fertilizer_recommend, name='fertilizer_recommend'),
]