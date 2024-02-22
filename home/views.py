from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from home.models import Contact,Notes
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    popular_posts = Post.objects.order_by('-views')[:3]
    # context = {'popular_posts': popular_posts}
    files = Notes.objects.all()
    context = {
        'popular_posts': popular_posts,
        'files':files
        }
    
    return render(request, 'home/home.html', context)

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['contact-email']
        phone = request.POST['phone']
        content = request.POST['content']
        
        if len(name)<1 or len(email)<5 or len(phone)<10 or len(content)<5:
            messages.error(request, 'Please fill the form correctly')
        else:    
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, 'Your message was sent')

    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def search(request):
    query = request.GET['query']
    allPostsTitle = Post.objects.filter(title__icontains=query)
    allPostsContent = Post.objects.filter(content__icontains=query)
    allPosts = allPostsTitle.union(allPostsContent)
    params = {'allPosts': allPosts, 'query':query}
    return render(request, 'home/search.html', params)
 

def handleSignup(request):
    if request.method=='POST':
        # Get the parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and number")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Password do not match")
            return redirect('home')


        #create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been successfully created")
        return redirect('home')
    else:
        return HttpResponse("404 - Not Found")


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['pass']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials, Please try again")
            return redirect('home')
    else:
        return HttpResponse("404 - Not Found")

def handleLogout(request):
    logout(request)
    messages.success(request, "You have Logged Out")
    return redirect('home')
