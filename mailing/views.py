from django.forms import inlineformset_factory
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from mailing.forms import ClientForm, MailingForm, MessageForm
from mailing.models import Client, Log, MailingSettings, Message



class ClientListView(ListView):
    model = Client
    template_name = 'mailing/clients_list.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients_list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients_list')


class MailingDetailView(DetailView):
    model = MailingSettings
    template_name = 'mailing/mailing_detail.html'


class MailingListView(ListView):
    model = MailingSettings
    template_name = 'mailing/mailing_list.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['all'] = context_data['object_list'].count()
        context_data['active'] = context_data['object_list'].filter(status=MailingSettings.STARTED).count()

        mailing_list = context_data['object_list'].prefetch_related('clients')
        clients = set()
        [[clients.add(client.email) for client in mailing.clients.all()] for mailing in mailing_list]
        context_data['clients_count'] = len(clients)

        return context_data


class MailingCreateView(CreateView):
    model = MailingSettings
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(MailingSettings, Message, extra=1, form=MessageForm)

        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST)
        else:
            context_data['formset'] = MessageFormset()

        return context_data


    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(MailingSettings, Message, extra=1, form=MessageForm)

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


class MailingDeleteView(DeleteView):
    model = MailingSettings
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')


class LogListView(ListView):
    model = Log
    template_name = 'mailing/log_list.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['all'] = context_data['object_list'].count()
        context_data['success'] = context_data['object_list'].filter(status_try=True).count()
        context_data['error'] = context_data['object_list'].filter(status_try=False).count()

        return context_data
