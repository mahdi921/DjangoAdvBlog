# Import necessary modules and classes from Django and the blog app
from django.contrib.postgres.search import (
    SearchVector,
    # Weighted search modules
    # SearchQuery,
    # SearchRank,
    TrigramSimilarity,
)
from django.views.generic import (
    RedirectView,
    DetailView,
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views import View
from blog.models import Post
from blog.forms import PostForm, SearchForm
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.shortcuts import render

# Function based view example (commented out)
"""
def index_view(request):
    # an example of function based view
    context = {
        'name': 'Mahdi1'
    }
    return render(request, 'index.html', context)
"""


# Class based view using TemplateView built-in class
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add custom context data
        context["name"] = "Mahdi2"
        return context


# Function based view for RedirectView (commented out)
"""from django.shortcuts import redirect
def redirect_to_mk(request):
    return redirect('https://maktabkhooneh.com/')"""


# Class based view using RedirectView built-in class
class RedirectToMk(RedirectView):
    url = "https://maktabkhooneh.com/"


# Class based view to list all posts
class PostListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "blog.view_post"
    queryset = Post.objects.all()
    context_object_name = "posts"
    paginate_by = 2


# Class based view to display post details
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


# FormView example for creating a post (commented out)
"""
class PostCreateView(FormView):
    template_name = "contact.html"
    form_class = PostForm
    success_url = "/blog/post/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
"""


# Class based view to create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # Use a form class for the post creation form
    form_class = PostForm
    success_url = "/blog/post/"

    def form_valid(self, form):
        # Set the author to the current user
        form.instance.author = self.request.user
        return super().form_valid(form)


# Class based view to edit an existing post
class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/post/"


# Class based view to delete a post
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/blog/post/"


# function based view to utilize postgres' search module
def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # weighted search
            # search_vector = SearchVector('title', weight='A'
            #                              ) + SearchVector(
            #                                  'content', weight='B')
            # search=search_vector,
            # rank=SearchRank(search_vector, search_query),
            # filter(rank__gte=0.3)
            # search_query = SearchQuery(query)
            results = Post.objects.annotate(
                # trigram search
                similarity=TrigramSimilarity('title', query)
            ).filter(similarity__gt=0.1).order_by('-similarity')
    return render(
        request,
        'blog/post_search.html',
        {
            'form': form,
            'query': query,
            'results': results
        }
    )


# this was to test cbv search
class TestView(View):
    template_name = "blog/post_search.html"
    form_class = SearchForm

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            return Post.objects.annotate(
                search=SearchVector('title', 'content'),
            ).filter(search=query)
