from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Author, Genre, Book, BookInstance


@admin.register(Book)  # admin.site.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'cover_thumbnail')
    readonly_fields = ('cover_preview',)

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


admin.site.register(Author)  # admin.site.register(Author)
# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
        list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance)  # admin.site.register(BookInstance)

