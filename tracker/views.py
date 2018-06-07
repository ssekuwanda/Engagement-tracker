from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.db.models import Q, Sum, Count
from .forms import NewClientForm, UserForm, EngagementForm, ProposalForm, PaymentForm, NotesForm, DisengagementForm, StuffOnJobForm, TargetForm, InvoiceForm, SearchForm
from .models import Client, ContactPerson, Engagement, Invoice, Payment, Target
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView,  CreateView, UpdateView, DetailView, ListView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .filters import EngagementFilter, ClientFilter
import json

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

@login_required
def home(request):
    clients = Client.objects.all()
    count = len(Client.objects.annotate(Count("name")))

    # if request.method == "GET":
    #     search_text = request.GET['search_text']
    #     if search_text is not None and search_text != u"":
    #         search_text = request.GET['search_text']
    #         statuss = Client.objects.filter(status__contains = search_text)
    #     else:
    #         statuss = []

    return render(request, 'home.html', {'clients':clients, 'count':count})

@login_required
def detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    engagements = client.engagements.all()

    return render(request, 'detail.html', {'client':client, 'engagements':engagements})

def all_invoices(request):
    all_inv = Invoice.objects.all()
    return render(request, 'invoices.html', {'all_inv':all_inv})

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
def edit_engagement(request, pk, engagement_pk):
    eng = get_object_or_404(Engagement, client__pk=pk, pk=engagement_pk)
    if request.POST:
        form = EngagementForm(request.POST, instance=eng)
        if form.is_valid():
            engagement = form.save()
            return redirect("tracker:detail", pk=engagement_pk)
    form = EngagementForm(instance=eng)
    return render(request, 'edit_engagement.html', {'form':form, 'eng':eng})


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

