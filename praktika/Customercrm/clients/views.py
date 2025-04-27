from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Client
from .forms import ClientForm
from django.views.decorators.http import require_http_methods
import json


def client_management(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            clients = Client.objects.all()

            # Для HTMX-запросов, обновляем только список клиентов
            if request.headers.get('HX-Request'):
                return render(request, 'clients/partials/clients_list.html', {'clients': clients})

            # Для обычных POST-запросов возвращаем страницу с результатами
            return render(request, 'clients/base.html', {'form': form, 'clients': clients})

        # Если форма невалидна, возвращаем только форму с ошибками
        if request.headers.get('HX-Request'):
            return render(request, 'clients/partials/client_form.html', {'form': form})

    # GET-запрос (при первой загрузке страницы)
    if not request.headers.get('HX-Request'):
        form = ClientForm()
        clients = Client.objects.all()
        return render(request, 'clients/base.html', {'form': form, 'clients': clients})

    return HttpResponse(status=204)


@require_http_methods(["GET", "POST"])
def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            # Для HTMX-запросов возвращаем обновленный список клиентов
            if request.headers.get('HX-Request'):
                clients = Client.objects.all()
                return render(request, 'clients/partials/clients_list.html', {'clients': clients})

            # Для обычных запросов возвращаем полный список
            clients = Client.objects.all()
            return render(request, 'clients/partials/clients_list.html', {'clients': clients})

        # Если форма невалидна, возвращаем ошибки
        return render(request, 'clients/partials/edit_modal.html', {
            'form': form,
            'client': client
        })

    # GET-запрос (показ формы для редактирования)
    form = ClientForm(instance=client)
    return render(request, 'clients/partials/edit_modal.html', {
        'form': form,
        'client': client
    })


@require_http_methods(["DELETE"])
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client.delete()
    clients = Client.objects.all()
    return render(request, 'clients/partials/clients_list.html', {'clients': clients})
