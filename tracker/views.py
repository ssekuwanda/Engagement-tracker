from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.db.models import Q, Sum, Count
from .forms import NewClientForm, UserForm, EngagementForm, ProposalForm, PaymentForm, NotesForm, DisengagementForm, StuffOnJobForm, TargetForm, InvoiceForm
from .models import Client, ContactPerson, Engagement, Invoice, Payment, Target
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView,  CreateView, UpdateView, DetailView, ListView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .filters import EngagementFilter

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

@login_required
def home(request):
    clients = Client.objects.all()
    count = len(Client.objects.annotate(Count("name")))
    return render(request, 'home.html', {'clients':clients, 'count':count })

@login_required
def detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    engagements = client.engagements.all()
    return render(request, 'detail.html', {'client':client, 'engagements':engagements})

@login_required
def new_client(request):
    if request.method =='POST':
        form = NewClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,' Client Added Successfully')
            # send_mail(
            #     'Subject here',
            #     'New notication version control',
            #     'notifications@brj.co.ug',
            #     ['paul.muwanguzi@mazars.ug', 'douglas.ssekuwanda@mazars.ug'],
            #     fail_silently=False,
            # )
            send_mail(
                'gmail nots..',
                'New notication version control',
                'cytixdoug@gmail.com',
                ['paul.muwanguzi@mazars.ug', 'douglas.ssekuwanda@mazars.ug'],
                fail_silently=False,
            )
            return redirect('tracker:home')
        else:
            messages.warning(request, 'Please fill in all the fields correctly')
    else:
        form = NewClientForm()
    return render(request, 'client_create.html', {'form': form} )

