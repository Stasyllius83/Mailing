from django.shortcuts import get_object_or_404


def change_active_object(request, model ,pk):

    client = get_object_or_404(model, pk=pk)
    if client.is_active:
        client.is_active = False
    else:
        client.is_active = True

    client.save()
