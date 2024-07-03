from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.core.serializers import serialize
import json
from .models import Book

def book_list(request):
    if request.method == "GET":
        books = Book.objects.all()
        books_json = serialize('json', books)
        return HttpResponse(books_json, content_type='application/json')
    elif request.method == "POST":
        data = json.loads(request.body)
        book = Book.objects.create(
            title=data['title'],
            author=data['author'],
            published_date=data['published_date']
        )
        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'published_date': book.published_date
        }, status=201)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

    if request.method == "GET":
        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'published_date': book.published_date
        })
    elif request.method == "PUT":
        data = json.loads(request.body)
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.published_date = data.get('published_date', book.published_date)
        book.save()
        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'published_date': book.published_date
        })
    elif request.method == "DELETE":
        book.delete()
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])
