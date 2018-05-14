from django.contrib.auth.models import Permission, User
from django.db import models
from django_countries.fields import CountryField
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
import datetime
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.db.models.signals import pre_save, post_save
from datetime import date


ass = (
    ('Tax compliance','Tax compliance'),
    ('Company secretarial', 'Company secretarial'),
    ('Audit & assurance','Audit & assurance'),
    ('Tax advisory','Tax advisory'),
    ('Accountancy','Accountancy'),
    ('Consultancy', 'Consultancy'),
    ('AOS','AOS'),
     )

money = (
    ('USD','USD'),
    ('UGX','UGX'),
    ('GBP','GBP'),
    )

job =(
      ('Annually','Annually'),
      ('Monthly','Monthly'),
      ('Seasonal','Seasonal'),
      )
source = (
            ('Referal by client','Referal by client'),
            ('Referal by competitor','Referal by competitor'),
            ('Published/Advertized','Published/Advertized'),
            ('Self approach','Self approach'),
            )
eng_status = (
            ('Pending','Pending'),
            ('Planned','Planned'),
            ('Active','Active'),
            ('Concluded','Concluded'),
    )


title_of_contact_person = (
                            ('Ms','Ms'),
                            ('Mr','Mr'),
                                            )


YEAR_CHOICES = []
for r in range(2014, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))
type = (
('Existing','Existing'),
('New','New'),
)
class Proposal(models.Model):
    company_name = models.CharField('Name of company or individual', max_length=89, blank=True, null=True)
    source = models.CharField(choices = source, max_length=122, default='Referal by client')
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    draft_proposal = models.FileField(blank=True, null=True)
    requirements = models.CharField(max_length = 200, blank=True, null= True, help_text='Separate by Tab or Commas')
    qualified = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name+'-'+self.date

