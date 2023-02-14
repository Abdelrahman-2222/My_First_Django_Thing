from django.shortcuts import render, get_object_or_404, redirect
from basic_app.models import Post, Comment
from basic_app.forms import PostForm, CommentForm
from django.urls import reverse_lazy
# bdl el decorators fe el function based view
from django.contrib.auth.mixins import LoginRequiredMixin
# d2 el decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.utils import timezone


# Create your views here.

class AboutView(TemplateView):
    template_name = 'basic_app/about.html'


# class NewPage(TemplateView):
#     template_name = 'basic_app/comment_detail.html'

# class NewPage(TemplateView, DetailView):
#     model = Post
#     template_name = 'basic_app/comment_detail.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        # SELECT * FROM Post WHERE publication_date order_by publication_date;
        return Post.objects.filter(publication_date__lte=timezone.now()).order_by('-publication_date')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class UpdatePostView(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(publication_date__isnull=True).order_by('creation_date')


########################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'basic_app/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


# def ninja_view(request):
#     # creating a dictionary
#     # for post in Post.approve_comments.count:
#     context = {
#         "data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
#     }
#     # returning response
#     return render(request, "basic_app/post_list.html", context)

def my_view(request):
    my_integers = [1, 2, 3, 4, 5]
    context = {'my_integers': my_integers}
    return render(request, 'basic_app/post_list.html', context)


def comment_detail(request, pk, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    return render(request, 'basic_app/comment_detail.html', {'comment': comment})