def create_payment(request, pk, engagement_pk):
    engagement = get_object_or_404(Engagement, client__pk=pk, pk=engagement_pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.engagement = engagement
            payment.save()
            return redirect('tracker:engagement_invoices', pk=pk, engagement_pk=engagement_pk)
    else:
        form = PaymentForm()
    return render(request, 'payment.html',{'form':form,'engagement':engagement})

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
    return render(request,  'disengagementform.html', {'form':form, 'client':client})

def dashboard(request):
    targets = Target.objects.all()

    dataset = Engagement.objects\
                .values('assignment','year')\
                .annotate(existing_count=Count('assignment', filter=Q(type='Existing')),
                        new_count=Count('assignment', filter=Q(type='New')),
                        active_count=Sum('active'),
                        )\
                .order_by('assignment')

    categories = list()
    new_series_data = list()
    existing_series_data = list()
    active_series_data = list()

    for entry in dataset:
        categories.append(entry['assignment'])
        new_series_data.append(entry['new_count'])
        existing_series_data.append(entry['existing_count'])
        active_series_data.append(entry['active_count'])

    new_series = {'name':'New',
                    'data':new_series_data,
                    'color':'green'
    }
    existing_series = {'name':'Existing',
                    'data':existing_series_data,
                    'color':'red'
    }

    chart = {
            'chart':{'type':'column'},
            'title':{'text': 'ENGAGEMENTS BY SERVICE'},
            'xAxis':{'categories':categories},
            'series':[new_series,existing_series]
    }

    dump =json.dumps(chart)

    def invoice(x):
        out = Invoice.objects.filter(engagement__assignment__contains=x).aggregate(Sum('amount'))['amount__sum']
        return int(0 if out is None else out)

    def total(a,b,c,d,e,f):
        return(a+b+c+d+e+f)

    invoices_taxcom =  invoice('Tax compliance')
    invoices_audit = invoice('Audit & assurance')
    invoices_aos = invoice('AOS')
    invoices_taxadv = invoice('Tax advisory')
    invoices_comsec = invoice('Company secretarial')
    invoices_consul = invoice('Consultancy')
    # invoices_account = invoice('account')
    invoice_total = total(invoices_taxcom,invoices_audit,invoices_aos,invoices_taxadv,invoices_comsec,invoices_consul)

    def engagement(y):
        current = Engagement.objects.filter(assignment__contains=y).filter(type__contains='Existing').aggregate(Sum('active'))['active__sum']
        return int(0 if current is None else current)


    sum_tax = engagement('Tax compliance')
    sum_comsec = engagement('Company secretarial')
    sum_audit = engagement('Audit & assurance')
    sum_taxadv = engagement('Tax advisory')
    sum_account = engagement('Accountancy')
    sum_cons = engagement('Consultancy')
    sum_aos = engagement('AOS')
    summation_all_assign1 = total(sum_tax,sum_comsec,sum_audit,sum_taxadv,sum_account,sum_cons)
    summation_all_assign = sum_aos+summation_all_assign1

    def engagement_new(y):
        new = Engagement.objects.filter(assignment__contains=y).filter(type__contains='New').aggregate(Sum('active'))['active__sum']
        return int(0 if new is None else new)

    sum_tax_new = engagement_new('Tax compliance')
    sum_comsec_new = engagement_new('Company secretarial')
    sum_audit_new = engagement_new('Audit & assurance')
    sum_taxadv_new = engagement_new('Tax advisory')
    sum_account_new = engagement_new('Accountancy')
    sum_cons_new = engagement_new('Consultancy')
    sum_aos_new = engagement_new('AOS')
    summation_all_assign_new1 = total(sum_tax_new,sum_comsec_new,sum_audit_new,sum_taxadv_new,sum_account_new,sum_cons_new)
    summation_all_assign_new = sum_aos_new+summation_all_assign_new1

    total_tax = sum_tax+sum_tax_new
    total_comsec = sum_comsec+sum_comsec_new
    total_audit = sum_audit+sum_audit_new
    total_taxadv = sum_taxadv+sum_taxadv_new
    total_account = sum_account+sum_account_new
    total_cons = sum_cons+sum_cons_new
    total_aos = sum_aos+sum_aos_new
    total = total_tax+total_comsec+total_audit+total_taxadv+total_account+total_cons+total_aos

    var1_tax = int(0 if sum_tax_new is None else sum_tax_new)
    var1_comsec = int(0 if sum_tax is None else sum_tax)+int(0 if sum_tax_new is None else sum_tax_new)
    var1_audit = int(0 if sum_tax is None else sum_tax)+int(0 if sum_tax_new is None else sum_tax_new)
    var1_taxadv = int(0 if sum_tax is None else sum_tax)+int(0 if sum_tax_new is None else sum_tax_new)
    var1_account = int(0 if sum_tax is None else sum_tax)+int(0 if sum_tax_new is None else sum_tax_new)
    var1_cons = int(0 if sum_tax is None else sum_tax)+int(0 if sum_tax_new is None else sum_tax_new)
    var1_aos = int(0 if sum_tax is None else sum_tax)+int(0 if sum_tax_new is None else sum_tax_new)
    total_var1 = var1_tax+var1_comsec+var1_audit+var1_taxadv+var1_account+var1_cons+var1_aos

    var2_tax = int(0 if total_tax is None else total_tax)
    var2_comsec = int(0 if total_comsec is None else total_comsec)
    var2_audit = int(0 if total_audit is None else total_audit)
    var2_taxadv = int(0 if total_taxadv is None else total_taxadv)
    var2_account = int(0 if total_account is None else total_account)
    var2_cons = int(0 if total_cons is None else total_cons)
    var2_aos = int(0 if total_aos is None else total_aos)
    total_var2 = var2_tax+var2_comsec+var2_audit+var2_taxadv+var2_account+var2_cons+var2_aos

    context = {'targets':targets,

                'sum_tax':sum_tax,
                'sum_audit':sum_audit,
                'sum_taxadv':sum_taxadv,
                'sum_comsec':sum_comsec,
                'sum_account':sum_account,
                'sum_cons':sum_cons,
                'sum_aos':sum_aos,
                'summation_all_assign':summation_all_assign,

                'sum_audit_new':sum_audit_new,
                'sum_aos_new':sum_aos_new,
                'sum_comsec_new':sum_comsec_new,
                'sum_account_new':sum_account_new,
                'sum_taxadv_new':sum_taxadv_new,
                'sum_cons_new':sum_cons_new,
                'sum_tax_new':sum_tax_new,
                'summation_all_assign_new':summation_all_assign_new,

                'total_tax':total_tax,
                'total_comsec':total_comsec,
                'total_audit':total_audit,
                'total_taxadv':total_taxadv,
                'total_account':total_account,
                'total_cons':total_cons,
                'total_aos':total_aos,

                'var2_tax':var2_tax,
                'var2_comsec':var2_comsec,
                'var2_audit':var2_audit,
                'var2_taxadv':var2_taxadv,
                'var2_account':var2_account,
                'var2_cons':var2_cons,
                'var2_aos':var2_aos,

                'total_var2':total_var2,
                'total':total,

                'total_var1':total_var1,

                'invoices_taxcom':invoices_taxcom,
                'invoices_audit':invoices_audit,
                'invoices_aos':invoices_aos,
                'invoices_taxadv':invoices_taxadv,
                'invoices_comsec':invoices_comsec,
                'invoices_consul':invoices_consul,

                'invoice_total':invoice_total,
                'dataset':dataset,
                'chart':chart,

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
    invoice = engagement.invoices.all()
    payment = payment.engagement.all()
    return render(request, 'detail.html', {'invoice':invoice, 'payment':payment})

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

class EngagementPayment(ListView):
    model = Payment
    context_object_name = 'payments'
    template_name = 'engagement_details.html'

    def get_context_data(self, **kwargs):
        kwargs['engagement']=self.engagement
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.engagement = get_object_or_404(Engagement, client__pk=self.kwargs.get('pk'), pk=self.kwargs.get('engagement_pk'))
        queryset = self.engagement.payments.order_by('-date')
        return queryset

def notifications(request):
    pass

def dasher(request):
    # new = Engagement.objects.values().filter(type__contains='Existing')
    new = Engagement.objects.filter(type__contains='New')
    existing = Engagement.objects.filter(type__contains='Existing')

    invoiced = Invoice.objects.all()
    payment = Payment.objects.all()

    from django.core import serializers
    data = serializers.serialize("json", Engagement.objects.all())

    dump = json.dumps(data)

    return render(request, 'dasher.html', {'new':new,'existing':existing, 'invoiced':invoiced,'payment':payment,'dump':dump})