class Client(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    client_number = models.CharField(max_length=100, blank=True, null=True)
    tin = models.CharField('TIN', max_length=19, blank=True, null=True)
    comp_type = models.CharField('Company Type',blank = True, null = True, max_length = 100 )

    services = models.TextField(blank = True, null=True)
    industry = models.CharField(blank = True, max_length = 300, null=True)
    origin = CountryField(blank = True, max_length = 2, help_text = "Country of origin", null=True)
    directors = models.TextField('BOARD OF DIRECTORS',blank = True, max_length = 500, null = True)
    company_secretary = models.TextField(blank = True, null = True)
    office = models.TextField('REGISTERED OFFICE',blank = True, null = True)
    bankers = models.TextField(blank = True, null = True)
    lawyers = models.TextField(blank = True, null = True)
    auditors = models.TextField(blank = True, null = True)
    trustees = models.TextField(blank = True, null = True)

    directors_renumenration = models.CharField(max_length=200,blank = True, null = True)
    currency = models.CharField(max_length = 3, default = 'USD', choices = money, null = True, blank = True)
    billing_frequency   = models.CharField(max_length = 19, choices = job, default = 'Annually', blank=True, null=True)
    share_capital = models.CharField(max_length=200,blank = True, null = True)

    year_end = models.CharField( max_length = 10, blank=True, null=True)
    company_logo = models.ImageField('Logo',blank = True, null = True, default='image/mazarslogo.jpg')
    logo = ImageSpecField(source='company_logo',processors =[ResizeToFill(250, 100)], format='JPEG', options={'quality':500})
    client = models.BooleanField('Client status',default= True, help_text = "Currently Client?")
    telephone_number = models.CharField(max_length = 20, blank = True, null=True)
    Email_address = models.CharField(max_length = 70, blank = True, null=True)
    is_favorite = models.BooleanField('Is Client',default=True)

    def __str__(self):
        return self.name

class ContactPerson(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    title = models.CharField(choices=title_of_contact_person, max_length=3)
    first_name = models.CharField(max_length=122)
    second_name = models.CharField(max_length=122)
    email = models.EmailField(blank=True, null= True)
    mobile_number = models.IntegerField(blank=True, null= True)

    def __str__(self):
        return self.title+' '+self.first_name+' '+self.second_name

class Engagement(models.Model):
    client              = models.ForeignKey(Client, on_delete=models.CASCADE,blank=True, null=True, related_name='engagements')
    year                = models.IntegerField('Year', choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    reference           = models.CharField(max_length =122,blank=True, null=True)
    date                = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    assignment          = models.CharField('Service', max_length = 19, choices = ass,blank=True, null=True)
    letter              = models.FileField('Engagement letter',blank=True, null=True)
    engagement_ending   = models.DateField('Ending date', blank=True, null = True)
    currency            = models.CharField(max_length = 19, choices = money, default = 'USD',blank=True, null=True)
    rate                = models.PositiveIntegerField('Rate', blank=True, null=True)
    factor              = models.PositiveIntegerField(default=1,blank=True, null=True)
    active              = models.PositiveIntegerField(blank=True, null=True)
    disbursements       = models.PositiveIntegerField(blank=True, null=True)
    payment             = models.PositiveIntegerField('Payment',blank=True, null=True )
    balance             = models.PositiveIntegerField(default=0, blank=True, null=True)
    status              = models.CharField(choices=eng_status, max_length=122,default ='Active',blank=True, null=True)
    remarks             = models.CharField(max_length=1000, blank=True, null=True)
    type                = models.CharField(choices=type, max_length=12, blank=True, null=True)

    class Meta:
        ordering = ('-date',)

    def get_absolute_url(self):
        """Returns the url to access a particular client instance."""
        return reverse('detail', args=[str(self.id)])

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.active = instance.rate*instance.factor
pre_save.connect(rl_pre_save_receiver, sender=Engagement)

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    today = datetime.date.today()
    later = instance.date
    timed = later- today
    timer = timed.days
    if timer >= 250:
        instance.type = "Existing"
pre_save.connect(rl_pre_save_receiver, sender=Engagement)

class StuffOnJob(models.Model):
    engagement = models.ForeignKey(Engagement, on_delete=models.CASCADE, blank=True, null= True)
    title = models.CharField(max_length=120, blank=True, null= True)
    first_name = models.CharField(max_length=122, blank=True, null= True)
    last_name = models.CharField(max_length=122, blank=True, null= True)
    section = models.CharField(max_length=122, blank=True, null= True, help_text='Section On The Job')

    def __str__(self):
        return self.title+' - '+self.first_name+' '+self.last_name

class Notes(models.Model):
    engagement = models.ForeignKey(Engagement, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=90)
    up_notes = models.CharField(max_length=225, blank=True, null=True)
    notes_file = models.FileField(help_text='(Images, Documents and Audio)')

    def __str__(self):
        return self.title

class Invoice(models.Model):
    engagement = models.ForeignKey(Engagement, on_delete=models.CASCADE, blank=True, null= True, related_name='invoices')
    reference = models.CharField('Invoice Number',max_length=19, blank=True, null= True)
    date = models.DateTimeField(blank=True, null= True)
    amount = models.IntegerField(blank=True, null= True)
    scan = models.FileField('Scanned Invoice',blank=True, null= True)
    reminder = models.DateField('Set Payment Date remainder',blank=True, null= True)

    def __str__(self):
        return self.reference

class Payment(models.Model):
    invoice  = models.ForeignKey(Invoice,on_delete=models.CASCADE, related_name='payments',blank=True, null=True)
    amount      = models.IntegerField(blank=True, null=True)
    doc         = models.FileField('Scanned Receipt')
    date        = models.DateField(blank=True, null= True)

    def __str__(self):
        return str(self.amount)

class Disengagement(models.Model):
    engagement = models.ForeignKey(Engagement, on_delete= models.CASCADE)
    date = models.DateField(auto_now_add=True)
    letter = models.FileField('Disengagement letter')
    report = models.FileField('Reports')
    client_comment = models.FileField('client_comments')
    notes = models.CharField('Engagement notes or concerns', max_length=250, blank=True, null= True)

    def __str__(self):
        return self.date

class Target(models.Model):
    year        = models.IntegerField(choices=YEAR_CHOICES, unique=True)
    audit       = models.PositiveIntegerField()
    aos         = models.PositiveIntegerField('AoS')
    taxcom      = models.PositiveIntegerField('TaxCom')
    taxadv      = models.PositiveIntegerField('TaxAdv')
    comsec      = models.PositiveIntegerField('ComSec')
    consul      = models.PositiveIntegerField('Consul')
    audit_new   = models.PositiveIntegerField('audit')
    aos_new     = models.PositiveIntegerField('AoS')
    taxcom_new  = models.PositiveIntegerField('TaxCom')
    taxadv_new  = models.PositiveIntegerField('TaxAdv')
    comsec_new  = models.PositiveIntegerField('ComSec')
    consul_new  = models.PositiveIntegerField('Consul')

    class Meta:
        ordering = ('-year',)

    def __str__(self):
        return str(self.year)
