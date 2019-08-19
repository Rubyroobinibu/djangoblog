from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth.models import auth
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
    
)
from .models import BlogPost

def register(request):
    form=UserCreationForm()

    if request.method == 'POST':
        form=UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username=form.cleaned_data.get('username')
        messages.success(request,"Account created for" +username)
        return redirect("/login")

    return render(request, "register.html", {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
    #if auth success, auth.auth()returns an obj
        user=auth.authenticate(username=username, password=password)

        if user is not None:

    #give permission to user to login
            auth.login(request,user)
            return redirect("/")

        else:
            messages.error(request,"invalid credentials")
            return redirect("login")

    else:
        form= LoginForm()
        return render(request,"login.html",{"form":form})


def logout(request):
# returnHttpResponse("<h1>hi</h1>")
    auth.logout(request)
    return render(request,"logout.html")





def show_home(request):

    blog_list =  BlogPost.objects.all()
    context={'bloglist':blog_list}
    return render(request, 'home.html', context)
    
    

class BlogListView(ListView):
    model = BlogPost
    template_name = 'home.html'
    context_object_name = 'bloglist'
    ordering = ['-blog_date']
    paginate_by=2
    
class BlogProfileView(DetailView):
    model = BlogPost
    template_name = 'blog_profile.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.blog_author:
            return True
        return False

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_detail.html'

    
class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ['blog_title','blog_text']
    template_name = 'blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = BlogPost
    fields = "__all__"
    template_name = 'blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.blog_author:
            return True
        return False

class BlogDeleteView(UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'blog_delete.html'
    success_url = '/'

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.blog_author:
            return True
        return False

    
  
