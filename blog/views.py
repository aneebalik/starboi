from django.shortcuts import redirect, render
from .models import Post
from .forms import CommentForm

# Create your views here.

def blog_page(request):
    posts = Post.objects.all()
    return render(request, 'blog/blog_page.html', {'posts' : posts})

def blog_details(request,slug):
    post = Post.objects.get(slug=slug)
    if request.method =='POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog_details', slug = post.slug)
    else:
        form = CommentForm()
    return render(request, 'blog/blog_details.html', {'post' : post, 'form':form})
