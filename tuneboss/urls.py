from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
from tuneboss.views import HomeView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tuneboss.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^facebook/', include('django_facebook.urls')),
    (r'^accounts/', include('django_facebook.auth_urls')),
)

urlpatterns += patterns('tuneboss.views',
    # Spaces
    url(r'^$', 'get_spotify_username', name='home'),
    url(r'^bootstrap$', 'bootstrap', name='bootstrap_example'),
    url(r'^spotify/$', 'spotify', name='spotify_example'),
    url(r'^echonest/$', 'echonest', name='echonest_example'),
    url(r'^home/$', 'get_spotify_username', name='home'),
    url(r'^home_view/$', HomeView.as_view()),
    url(r'^clientlists/(?P<clientlist_id>\d+)/$', 'clientlist', name='clientlist'),
)


