import markdown
from django.shortcuts import render, get_object_or_404
from comments.forms import CommentForm
from .models import Post, Category
from django.views.generic import ListView

# def index(request):
#   post_list = Post.objects.all()
#   return render(request, 'blog/index.html', context={'post_list': post_list})

class IndexView(ListView):
  model = Post
  template_name = 'blog/index.html'
  context_object_name = 'post_list'

def detail(request, pk):
  post = get_object_or_404(Post, pk=pk)
  post.increase_view()
  post.body = markdown.markdown(post.body,
                                extensions=[
                                  'markdown.extensions.extra',
                                  'markdown.extensions.codehilite',
                                  'markdown.extensions.toc',
                                ])
  form = CommentForm()
  comment_list = post.comment_set.all()
  context = { 'post': post,
              'form': form,
              'comment_list': comment_list
            }
  return render(request, 'blog/detail.html', context=context)

# def archives(request, year, month):
#   post_list = Post.objects.filter(created_time__year=year,
#                                   created_time__month=month
#                                   )
#   return render(request, 'blog/index.html', context={'post_list': post_list})

class ArchivesView(ListView):
  model = Post
  template_name = 'blog/index.html'
  context_object_name = 'post_list'

  def get_queryset(self):
    year = self.kwargs.get('year')
    month = self.kwargs.get('month')
    return super(ArchivesView, self).get_queryset().filter(created_time_year=year,
                                                           created_time_month=month)

# def category(request, pk):
#   cate = get_object_or_404(Category, pk=pk)
#   post_list = Post.objects.filter(category=cate)
#   return render(request, 'blog/index.html', context={'post_list': post_list})

class CategoryView(IndexView):
  def get_queryset(self):
    cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
    return super(CategoryView, self).get_queryset().filter(category=cate)
