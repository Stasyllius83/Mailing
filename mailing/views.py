from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from mailing.forms import ClientForm, MailingForm, MessageForm
from mailing.models import Client, Log, MailingSettings, Message
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import permission_required
from mailing.service import send_deactivate_email
from blog.models import Blog
from django.shortcuts import get_object_or_404



class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data( **kwargs)
        context_data['count_mailings'] = MailingSettings.objects.all().count()
        context_data['count_mailings_is_active'] = MailingSettings.objects.filter(status=MailingSettings.STARTED).count()
        context_data['clients_count'] = Client.objects.all().count()
        context_data['random_blog'] = Blog.objects.order_by('?')[:3]

        return context_data

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.order_by('?')
        return queryset[:3]


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/clients_list.html'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients_list')


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients_list')

    def test_func(self):
        return self.get_object().owner == self.request.user.is_superuser \
            or self.request.user.has_perms(['mailing.delete_client'])


@permission_required('mailing.set_active_client')
def toggle_active_client(request, pk):
    client_item = get_object_or_404(Client, pk=pk)
    if client_item.is_active:
        client_item.is_active = False
        send_deactivate_email(client_item)
    else:
        client_item.is_active = True

    client_item.save()

    return redirect(reverse('mailing:clients_list'))


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients_list')


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = MailingSettings
    template_name = 'mailing/mailing_detail.html'


class MailingListView(LoginRequiredMixin, ListView):
    model = MailingSettings
    template_name = 'mailing/mailing_list.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['all_mailings'] = context_data['object_list'].count()
        context_data['active_mailings'] = context_data['object_list'].filter(status=MailingSettings.STARTED).count()

        mailing_list = context_data['object_list'].prefetch_related('clients')
        clients = set()
        [[clients.add(client.email) for client in mailing.clients.all()] for mailing in mailing_list]
        context_data['clients_count'] = len(clients)

        return context_data


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object.owner = self.request.user
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(MailingSettings, Message, form=MessageForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST)
        else:
            context_data['formset'] = MessageFormset()

        return context_data


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MailingSettings
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(MailingSettings, Message, form=MessageForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MessageFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


    def get_success_url(self):
        return reverse('mailing:mailing_detail', args=[self.object.pk])

    def test_func(self):
        return self.get_object().owner == self.request.user or self.request.user.is_superuser \
              or self.request.user.has_perms(['mailing.change_mailing'])

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user != self.get_object().owner:
            fields = [i for i in form.fields]
            for field in fields:
                if not self.request.user.has_perm(f'mailing.set_{field}'):
                    del form.fields[field]
        return form


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MailingSettings
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def test_func(self):
        return self.get_object().owner == self.request.user or self.request.user.is_superuser \
            or self.request.user.has_perms(['mailing.delete_mailing'])


@permission_required('mailing.set_active')
def toggle_active_mailing(request, pk):
    mailing_item = get_object_or_404(MailingSettings, pk=pk)
    if mailing_item.is_active:
        mailing_item.is_active = False
    else:
        mailing_item.is_active = True

    mailing_item.save()

    return redirect(reverse('mailing:mailing_list'))


class LogListView(LoginRequiredMixin, ListView):
    model = Log
    template_name = 'mailing/log_list.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['all'] = context_data['object_list'].count()
        context_data['success'] = context_data['object_list'].filter(status_try=True).count()
        context_data['error'] = context_data['object_list'].filter(status_try=False).count()

        return context_data


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')

    context = {
        'title': 'Контакты'
    }
    return render(request, 'mailing/contact.html', context)
