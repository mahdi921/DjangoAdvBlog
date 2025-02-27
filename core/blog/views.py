# Import necessary modules and classes from Django and the blog app
from django.shortcuts import render
from django.views.generic import (RedirectView, FormView, DetailView, ListView,
                                  TemplateView, CreateView, UpdateView, DeleteView)
from blog.models import Post
from blog.forms import PostForm
from django.shortcuts import get_object_or_404
from django.utils import timezone


# Function based view example (commented out)
'''
def index_view(request):
    # an example of function based view
    context = {
        'name': 'Mahdi1'
    }
    return render(request, 'index.html', context)
'''


# Class based view using TemplateView built-in class
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add custom context data
        # context['posts'] = Post.objects.filter(status=1, published_date__lte=timezone.now())
        context['name'] = 'Mahdi2'
        return context


# Function based view for RedirectView (commented out)
'''from django.shortcuts import redirect
def redirect_to_mk(request):
    return redirect('https://maktabkhooneh.com/')'''


# Class based view using RedirectView built-in class
class RedirectToMk(RedirectView):
    url = 'https://maktabkhooneh.com/'


# Class based view to list all posts
class PostList(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 2


# Class based view to display post details
class PostDetailView(DetailView):
    model = Post


# FormView example for creating a post (commented out)
'''
class PostCreateView(FormView):
    template_name = "contact.html"
    form_class = PostForm
    success_url = "/blog/post/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
'''


# Class based view to create a new post
class PostCreateView(CreateView):
    model = Post
    # Use a form class for the post creation form
    # fields = ['author', 'title', 'content', 'category', 'status', 'published_date']
    form_class = PostForm
    success_url = '/blog/post/'

    def form_valid(self, form):
        # Set the author to the current user
        form.instance.author = self.request.user
        return super().form_valid(form)


# Class based view to edit an existing post
class PostEditView(UpdateView):
    model = Post
    form_class = PostForm
    success_url = '/blog/post/'


# Class based view to delete a post
class PostDeleteView(DeleteView):
    model = Post
    success_url = '/blog/post/'
