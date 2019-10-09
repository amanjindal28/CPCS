from django.urls import path
from .views import SignUpCreateView,CreateStudentView,SuccessView,RecordsListView
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
	path('',CreateStudentView.as_view(),name='home'),
	path('records/',RecordsListView.as_view(),name='records'),
	path('success/',SuccessView.as_view(),name='success'),
	path('signup/',SignUpCreateView.as_view(),name='signup'),
	path('login/',LoginView.as_view(),name='login'),
	path('logout/',LogoutView.as_view(template_name='thankyou.html'),name='logout'),

]
