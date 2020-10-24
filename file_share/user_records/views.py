from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.views.generic import RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from user_records.models import FileInfo


class AboutPageView(TemplateView):
    template_name = 'about.html'


class SignUpFormView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    success_message = "You account created successfully !!!"
    success_url = reverse_lazy('user_app:login')
    template_name = 'signup.html'


class LoginFormView(SuccessMessageMixin, LoginView):
    success_message = "You were successfully logged IN !!!"
    template_name = 'login.html'

    def get_redirect_url(self):
        redirect_to = reverse_lazy('user_app:home')
        return redirect_to


class LogoutView(RedirectView):
    url = reverse_lazy('user_app:login')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You were successfully logged OUT !!!")
        return super(LogoutView, self).get(request, *args, **kwargs)


class HomePageView(TemplateView):
    template_name = 'index.html'


class FileListView(TemplateView, ListView):
    model = FileInfo
    template_name = 'FileList.html'
    context_object_name = 'data'
    object_list = FileInfo.objects.filter()
