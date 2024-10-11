from django.urls import path
from . import views


urlpatterns = [
    path('delete/<int:id>/',views.delete,name='delete'),
     path('delete_comment/<int:id>/',views.delete_comment,name='delete_comment'),

    path('signup/',views.signup,name='signup'),
    path('login/',views.signin,name='singin'),
    path('profile/',views.profile,name='profile'),
    path('viewcomment/', views.view_to_comment, name='view_to_comment'),
      
    
]
