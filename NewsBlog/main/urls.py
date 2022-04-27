from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns=[
    path("",views.register,name='register'),
    path("login",views.login,name='login'),
    path("home",views.home,name='home'),
    path("dashboard",views.dashboard,name="dashboard"),
    path("createblog",views.createblog,name="createblog"),
    path('Delete_blog/<int:id>',views.Delete_blog,name='Delete_blog'),
    path('view/<int:id>',views.view,name='view'),
    path('view/dashboard',views.dash1,name='dash1'),
    path('view/home',views.home1,name="home1"),
    path('view/createblog',views.cr1,name='cr1'),
    path('admin_post',views.post_list),
    path('admin_post_detail/<int:id>',views.post_detail),
    path('logout',views.logout,name='logout'),
    #path('edit_blog/<int:id>',views.edit_blog,name='edit_blog'),
    #path("edit_blog/save",views.save,name="save"),
]
urlpatterns=format_suffix_patterns(urlpatterns)