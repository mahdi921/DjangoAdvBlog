from django.urls import path
from blog import views
from django.views.generic import TemplateView

app_name = "blog"

urlpatterns = [
    path("fbv", views.index_view, name="fbv-test"),
    # path("cbv", TemplateView.as_view(template_name="index.html")),
    path("cbv", views.IndexView.as_view(), name='cbv-index' )

]