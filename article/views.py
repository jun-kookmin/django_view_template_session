from django.shortcuts import render, redirect
from .models import Article, Comment
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    articles = Article.objects.all().order_by('-created_at')    
    paginator = Paginator(articles, 5)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)  # 해당 페이지에 해당하는 객체들

    return render(request, 'index.html', {'page_obj': page_obj})

def show(request, pk):
    article = Article.objects.get(pk=pk)
    comments = article.comments.all().order_by('-created_at')
    return render(request, 'show.html', {'article': article, 'comments': comments})

def create(request):
    if request.method == 'POST':    
        article = Article()
        article.author = request.user   
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.save()
        return redirect('article:show', pk=article.pk)
    else:
        return render(request, 'new.html')

def update(request, pk):
    article = Article.objects.get(pk=pk)    
    if article.author == request.user:
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.save()
    return redirect('article:show', pk=article.pk)

def edit(request, pk):
    article = Article.objects.get(pk=pk)
    return render(request, 'edit.html', {"article" : article})

def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if article.author == request.user:
        article.delete()
        return redirect('article:index') 
    return redirect('article:show', pk=article.pk)

def create_comment(request, pk):
    if request.method == 'POST':
        comment = Comment()
        comment.article = Article.objects.get(pk=pk)
        comment.author = request.user
        comment.content = request.POST['content']
        comment.save()

    return redirect('article:show', pk=pk)