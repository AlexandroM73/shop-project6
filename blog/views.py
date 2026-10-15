from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    # Задание 3: фильтрация только опубликованных статей
    def get_queryset(self):
        return Post.objects.filter(is_published=True)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    # Задание 3: увеличение счётчика просмотров
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        # update_fields ускоряет обновление и не трогает другие поля
        obj.save(update_fields=['views_count'])
        return obj

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    # Задание 3: перенаправление на просмотр статьи после редактирования
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
