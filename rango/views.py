from django.shortcuts import render
from rango.models import Category
from django.http import HttpResponse
from rango.models import Page
from rango.forms import CategoryForm
def index(request):
    page_list = Page.objects.order_by('-views')[:5]
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'pages': page_list, 'categories': category_list}
    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict = {'wer': 'Новая картинка!!!'}
    return  render(request, 'rango/about.html', context_dict)


def category(request,category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    # HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Все поля формы были заполнены правильно?
        if form.is_valid():
            # Сохранить новую категорию в базе данных.
            form.save(commit=True)

            # Теперь вызвать предсталвение index().
            # Пользователю будет показана главная страница.
            return index(request)
        else:
            # Обрабатываемая форма содержит ошибки - вывести их в терминал.
            print(form.errors)
    else:
        # Если запрос был не POST, вывести форму, чтобы можно было ввести в неё данные.
        form = CategoryForm()

    # Форма с ошибкой (или ошибка с данных), форма не была получена...
    # Вывести форму с сообщениями об ошибках (если они были).
    return render(request, 'rango/add_category.html', {'form': form})