@login_required
def create_engagement(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = EngagementForm(request.POST)
        if form.is_valid():
            engagement = form.save(commit=False)
            engagement.client = client
            engagement.save()
            return redirect("tracker:detail", pk=pk)
    else:
        form = EngagementForm()
    return render(request, 'engagement_create.html', {'form':form, 'client':client})

@login_required
def edit_engagement(request, client_id, engagement_id):
    eng = get_object_or_404(Engagement, client__id=client_id, id=engagement_id)
    if request.POST:
        form = EngagementForm(request.POST,instance=eng)
        if form.is_valid():
            engagement = form.save()
            return redirect("tracker:detail", pk=engagement_id)
    form = EngagementForm(instance=eng)
    return render(request, 'edit_engagement.html', {'form':form, 'eng':eng})

@login_required
def index(request):
        client      = Client.objects.all()
        year        = Year.objects.all()
        engagement_results = Engagement.objects.all()
        query       = request.GET.get("q")
        if query:
            client = client.filter(
                Q(name=query) |
                Q(client_number=query)
            ).distinct()
            engagement_results = engagement_results.filter(
                Q(client_name__icontains=query)
            ).distinct()
            return render(request, 'tracker/index.html', {
                'client': client,
                'engagement_results': engagement_results,
            })
        else:
            return render(request, 'index.html', {'client': client})

class ClientEdit(UpdateView):
    model = Client
    fields = ('__all__')
    template_name = 'client_create.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'client'

    def form_valid(self, form):
        client = form.save()
        client.save()
        return redirect('tracker:detail', pk=client.pk)

def delete_client(request, client_id):
    client = Client.objects.get(id=client_id)
    client.delete()
    client = Client.objects.all()
    return render(request, 'detail.html', {'client': client})

def delete_engagement(request, client_id, engagement_id):
    client          = get_object_or_404(Client, id=client_id)
    engagement      = Engagement.objects.get(id=engagement_id)
    engagement.delete()
    return render(request, 'detail.html', {'client': client})

def new_proposal(request):
    form            = ProposalForm
    template_name   = 'create_proposal.html'
    return render(request, template_name, {'form':form})

def create_invoice(request, pk, engagement_pk):
    engagement = get_object_or_404(Engagement, client__pk=pk, pk=engagement_pk)
    if request.method =="POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.engagement = engagement
            invoice.save()

            engagement_url = reverse('tracker:engagement_invoices', kwargs={'pk':pk, 'engagement_pk':engagement_pk})
            engagement_invoice_url = '{url}/{id}'.format(
                url=engagement_url,
                id=invoice.pk,
                  )
            return redirect(engagement_url)
    else:
        form = InvoiceForm()
    return render(request, 'invoice_create.html',{'form':form,'engagement':engagement})

class PayInvoice(CreateView):
    model = Payment
    fields = ('__all__')
    template_name = 'payment.html'
    pk_url_kwarg = 'pay_pk'
    context_object_name = "post"

    def get_queryset(self):
        self.invoice = get_object_or_404(Invoice, engagement__pk=self.kwargs.get('pk'), pk=self.kwargs.get(invoice_pk))
        queryset = self.invoice.payment.order_by('-date')
        return queryset

    def form_valid(self, form):
        pay = form.save(commit=False)
        pay.invoice = self.invoice
        return redirect('tracker:engagement_invoices', kwargs={'pk':pk, 'engagement_pk':engagement_pk})

class EngagementDetails(DetailView):
    template_name = 'engagement_details.html'
    def get_queryset(self):
        disengagement   = Disengagement.objects.all()
        stuff           = StuffOnJob.objects.all()
        contact         = ContactPerson.objects.all()
        notes           = Notes.objects.all()
        return queryset()

def notes(request):
    if request.method=='POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            return redirect('detail')
    else:
        form = NotesForm()
    return render(request, 'notes.html', {'form': form} )

def stuffonjob(request):
    client = get_objects_or_404(Client, pk=pk)
    if request.method=='POST':
        form = StuffOnJobForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            return redirect('detail')
    else:
        form = StuffOnJobForm()
    return render(request, 'stuffonjob.html',{'form':form})

def DisengagementForm(request):
    client = get_object_or_404(Client, pk=pk)
    if form.method=='POST':
        form = DisengagementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('detail')
    else:
        form = DisengagementForm()
    return render(request,  'disengagementform.html', {'form':form })

def dashboard(request):
    targets = Target.objects.all()

    exiting_audit = Target.objects.all().aggregate(Sum('audit'))['audit__sum']
    exiting_aos = Target.objects.all().aggregate(Sum('aos'))['aos__sum']
    exiting_taxcom = Target.objects.all().aggregate(Sum('taxcom'))['taxcom__sum']
    exiting_taxadv = Target.objects.all().aggregate(Sum('taxadv'))['taxadv__sum']
    exiting_comsec = Target.objects.all().aggregate(Sum('comsec'))['comsec__sum']
    exiting_consul = Target.objects.all().aggregate(Sum('consul'))['consul__sum']
    exiting = exiting_audit+exiting_aos+exiting_taxcom+exiting_taxadv+exiting_comsec+exiting_consul

    audit_new = Target.objects.all().aggregate(Sum('audit_new'))['audit_new__sum']
    aos_new = Target.objects.all().aggregate(Sum('aos_new'))['aos_new__sum']
    taxcom_new = Target.objects.all().aggregate(Sum('taxcom_new'))['taxcom_new__sum']
    taxadv_new = Target.objects.all().aggregate(Sum('taxadv_new'))['taxadv_new__sum']
    comsec_new = Target.objects.all().aggregate(Sum('comsec_new'))['comsec_new__sum']
    consul_new = Target.objects.all().aggregate(Sum('consul_new'))['consul_new__sum']
    new = audit_new+aos_new+taxcom_new+taxadv_new+comsec_new+consul_new

    summation_all_assign = Engagement.objects.filter(type__contains='Existing').aggregate(Sum('rate'))['rate__sum']


    sum_tax = Engagement.objects.filter(assignment__contains='Tax compliance').filter(type__contains='Existing').aggregate(Sum('rate'))['rate__sum']
    sum_comsec = Engagement.objects.filter(assignment__contains='Company secretarial').filter(type__contains='Existing').aggregate(Sum('rate'))['rate__sum']
    sum_audit = Engagement.objects.filter(assignment__contains='Audit & assurance').filter(type__contains='Existing').aggregate(Sum('rate'))['rate__sum']
    sum_taxadv = Engagement.objects.filter(assignment__contains='Tax advisory').filter(type__contains='Existing').aggregate(Sum('rate'))['rate__sum']
    sum_account = Engagement.objects.filter(assignment__contains='Accountancy').filter(type__contains='Existing').aggregate(Sum('rate'))['rate__sum']
    sum_cons = Engagement.objects.filter(assignment__contains='Consultancy').filter(type__contains='Existing').aggregate(Sum('rate'))['rate__sum']
    sum_aos = Engagement.objects.filter(assignment__contains='AOS').filter(type__contains='Existing').aggregate(Sum('rate'))['rate__sum']

    summation_all_assign_new = Engagement.objects.filter(type__contains='New').aggregate(Sum('rate'))['rate__sum']

    sum_tax_new = Engagement.objects.filter(assignment__contains='Tax compliance').filter(type__contains='New').aggregate(Sum('rate'))['rate__sum']
    sum_comsec_new = Engagement.objects.filter(assignment__contains='Company secretarial').filter(type__contains='New').aggregate(Sum('rate'))['rate__sum']
    sum_audit_new = Engagement.objects.filter(assignment__contains='Audit & assurance').filter(type__contains='New').aggregate(Sum('rate'))['rate__sum']
    sum_taxadv_new = Engagement.objects.filter(assignment__contains='Tax advisory').filter(type__contains='New').aggregate(Sum('rate'))['rate__sum']
    sum_account_new = Engagement.objects.filter(assignment__contains='Accountancy').filter(type__contains='New').aggregate(Sum('rate'))['rate__sum']
    sum_cons_new = Engagement.objects.filter(assignment__contains='Consultancy').filter(type__contains='New').aggregate(Sum('rate'))['rate__sum']
    sum_aos_new = Engagement.objects.filter(assignment__contains='AOS').filter(type__contains='New').aggregate(Sum('rate'))['rate__sum']

    # var_tax = sum_tax-sum_tax_new
    # var_comsec = sum_comsec-sum_comsec_new
    # var_audit = sum_audit-sum_audit_new
    # var_taxadv = sum_taxadv-sum_taxadv_new
    # var_account = sum_account-sum_account_new
    # var_cons = sum_cons-sum_cons_new
    # var_aos = sum_aos-sum_aos_new

    context = {'targets':targets,'exiting':exiting,'new':new,'sum_tax':sum_tax,
                'sum_audit':sum_audit,
                'sum_taxadv':sum_taxadv,
                'sum_comsec':sum_comsec,
                'sum_account':sum_account,
                'sum_cons':sum_cons,
                'sum_aos':sum_aos,
                'summation_all_assign':summation_all_assign,

                'sum_tax_new':sum_tax_new,
                'sum_comsec_new':sum_comsec_new,
                'sum_audit_new':sum_audit_new,
                'sum_taxadv_new':sum_taxadv_new,
                'sum_account_new':sum_account_new,
                'sum_cons_new':sum_cons_new,
                'sum_aos_new':sum_aos_new,
                'summation_all_assign_new':summation_all_assign_new,

                # 'var_tax':var_tax,
                # 'var_comsec':var_comsec,
                # 'var_audit':var_audit,
                # 'var_taxadv':var_taxadv,
                # 'var_account':var_account,
                # 'var_cons':var_cons,
                # 'var_aos':var_aos,

                }
    template_name = 'dashboard.html'
    return render(request, template_name, context)

def add_target(request):
    target = Target.objects.all()
    if request.method=='POST':
        form = TargetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracker:dashboard')
    else:
        form = TargetForm()
    return render(request, 'add_target.html', {'form':form})

def search(request):
    eng_list = Engagement.objects.all()
    filter = EngagementFilter(request.GET, queryset=eng_list)
    return render(request, 'search.html',{'filter':filter})

def engagement_invoices(request, pk, engagement_pk):
    engagement =get_object_or_404(Engagement, pk=pk, engagement__pk=engagement_pk)
    invoice = invoice.engagement.all()
    return render(request, 'detail.html', {'client':client, 'invoice':invoice})

class EngagementInvoice(ListView):
    model = Invoice
    context_object_name = 'invoices'
    template_name = 'engagement_details.html'

    def get_context_data(self, **kwargs):
        kwargs['engagement']=self.engagement
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.engagement = get_object_or_404(Engagement, client__pk=self.kwargs.get('pk'), pk=self.kwargs.get('engagement_pk'))
        queryset = self.engagement.invoices.order_by('-date')
        return queryset
