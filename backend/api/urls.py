from django.urls import path
from . import views

urlpatterns = [

    
    path('auth/login/', views.login_view),
    path('auth/logout/', views.logout_view),

    path('counts/', views.get_counts),

    path('news/', views.news_list),
    path('news/create/', views.news_create),
    path('news/<uuid:pk>/', views.news_detail),
    path('news/<uuid:pk>/update/', views.news_update),
    path('news/<uuid:pk>/delete/', views.news_delete),

    path('gallery/', views.gallery_list),
    path('gallery/create/', views.gallery_create),
    path('gallery/<uuid:pk>/', views.gallery_detail),
    path('gallery/<uuid:pk>/update/', views.gallery_update),
    path('gallery/<uuid:pk>/delete/', views.gallery_delete),

    path('slider/', views.slider_list),
    path('slider/create/', views.slider_create),
    path('slider/<uuid:pk>/', views.slider_detail),
    path('slider/<uuid:pk>/update/', views.slider_update),
    path('slider/<uuid:pk>/delete/', views.slider_delete),

    path('topics/', views.topics_list),
    path('topics/create/', views.topics_create),
    path('topics/<uuid:pk>/', views.topics_detail),
    path('topics/<uuid:pk>/update/', views.topics_update),
    path('topics/<uuid:pk>/delete/', views.topics_delete),
]
