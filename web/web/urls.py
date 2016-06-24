"""web URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin

from cluster.views import IndexView, ClusterView, PostingsView, VolumeDataView, VolumeView, TagcloudDataView, TermsDataView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', IndexView.as_view()),
    url(r'^clusters/$', ClusterView.as_view()),
    url(r'^postings/$', PostingsView.as_view()),
    url(r'^volume/$', VolumeView.as_view()),
    url(r'^data/volume/?$', VolumeDataView.as_view()),
    url(r'^data/tagcloud/?$', TagcloudDataView.as_view()),
    url(r'^data/author/?$', TermsDataView.as_view(field='user.screen_name')),
    url(r'^data/hashtags/?$', TermsDataView.as_view(field='entities.hashtags.text')),
    url(r'^data/urls/?$', TermsDataView.as_view(field='entities.urls.expanded_url')),
    url(r'^data/mentions/?$', TermsDataView.as_view(field='entities.user_mentions.screen_name')),
]