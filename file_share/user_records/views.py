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
from django.conf import settings
from django.db.models import Q

# db imports
from user_records.models import FileInfo
from django.contrib.auth.models import User

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


class HomePageView(LoginRequiredMixin, CreateView):
    config = ConfigParser()
    config.read(config_file)
    cloudinary.config(
        cloud_name=config.get('CLOUDINARY', 'cloud_name'),
        api_key=config.get('CLOUDINARY', 'api_key'),
        api_secret=config.get('CLOUDINARY', 'api_secret'),
    )
    model = FileInfo
    fields = ('file_name', 'description', 'shared_with')
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        name_of_file = request.FILES['myfile']
        fs = FileSystemStorage()
        # save the file in the specific folder
        saved_file = fs.save(name_of_file.name, name_of_file)
        final_path = os.path.join(settings.MEDIA_ROOT, saved_file)
        read_file = open(final_path, 'rb')
        readed_file_obj = read_file.read()
        created_data_obj = cloudinary.uploader.upload(
            readed_file_obj,
            folder="test_folder/",
            public_id=name_of_file.name,
            overwrite=True,
            resource_type="raw"
        )
        # os.remove(final_path)
        save_in_db = FileInfo.objects.create(
            admin_id=request.user.id,
            admin_user_name=request.user.username,
            description=request.POST['description'],
            file_url=created_data_obj['secure_url'],
            file_name=request.POST['file_name'],
        )
        shared_ids = request.POST.getlist('shared_with')
        for i in shared_ids:
            user_obj = User.objects.get(id=int(i))
            save_in_db.shared_with.add(user_obj)
        messages.success(request, "Your file shared successfully !!!")
        return super(HomePageView, self).get(request, *args, **kwargs)


class FileListView(LoginRequiredMixin, TemplateView, ListView):
    model = FileInfo
    template_name = 'FileList.html'
    object_list = FileInfo.objects.filter()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_data'] = FileInfo.objects.filter(Q(admin_id=self.request.user.id) | Q(shared_with__in=[self.request.user]))
        context['my_data_status'] = True if len(context['my_data']) > 0 else False
        return context