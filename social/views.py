from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponseRedirect


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
    


class ProfileView(View):
    def get(self, request,pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        followers = profile.followers.all()
        if len(followers) == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        number_of_followers = len(followers)
        posts = Post.objects.filter(author=user)
        context = {
            'user': user,
            'posts': posts,
            'profile': profile,
            'number_of_followers': number_of_followers,
            'is_following': is_following,
        }
        
        return render(request,'social/profile.html',context)



class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name','bio','birth_date', 'location', 'picture']
    template_name = 'social/profile_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})
    
    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user






class AddFollower(LoginRequiredMixin, View):
    def post(self,request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)
        
        return redirect('profile', pk= profile.pk)


class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        
        return redirect('profile', pk= profile.pk)



class Like(LoginRequiredMixin, View):
    def post(self,request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if is_dislike:
            post.dislikes.remove(request.user)
            
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        
        if not is_like:
            post.likes.add(request.user)
        else:
            post.likes.remove(request.user)
        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)


class Dislike(LoginRequiredMixin, View):
    def post(self,request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if is_like:
            post.likes.remove(request.user)
            
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if not is_dislike:
            post.dislikes.add(request.user)
        else:
            post.dislikes.remove(request.user)
        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)
