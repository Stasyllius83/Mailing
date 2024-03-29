from pytils.translit import slugify
from django.urls import reverse, reverse_lazy
from blog.models import Blog
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from blog.services import get_cached_blogs
from django.views.decorators.cache import cache_page

class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blog/blogs_list.html'


    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = get_cached_blogs()
        return context_data


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Blog
    fields = ('title', 'content', 'preview', 'date_create', 'is_published', 'author')
    permission_required = 'blog.add_blog'
    success_url = reverse_lazy('blog:blogs_list')

    def form_valid(self, form):
        slug = slugify(form.cleaned_data['title'])
        if self.model.objects.filter(slug=slug).exists():
            form.add_error('title', 'Пост с таким slug уже существует')
            return self.form_invalid(form=form)

        return super().form_valid(form)



class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Blog
    fields = ('title', 'content', 'preview', 'date_create', 'is_published',)
    permission_required = 'blog.change_blog'

    def form_valid(self, form):
        if form.is_valid:
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view_blog', args= [self.kwargs.get('pk')])


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()

        return self.object


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blogs_list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perms(['blog.delete_blog'])
