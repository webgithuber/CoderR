from django.urls import path , include
from chatapp import views as chatapp_views
app_name = "chatapp"
urlpatterns = [
    path('home/',chatapp_views.home , name='home'),
    path('register/',chatapp_views.register_request , name='register'),
    path('login/',chatapp_views.login_request , name='login'),
    path('logout/',chatapp_views.logout_request , name='logout'),
    path('<str:id>/',chatapp_views.index , name='index'),
    path('join',chatapp_views.join , name='join'),
    path('',chatapp_views.create_new , name='create_new'),
    
    


]