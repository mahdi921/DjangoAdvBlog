from django.shortcuts import render
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from blog.models import Post
from django.shortcuts import get_object_or_404
from django.utils import timezone

# Function based view example
'''
def index_view(request):
    # an example of function based view
    context = {
        'name': 'Mahdi1'
    }
    return render(request, 'index.html', context)
'''


class IndexView(TemplateView):
    # an example of class based view using TemplateView built-in class
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['posts'] = Post.objects.filter(status=1, published_date__lte=timezone.now())
        context['name'] = 'Mahdi2'
        return context


# fbv for RedirectView
'''from django.shortcuts import redirect
def redirect_to_mk(request):
    return redirect('https://maktabkhooneh.com/')'''


# an example of class based view using RedirectView built-in class
class RedirectToMk(RedirectView):
    url = 'https://maktabkhooneh.com/'
    

class PostList(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    
