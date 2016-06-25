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

from cluster.views import IndexView, ClusterDataView, VolumeDataView,\
    TagcloudDataView, TermsDataView, PostingsDataView, ReachDataView,\
    OwnOtherVolumeDataView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', IndexView.as_view()),
    url(r'^data/volume/?$', VolumeDataView.as_view()),
    url(r'^data/own_other/?$', OwnOtherVolumeDataView.as_view()),
    url(r'^data/reach/?$', ReachDataView.as_view()),
    url(r'^data/tagcloud/?$', TagcloudDataView.as_view()),
    url(r'^data/author/?$', TermsDataView.as_view(field='user.screen_name')),
    url(r'^data/hashtags/?$', TermsDataView.as_view(field='entities.hashtags.text')),
    url(r'^data/urls/?$', TermsDataView.as_view(field='entities.urls.expanded_url')),
    url(r'^data/mentions/?$', TermsDataView.as_view(field='entities.user_mentions.screen_name')),
    url(r'^data/postings/?$', PostingsDataView.as_view()),
    url(r'^data/clusters/?$', ClusterDataView.as_view()),
]
