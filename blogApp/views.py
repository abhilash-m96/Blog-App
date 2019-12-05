from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . models import Post
from django.contrib.auth import logout
from django.contrib.auth.models import User

# To use @login reuired on class based views import below
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Blog Home'
    }

    return render(request, 'blogApp/home.html', context)

def about(request):
    return render(request, 'blogApp/about.html', {'title': 'Blog About'})

class PostListView(ListView):
    # To tell which model to interact with
    model = Post
    template_name = 'blogApp/home.html' #<app>/<model>_<viewtype>.html

    context_object_name = 'posts'
    ordering = ['-date_posted']

    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blogApp/user_posts.html' #<app>/<model>_<viewtype>.html

    context_object_name = 'posts'

    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post

    # setting the fields to be created
    fields = ['title', 'content']

    # To use current logged in user as the owner of the post created, override form valid method

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post

    # setting the fields to be edited
    fields = ['title', 'content']

    # To use current logged in user as the owner of the post created, override form valid method

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # To allow only user to only edit his posts:
    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    # To allow only user to only delete his posts:
    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False

def logout_view(request):
    logout(request)
    return render(request, 'blogApp/logout.html')
