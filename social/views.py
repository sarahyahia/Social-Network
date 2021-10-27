from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView

class PostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        form = PostForm()
        
        context ={
            'posts': posts,
            'form': form,
        }
        return render(request,'social/post_list.html', context)
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            # messages.add_message(request, messages.SUCCESS,'')
        posts = Post.objects.all()
        context ={
            'posts': posts,
            'form': form,
        }
        return render(request,'social/post_list.html', context)
    





class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        form = CommentForm()
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        
        context ={
            'post': post,
            'comments': comments,
            'form': form,
        }
        return render(request,'social/post_details.html',context)

    
    def post(self, request, pk, *args, **kwargs):
        form= CommentForm(request.POST)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = Post.objects.get(pk=pk)
            new_comment.save()
        
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.all()
        context ={
            'post': post,
            'comments': comments,
            'form': form,
        }
        return render(request,'social/post_details.html',context)
    


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author



class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'
    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author