from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm

# Create your views here.
def home_page(request):
    return render(
        request,
        'home.html',
        context={
            'form': ItemForm(),
            'user': request.user,
            'request': request,
        }
    )
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_list', list_.id)
    return render(request, 'list.html', {'list': list_, "form": form})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect('view_list', list_.id)
    else:
        return render(request, 'home.html', {"form": form})