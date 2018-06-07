from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from .models import Client, Engagement, User, Proposal, Payment, Notes, Disengagement, StuffOnJob, Target, Invoice
import calendar, datetime
from django.utils.dates import MONTHS

job =(
      ('Annually','Annually'),
      ('Monthly','Monthly'),
      ('Seasonal','Seasonal'),
      )

MONTHS = tuple(zip(range(1,13), (calendar.month_name[i] for i in range(1,13))))

class NewClientForm(ModelForm):
    year_end = forms.ChoiceField(choices=MONTHS)
    class Meta:
        model = Client
        fields = ('__all__')


    def __init__(self, *args, **kwargs):
        super(NewClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id ='id-client-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
                                Fieldset('COMPANY DETAILS',
                                   Field('name',placeholder='Name of the Company', css_class="some-class"),
                                   Field('tin'),
                                   Field('comp_type'),
                                   Field('year_end'),
                                   Field('company_logo'),
                                   ),

                                Fieldset('SERVICE PROVIDERS',
                                   TabHolder(Tab('bankers', 'bankers'),
                                            Tab('lawyers', 'lawyers'),
                                            Tab('auditors', 'auditors'),
                                            Tab('trustees', 'trustees'),
                                            ),
                                            ),
                                Fieldset('CONTACT INFOMATION',
                                   Field('telephone_number',placeholder='Company mobile', css_class="some-class"),
                                   Field('Email_address'),
                                   Field('office'),
                                   ),
                             Fieldset('OTHER INFOMATION',
                                Field('directors_renumenration', css_class="some-class"),
                                Field('currency'),
                                Field('audit_fees'),
                                Field('share_capital'),
                                Field('directors_renumenration'),
                                ),

                                )

class EngagementForm(ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget(years=range(2015, 2021))) #, initial=datetime.date.today()
    date_printed = forms.DateField(widget=forms.SelectDateWidget(years=range(2015, 2021)))
    engagement_ending = forms.DateField(widget=forms.SelectDateWidget(years=range(2015, 2021)))
    CHOICES = eng_status = (('None','None'),('Pending','Pending'),('Planned','Planned'),('Active','Active'),('Concluded','Concluded'),)
    status = forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect, initial ='None')
    class Meta:
        model = Engagement
        exclude = ['balance', 'payment', 'client','date','active']
    def __init__(self, *args, **kwargs):
        super(EngagementForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id ='id-client-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProposalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.method = 'post'
        self.helper.form_action = 'index'
        self.helper[1] = InlineRadios('source')

    class Meta:
        model = Proposal
        exclude = ['date']
        widgets = {
                'requirements': forms.Textarea(attrs={'class': 'desc'}),
        }

class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        exclude = ['date', 'engagement']
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id ='payment-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class NotesForm(ModelForm):
    class Meta:
        model = Notes
        exclude = ['date','engagement']

class DisengagementForm(ModelForm):
    class Meta:
        model = Disengagement
        exclude = ['date', 'engagement']

class StuffOnJobForm(ModelForm):
    class Meta:
        model = StuffOnJob
        exclude = ['engagement']

class TargetForm(ModelForm):
    class Meta:
        model = Target
        fields = ('__all__')
    def __init__(self, *args, **kwargs):
        super(TargetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-target-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit',css_class='btn-success'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
                                Fieldset('YEAR','year'),
                                Fieldset('EXISTING ENGAGEMENTS','audit','aos','taxcom','taxadv','comsec','consul'),
                                Fieldset('NEW ENGAGEMENTS','audit_new','aos_new','taxcom_new','taxadv_new','comsec_new','consul_new'),)

class InvoiceForm(ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.date.today())
    class Meta:
        model = Invoice
        fields = ('reference','date','amount','scan')
    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id ='invoice-create-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class SearchForm(ModelForm):
    class Meta:
        model = Client
        fields = ('name',)
