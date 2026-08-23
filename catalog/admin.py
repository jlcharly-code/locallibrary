from django.contrib import admin
from django.utils.html import format_html

from .models import Author, Genre, Book, BookInstance


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'cover_thumbnail')
    readonly_fields = ('cover_preview',)
    inlines = [BooksInstanceInline]

    def cover_thumbnail(self, obj):
        """Petite miniature affichée dans la liste des livres."""
        if obj.cover_image:
            return format_html('<img src="{}" style="height: 50px;" />', obj.cover_image.url)
        return "—"
    cover_thumbnail.short_description = 'Couverture'

    def cover_preview(self, obj):
        """Aperçu plus grand affiché dans la fiche détail du livre."""
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height: 300px;" />', obj.cover_image.url)
        return "Aucune image"
    cover_preview.short_description = 'Aperçu de la couverture'


class BooksInline(admin.TabularInline):
    model = Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death', 'bio')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death'), 'bio']
    inlines = [BooksInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)