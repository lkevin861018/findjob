"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include, re_path
from main import views, view2, search, viewjobs
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    re_path(r'^signIn/', views.signIn, name='signIn'),
    re_path(r'^login/', views.login, name='login'),
    re_path(r'^logout/', views.logout, name='logout'),
    re_path(r'^confirm/', views.confirm, name='confirm'),
    re_path(r'^resetconfirm/', views.resetconfirm, name='resetconfirm'),
    re_path(r'^index/', views.index, name='index'),
    re_path(r'^reset/', views.reset, name='reset'),
    re_path(r'^resume_style/', view2.resume_style, name='resume_style'),
    re_path(r'^resume_edit/', view2.resume_edit, name='resume_edit'),
    re_path(r'^resume_save/', view2.resume_save, name='resume_save'),
    re_path(r'^search104/', search.search104, name='search104'),
    re_path(r'^search_hahow/', search.search_hahow, name='search_hahow'),
    re_path(r'^parttime/', viewjobs.parttime, name='parttime'),
    re_path(r'^fulltime/', viewjobs.fulltime, name='fulltime'),
    re_path(r'^joblist/', views.joblist, name='joblist'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
