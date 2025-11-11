from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment, Tag
from django.contrib.auth import authenticate, login, logout
from .forms import Post_Form, Comment_form
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from . forms import Update_Profile_forms
from django.contrib.auth.decorators import login_required


def Post_list(request):
    categoryQ = request.GET.get('Category')
    tagQ = request.GET.get('tag')
    searchQ = request.GET.get('searchQ')

    posts = Post.objects.all()

    if categoryQ:
        posts = posts.filter(category__name=categoryQ)
    if tagQ:
        posts = posts.filter(tags__name=tagQ)   
    if searchQ:
        posts = posts.filter(
            Q(title__icontains=searchQ)
            | Q(content__icontains=searchQ)
            | Q(tags__name__icontains=searchQ)
            | Q(category__name__icontains=searchQ)
        ).distinct()

    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    context = {
        'page_object': page_object,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'search_query': searchQ,
        'category_query': categoryQ,
        'tag_query': tagQ,
    }
    return render(request, 'blog/post_list.html', context)

@login_required
def post_details(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        comment_form = Comment_form(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user

            comment.save()
            return redirect('post_details', id=post.id)
    else:
        comment_form = Comment_form()

    comments = post.comment_set.all()
    is_liked = post.like_users.filter(id=request.user.id).exists()
    like_count = post.like_users.count()

    context = {
        'post': post,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': is_liked,
        'like_count': like_count
    }

    post.view_count += 1
    post.save()

    return render(request, 'blog/post_details.html', context)


@login_required
def Post_like(request, id):
    post = get_object_or_404(Post, id=id)
    if post.like_users.filter(id=request.user.id).exists():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    return redirect('post_details', id=post.id)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = Post_Form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # fixed "auther" spelling
            post.save()
            return redirect('Post_list')
    else:
        form = Post_Form()
    return render(request, 'blog/post_create.html', {'form': form})

@login_required
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = Post_Form(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_details', id=post.id)
    else:
        form = Post_Form(instance=post)
    return render(request, 'blog/post_create.html', {'form': form})


@login_required
def Post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('Post_list')


# def signup_view(request):
#     if request.method =='POST':
#         form =UserCreationForm(request.POST)
#         if form.is_valid():
#             user= form.save()
#             login(request, user)
#             return redirect ('Post_list')
#         else:
#             form = UserCreationForm()
#         return render(request,'user/signup.html',{'form' : form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Post_list')
    else:
        form = UserCreationForm()
    return render(request, 'user/signup.html', {'form': form})

@login_required   
def profile_view(request):
    section= request.GET.get('section', 'profile')
    context = {
        'section' : section
    }
    if section == "posts":
        posts = Post.objects.filter(author=request.user)
        context['posts']=posts   
    elif section == 'update':
        if request.method == 'POST':
            form = Update_Profile_forms(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('/profile?section=update')
        else:
            form = Update_Profile_forms(instance=request.user)

        context['form'] = form
    return render(request, 'user/profile.html', context)
