from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import (ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


def home(request):
    context={
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',context)


#class based view for blog posts

class PostListView(ListView):
    model=Post
    template_name='blog/home.html' #normmal convention for django is <app>/<model>_<viewtype>.html
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5

class UserPostListView(ListView):
    model=Post
    template_name='blog/user_posts.html' #normmal convention for django is <app>/<model>_<viewtype>.html
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5

    def get_queryset(self):
        user= get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
class PostDetailView(DetailView):
    model=Post
    '''
    No need to provide link to template. Class based views conventionally
    look at app_name/model_name_viewtype.html . in this we have provided
    blog/post_detail.html. Similarly we will do for other class based views.
    '''

class PostCreateView(LoginRequiredMixin,CreateView): #Login required mixin is used to check the login status for user to access this page
     model=Post
     fields=['title','content']

     def form_valid(self,form):
         form.instance.author=self.request.user
         return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView): #Login required mixin is used to check the login status for user to access this page
     model=Post
     fields=['title','content']

     def form_valid(self,form):
         form.instance.author=self.request.user
         return super().form_valid(form)

     def test_func(self):
         post=self.get_object() #get object method gets the post we are currently trying to access. this is out of the box function pprovided by Django

         if self.request.user== post.author:
             return True
         return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url='/'
    def test_func(self):
        post=self.get_object() #get object method gets the post we are currently trying to access. this is out of the box function pprovided by Django
        if self.request.user== post.author:
            return True
        return False

def about(request):
    return render(request,'blog/about.html',{'title':'About'})
