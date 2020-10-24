from django.urls import path
from .views import (SignUpFormView, LoginFormView,
                    AboutPageView, LogoutView, HomePageView, FileListView )

urlpatterns = [
    path('', AboutPageView.as_view(), name='about'),
    path('signup/', SignUpFormView.as_view(), name='signup'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', HomePageView.as_view(), name='home'),
    path('files/', FileListView.as_view(), name='files'),

]