from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, ArchiveIndexView, YearArchiveView, CreateView, UpdateView, \
    DeleteView
from .models import Post
from .forms import PostForm


# @login_required
# def post_new(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # post = form.save()
#             post = form.save(commit=False)
#             post.author = request.user  # 현재 로그인 User Insatance
#             post.save()
#             messages.success(request, '포스팅을 저장 했습니다.')
#
#             return redirect(post)
#     else:
#         form = PostForm()
#
#     return render(request, 'instagram/post_form.html', {
#         'form': form,
#         'post': None,
#     })

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        messages.success(self.request, '포스팅을 저장 하였습니다.')
        return super().form_valid(form)


post_new = PostCreateView.as_view()


# @login_required
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     if post.author != request.user:
#         messages.error(request, '작성자만 수정 가능합니다.')
#         return redirect(post)
#
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             post = form.save()
#             messages.success(request, '포스팅을 수정 했습니다.')
#             return redirect(post)
#     else:
#         form = PostForm(instance=post)
#
#     return render(request, 'instagram/post_form.html', {
#         'form': form,
#         'post': post,
#     })

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        messages.success(self.request, '포스팅을 수정 했습니다.')
        return super().form_valid(form)


post_edit = PostUpdateView.as_view()


# @login_required
# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         post.delete()
#         messages.success(request, '포스팅을 삭제 하였습니다.')
#         return redirect('instagram:post_list')
#     return render(request, 'instagram/post_confirm_delete.html', {
#         'post': post,
#     })

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    # success_url = reverse('instagram:post_list')
    # success_url = reverse_lazy('instagram:post_list')
    def get_success_url(self):
        return reverse('instagram:post_list')

post_delete = PostDeleteView.as_view()


# post_list = login_required(ListView.as_view(model=Post, paginate_by=10))

# @method_decorator(login_required, name='dispatch')
# class PostListView(ListView):

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10


post_list = PostListView.as_view()

# @login_required
# def post_list(request):
#     # request.GET
#     # request.POST
#     # request.FILES
#     qs = Post.objects.all()
#     q = request.GET.get('q', '')
#
#     if q:
#         qs = qs.filter(message__icontains=q)
#
#     # instagram/templates/instagram/post_list.html
#     return render(request, 'instagram/post_list.html', {
#         'post_list': qs,
#         'q': q,
#     })


# def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
#     # try:
#     #     post = Post.objects.get(pk=pk)
#     # except:
#     #     raise Http404
#     post = get_object_or_404(Post, pk=pk)
#
#     return render(request, 'instagram/post_detail.html', {
#         'post': post,
#     })
# post_detail = DetailView.as_view(model=Post)

# post_detail = DetailView.as_view(
#     model=Post,
#     queryset=Post.objects.filter(is_public=True)
# )

class PostDetailView(DetailView):
    model = Post
    # queryset = Post.objects.filter(is_public=True)

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_public=True)

        return qs


post_detail = PostDetailView.as_view()


# def archives_year(request, year):
#     return HttpResponse(f"{year} !!")

post_archive = ArchiveIndexView.as_view(model=Post, date_field='created_at', paginate_by=10)

post_archive_year = YearArchiveView.as_view(model=Post, date_field='created_at', make_object_list=True)