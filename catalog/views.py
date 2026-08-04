from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic

def index(request):
    """View function for home page of site."""

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()

    search_word = request.GET.get('search_word', '')
    if search_word:
        num_books_containing_word = Book.objects.filter(title__icontains=search_word).count()
    else:
        num_books_containing_word = None

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_containing_word': num_books_containing_word,
        'search_word': search_word,
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    class BookListView(generic.ListView):
      model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author
