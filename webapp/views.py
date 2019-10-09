from django.shortcuts import render
from django.views.generic import CreateView,TemplateView,ListView
from .forms import UserCreateForm,CreateStudentForm
from django.urls import reverse_lazy
from .models import CreateStudentModel
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class SignUpCreateView(CreateView):

	form_class = UserCreateForm
	success_url = reverse_lazy('login')
	template_name = 'webapp/signup.html'


class CreateStudentView(LoginRequiredMixin,CreateView):
	login_url = '/login/'
	form_class = CreateStudentForm
	template_name = 'webapp/create.html'
	success_url = '/success'


class SuccessView(TemplateView):
	template_name = 'success.html'


class RecordsListView(ListView):
	model = CreateStudentModel

	template_name = 'webapp/records.html'

	def get_queryset(self):
		return CreateStudentModel.objects.all()


