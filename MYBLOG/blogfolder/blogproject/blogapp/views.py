from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
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
        request.session['username'] = username
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

def show_myposts(request):
    user=User.objects.get(username=request.session['username'])
    print(user.username)
    user=User.objects.get(username=user.username)
    myblog_list = BlogPost.objects.filter(blog_author=user.pk) 
    context={'mybloglist':myblog_list}
    return render(request, 'blog_myposts.html', context)
    

class BlogMyListView(ListView):
    model = BlogPost
    template_name = 'blog_myposts.html'
    context_object_name = 'mybloglist'
    paginate_by=2
    ordering = ['-blog_date']




def show_home(request):

    blog_list =  BlogPost.objects.all()
    print(blog_list)
    context={'bloglist':blog_list}
    return render(request, 'home.html', context)
    
    

class BlogListView(ListView):
    model = BlogPost
    template_name = 'home.html'
    context_object_name = 'bloglist'
    ordering = ['-blog_date']
    paginate_by=2
    
class BlogProfileView(DetailView):
    model = User
    template_name = 'blog_profile.html'
    fields = "__all__" 

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
    fields = ['blog_title','blog_text','blog_date']
    template_name = 'blog_form.html'

    def form_valid(self, form):
        form.instance.blog_author = self.request.user
        return super().form_valid(form)

    
    
class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = BlogPost
    fields = ['blog_title','blog_text']
    template_name = 'blog_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)
    
    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.blog_author:
            return True
        return False


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'blog_delete.html'
    success_url = '/'
    
    
    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.blog_author:
            print(obj.blog_author)
            print(self.request.user )
            return True
        return False

    
  
