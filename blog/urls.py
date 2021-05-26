from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    #post views
    # path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    #takes 4 arguments and is mapped to the post_detail views
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail') 
    
]