from django.urls import path
from blog import views
from django.views.generic import TemplateView
from django.views.generic import RedirectView

app_name = "blog"

urlpatterns = [
    path("cbv", views.IndexView.as_view(), name='cbv-index'),
    path('post/', views.PostList.as_view(), name='post-list'),
    path("go-to-mk/<int:pk>", views.RedirectToMk.as_view(), name="go-to-mk"),
]
