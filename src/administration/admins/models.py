from django.db import models

from src.accounts.models import User


# Create your models here.


class GuestList(models.Model):
    group_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.group_name


class GuestGroup(models.Model):
    group_name = models.CharField(max_length=100)
    guest_list = models.ForeignKey(GuestList, on_delete=models.CASCADE)

    def __str__(self):
        return self.group_name


class Guest(models.Model):
    guest_name = models.CharField(max_length=100)
    group = models.ForeignKey(GuestGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.group.group_name


class InvitationLetter(models.Model):
    group = models.ForeignKey(GuestGroup, on_delete=models.CASCADE)
    letter_count = models.IntegerField()

    def __str__(self):
        return self.group.group_name


class Invitation(models.Model):
    group = models.ForeignKey(GuestGroup, on_delete=models.CASCADE)
    invitation_count = models.IntegerField()

    def __str__(self):
        return self.group.group_name


class Provider(models.Model):
    provider_name = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.DecimalField(max_digits=10, decimal_places=2)
    attachment = models.FileField(upload_to='attachments/')
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Table(models.Model):
    table_name = models.CharField(max_length=100)
    table_type = models.CharField(max_length=100)
    seat_count = models.IntegerField()
    seats_left = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class GuestTable(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)

    def __str__(self):
        return self.guest.group.group_name
