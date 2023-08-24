from django.db import models
from django.db.models import Max

from src.accounts.models import User


# Create your models here.


class GuestGroup(models.Model):
    sequence = models.IntegerField(blank=True)
    group_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_guests(self):
        return Guest.objects.filter(group=self).count()

    def save(self, *args, **kwargs):
        if not self.id:
            # Set the sequence field to the next available value
            max_sequence = GuestGroup.objects.aggregate(Max('sequence'))['sequence__max']
            self.sequence = (max_sequence or 0) + 1

        super(GuestGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.group_name

    class Meta:
        ordering = ['sequence']


class Guest(models.Model):
    guest_name = models.CharField(max_length=100)
    group = models.ForeignKey(GuestGroup, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.guest_name


class InvitationLetter(models.Model):
    group = models.OneToOneField(GuestGroup, on_delete=models.CASCADE, related_name='invitation_set')
    sequence = models.IntegerField(blank=True)
    total_invitation = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group.group_name

    def save(self, *args, **kwargs):
        if not self.id:
            # Set the sequence field to the next available value
            max_sequence = InvitationLetter.objects.aggregate(Max('sequence'))['sequence__max']
            self.sequence = (max_sequence or 0) + 1

        super(InvitationLetter, self).save(*args, **kwargs)

    class Meta:
        ordering = ['sequence']


class Provider(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider_name = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    attachment = models.FileField(upload_to='attachments/', help_text='File Should be less than 5mb', null=True,
                                  blank=True)
    link = models.URLField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def pending_amount(self):
        if self.total_cost:
            pending = float(self.total_cost) - float(self.paid)
            return pending
        return None

    class Meta:
        ordering = ['-created_at']


class Table(models.Model):
    TABLE_TYPE = (
        ('1', 'Rounded Table'),
        ('2', 'Rectangle Table'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table_name = models.CharField(max_length=100)
    table_type = models.CharField(max_length=100, choices=TABLE_TYPE)
    seat_count = models.IntegerField()
    seats_left = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.table_name

    def guests(self):
        return GuestTable.objects.filter(table=self)

    class Meta:
        ordering = ('-created_at',)


class GuestTable(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='guest_table')

    def __str__(self):
        return self.guest.group.group_name


class EventTimeLine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('date',)
