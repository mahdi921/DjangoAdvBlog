from django.shortcuts import render
from django.views.generic.base import TemplateView
from blog.models import Post
from django.utils import timezone

def index_view(request):
    # an example of function based view
    context = {
        'name': 'Mahdi1'
    }
    return render(request, 'index.html', context)

class IndexView(TemplateView):
    # an example of class based view using TemplateView built-in class
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['posts'] = Post.objects.filter(status=1, published_date__lte=timezone.now())
        context['name'] = 'Mahdi2'
        return context