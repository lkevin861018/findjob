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
from main import views, search, viewjobs
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
    re_path(r'^resume_style/', views.resume_style, name='resume_style'),
    re_path(r'^resume_edit/', views.resume_edit, name='resume_edit'),
    re_path(r'^resume_save/', views.resume_save, name='resume_save'),
    re_path(r'^search104/', viewjobs.search104, name='search104'),
    re_path(r'^search_hahow/', search.search_hahow, name='search_hahow'),
    re_path(r'^parttime/', viewjobs.parttime, name='parttime'),
    re_path(r'^fulltime/', viewjobs.fulltime, name='fulltime'),
    re_path(r'^joblist/', views.joblist, name='joblist'),

    re_path(r'^company_signIn/', views.company_signIn, name='company_signIn'),
    re_path(r'^company_confirm/', views.company_confirm, name='company_confirm'),
    re_path(r'^companyjobs_edit/', views.companyjobs_edit,
            name='companyjobs_edit'),
    re_path(r'^companyjobs_save/', views.companyjobs_save,
            name='companyjobs_save'),
    re_path(r'^partnerjobs/', views.partnerjobs, name='partnerjobs'),
    re_path(r'^search_book/', search.search_tenlong,
            name='search_book'),
    re_path(r'^govresource/', search.govresource, name='govresource'),
    re_path(r'^info_reset/', views.info_reset, name='info_reset'),
    re_path(r'^info_resetconfirm/', views.info_resetconfirm,
            name='info_resetconfirm'),
    re_path(r'^shoppingr/', search.shoppingr, name='shoppingr'),
    re_path(r'^shopping/', search.shopping, name='shopping'),
    re_path(r'^shoplist/', search.shoplist, name='shoplist'),

    re_path(r'^applyrecord/', views.applyrecord, name='applyrecord'),
    re_path(r'^apply/', views.apply, name='apply'),
    re_path(r'^partnerresumes/', views.partnerresumes, name='partnerresumes'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
