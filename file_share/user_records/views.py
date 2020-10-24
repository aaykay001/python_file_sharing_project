import os
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

# db imports
from user_records.models import FileInfo

# cloudinary imports
from configparser import ConfigParser
import cloudinary
import cloudinary.uploader
import cloudinary.api
config_file = os.path.join(os.getcwd(), 'config.ini')


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


class HomePageView(LoginRequiredMixin, TemplateView ):
    config = ConfigParser()
    config.read(config_file)
    cloudinary.config(
        cloud_name=config.get('CLOUDINARY', 'cloud_name'),
        api_key=config.get('CLOUDINARY', 'api_key'),
        api_secret=config.get('CLOUDINARY', 'api_secret'),
    )
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        name_of_file = request.FILES['myfile']
        fs = FileSystemStorage()
        # save the file in the specific folder
        saved_file = fs.save(name_of_file.name, name_of_file)
        print(saved_file)
        predicted_details = {}
        return super(TemplateView, self).render_to_response({})


class FileListView(LoginRequiredMixin, TemplateView, ListView):
    model = FileInfo
    template_name = 'FileList.html'
    context_object_name = 'data'
    object_list = FileInfo.objects.filter()
