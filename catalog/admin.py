from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Author, Genre, Book, BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'cover_thumbnail')
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


admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)

