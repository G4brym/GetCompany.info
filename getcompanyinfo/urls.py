"""getcompanyinfo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Main.views import *
from django.views.generic import TemplateView
from Main.handlers.settings import get_DEBUG
from django.conf.urls import include, url

handler500 = 'Main.views.error500'

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^(?P<nif>[0-9]+)/$', company, name="company"),
    url(r'^c/(?P<nif>[0-9]+)/$', redirectCompany, name="redirect"),
    url(r'^about/$', about, name="about"),
    url(r'^terms/$', terms, name="terms"),
    url(r'^contact/$', contact, name="contact"),

    url(r'^v1/$', v1_req, name="v1"),
    url(r'^v1/docs/$', docs, name="docs"),
    url(r'^v1/(?P<endpoint>[a-z]+)/$', api_req, name="api"),
    url(r'^v1/(?P<endpoint>[a-z]+)/(?P<action>[a-z0-9]+)/$', api_req, name="api"),

    url(r'^sitemap.xml$', sitemapmain, name="sitemapmain"),
    url(r'^companies-(?P<id>[0-9]+).xml$', sitemap_companies, name="sitemap_companies"),
    url(r'^status/$', status, name="status"),
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text')),
]

if get_DEBUG() == True:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))