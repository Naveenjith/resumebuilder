
from django.urls import path

from rsmapp import views

urlpatterns = [
    path('',views.index,name='index'),
    path('home/',views.home,name='home'),
    path('create/', views.create_resume, name='create_resume'),
    path('update/<int:pk>/', views.update_resume, name='update_resume'),
    path('view/', views.view_resume, name='view_resume'),
    path('accounts/login/',views.loginview,name="login"),
	path('logout',views.logout_view),
	path('accounts/sign_up/',views.sign_up,name="signup") ,
	path('reset',views.Resethome,name='reset'), 
	path('passwordreset',views.resetPassword,name="passwordreset"),
    path('download/<int:pk>/', views.download_resume, name='download_resume'),

]
