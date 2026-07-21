from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Article, ArticleView, Category


def home(request):

    featured_articles = Article.objects.filter(
        status="published",
        is_featured=True
    ).select_related(
        "category",
        "author"
    )[:5]

    breaking_articles = Article.objects.filter(
        status="published",
        is_breaking=True
    ).select_related(
        "category",
        "author"
    ).order_by(
        "-published_at",
        "-created_at"
    )[:10]

    latest_articles = Article.objects.filter(
        status="published"
    ).select_related(
        "category",
        "author"
    ).order_by(
        "-published_at",
        "-created_at"
    )[:12]

    trending_articles = Article.objects.filter(
        status="published",
        is_trending=True
    ).select_related(
        "category",
        "author"
    ).order_by(
        "-views"
    )[:5]

    categories = Category.objects.all()

    context = {
        "featured_articles": featured_articles,
        "breaking_articles": breaking_articles,
        "latest_articles": latest_articles,
        "trending_articles": trending_articles,
        "categories": categories,
    }

    return render(
        request,
        "home/home.html",
        context
    )


def article_detail(request, slug):

    article = get_object_or_404(
        Article.objects.select_related(
            "category",
            "author"
        ).prefetch_related(
            "tags"
        ),
        slug=slug,
        status="published"
    )

    Article.objects.filter(
        id=article.id
    ).update(
        views=article.views + 1
    )

    article.views += 1

    ip_address = request.META.get(
        "HTTP_X_FORWARDED_FOR"
    )

    if ip_address:
        ip_address = ip_address.split(",")[0].strip()
    else:
        ip_address = request.META.get(
            "REMOTE_ADDR"
        )

    ArticleView.objects.create(
        article=article,
        user=(
            request.user
            if request.user.is_authenticated
            else None
        ),
        ip_address=ip_address
    )

    related_articles = Article.objects.filter(
        status="published",
        category=article.category
    ).exclude(
        id=article.id
    ).select_related(
        "category",
        "author"
    ).order_by(
        "-published_at"
    )[:4]

    categories = Category.objects.all()

    context = {
        "article": article,
        "related_articles": related_articles,
        "categories": categories,
    }

    return render(
        request,
        "news/article_detail.html",
        context
    )


def search(request):

    query = request.GET.get(
        "q",
        ""
    ).strip()

    articles = Article.objects.filter(
        status="published"
    ).select_related(
        "category",
        "author"
    )

    if query:

        articles = articles.filter(

            Q(title__icontains=query)
            |
            Q(excerpt__icontains=query)
            |
            Q(content__icontains=query)
            |
            Q(category__name__icontains=query)
            |
            Q(tags__name__icontains=query)

        ).distinct()

    articles = articles.order_by(
        "-published_at",
        "-created_at"
    )

    categories = Category.objects.all()

    context = {
        "articles": articles,
        "query": query,
        "categories": categories,
    }

    return render(
        request,
        "news/search.html",
        context
    )


def category(request, slug):

    category_obj = get_object_or_404(
        Category,
        slug=slug
    )

    articles_list = Article.objects.filter(
        status="published",
        category=category_obj
    ).select_related(
        "category",
        "author"
    ).order_by(
        "-published_at",
        "-created_at"
    )

    paginator = Paginator(
        articles_list,
        10
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    breaking_articles = Article.objects.filter(
        status="published",
        is_breaking=True
    ).select_related(
        "category",
        "author"
    ).order_by(
        "-published_at",
        "-created_at"
    )[:10]

    trending_articles = Article.objects.filter(
        status="published",
        is_trending=True
    ).select_related(
        "category",
        "author"
    ).order_by(
        "-views"
    )[:5]

    categories = Category.objects.all()

    context = {
        "category": category_obj,
        "articles": page_obj,
        "page_obj": page_obj,
        "breaking_articles": breaking_articles,
        "trending_articles": trending_articles,
        "categories": categories,
    }

    return render(
        request,
        "news/category.html",
        context
    )