from django.contrib import admin

from .models import (
    Category,
    Tag,
    Author,
    Article,
    Comment,
    ArticleView,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = (
        "display_name",
        "user",
        "created_at",
    )

    search_fields = (
        "display_name",
        "user__username",
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "author",
        "status",
        "is_featured",
        "is_breaking",
        "is_trending",
        "views",
        "published_at",
    )

    list_filter = (
        "status",
        "category",
        "is_featured",
        "is_breaking",
        "is_trending",
        "published_at",
    )

    search_fields = (
        "title",
        "content",
        "excerpt",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    filter_horizontal = (
        "tags",
    )

    readonly_fields = (
        "views",
        "created_at",
        "updated_at",
    )

    date_hierarchy = "published_at"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        "article",
        "user",
        "is_approved",
        "created_at",
    )

    list_filter = (
        "is_approved",
        "created_at",
    )

    search_fields = (
        "comment",
        "user__username",
        "article__title",
    )


@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):

    list_display = (
        "article",
        "user",
        "ip_address",
        "viewed_at",
    )

    list_filter = (
        "viewed_at",
    )

    search_fields = (
        "article__title",
        "ip_address",
    )

    readonly_fields = (
        "article",
        "user",
        "ip_address",
        "viewed_at",
    )