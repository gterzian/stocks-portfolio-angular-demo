from django.conf.urls import patterns, include, url


from portfolio import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'feigou.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^user/$', views.get_user, ),
    url(r'^new_transaction/$', views.new_transaction, ),
 
   
)
