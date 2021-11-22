# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    user_email = models.TextField()
    birthdate = models.DateField()
    gender = models.CharField(max_length=10)
    signup_since = models.DateField()

    class Meta:
        db_table = 'User'


class Contact(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    contact_number = models.BigIntegerField()

    class Meta:
        db_table = 'Contact'
        unique_together = (('user', 'contact_number'),)


class Login(models.Model):
    login_username = models.CharField(primary_key=True, max_length=30)
    login_password = models.CharField(max_length=50)
    user = models.ForeignKey('User',  on_delete=models.CASCADE)

    class Meta:
        db_table = 'Login'


class Gallery(models.Model):
    user = models.ForeignKey('User',  on_delete=models.CASCADE)
    photo_oid = models.BigIntegerField(primary_key=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'Gallery'


class PhotoTags(models.Model):
    photo_oid = models.OneToOneField(Gallery,  db_column='photo_oid', on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'Photo Tags'
        unique_together = (('photo_oid', 'tag_name'),)


class Traveller(models.Model):
    traveller = models.OneToOneField('User',  primary_key=True, on_delete=models.CASCADE)
    is_fully_vaccinated = models.BooleanField()
    vacctination_certificate_oid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Traveller'


class FavouriteTours(models.Model):
    traveller = models.OneToOneField('Traveller',  on_delete=models.CASCADE)
    tour_type = models.CharField(max_length=50)

    class Meta:
        db_table = 'Favourite_Tours'
        unique_together = (('traveller', 'tour_type'),)


class Employee(models.Model):
    employee_id = models.OneToOneField('User',  primary_key=True, on_delete=models.CASCADE)
    salary = models.IntegerField()
    supervisor = models.ForeignKey('self',  blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'Employee'


class TravelAgency(models.Model):
    agency_id = models.IntegerField(primary_key=True)
    agency_name = models.CharField(max_length=50)
    street_address = models.CharField(db_column='street_address', max_length=50)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    email_id = models.TextField()
    no_of_employees = models.IntegerField()
    total_tour_packages = models.IntegerField()
    customer_care_number = models.BigIntegerField()

    class Meta:
        db_table = 'Travel Agency'


class BankAccountDetails(models.Model):
    account_number = models.BigIntegerField()
    account_holder_name = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=50)
    ifsc_code = models.CharField(db_column='IFSC_code', max_length=20)  # Field name made lowercase.
    agency = models.OneToOneField('TravelAgency',  primary_key=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Bank Account Details'


class TravelAgent(models.Model):
    agent = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True)
    salary = models.FloatField()
    agency = models.ForeignKey(TravelAgency,  on_delete=models.CASCADE)
    manager = models.ForeignKey('self',  blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'Travel Agent'


class TourPackage(models.Model):
    package_id = models.IntegerField(primary_key=True)
    package_name = models.CharField(db_column='Package_name', max_length=50)  # Field name made lowercase.
    agency = models.ForeignKey('TravelAgency',  on_delete=models.CASCADE)
    vehicle = models.CharField(max_length=20)
    duration = models.IntegerField()
    package_amount = models.DecimalField(max_digits=65535, decimal_places=65535)
    rating = models.FloatField()
    guide_availability = models.BooleanField(blank=True, null=True)
    rulebook_oid = models.BigIntegerField()

    class Meta:
        db_table = 'Tour Package'


class Activities(models.Model):
    package = models.OneToOneField('TourPackage',  on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Activities'
        unique_together = (('package_id', 'activity_name'),)


class Places(models.Model):
    package = models.OneToOneField('TourPackage',  on_delete=models.CASCADE)
    place_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    class Meta:
        db_table = 'Places'
        unique_together = (('package_id', 'place_name', 'city', 'country'),)


class TourTags(models.Model):
    package = models.OneToOneField(TourPackage,  on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'Tour tags'
        unique_together = (('package_id', 'tag_name'),)


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=50)
    package = models.ForeignKey('TourPackage',  on_delete=models.CASCADE)
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    provides_veg = models.BooleanField()
    provides_non_veg = models.BooleanField()
    rating = models.FloatField()
    link = models.CharField(max_length=50, null = True)

    class Meta:
        db_table = 'Hotel'
        unique_together = (('hotel_name', 'street_address', 'city', 'country', 'pincode'),)


class ScheduledOn(models.Model):
    schedule_id = models.IntegerField(primary_key=True)
    package = models.ForeignKey('TourPackage',  on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    available_seats = models.IntegerField()
    total_seats = models.IntegerField()

    class Meta:
        db_table = 'Scheduled_on'


class Feedback(models.Model):
    feedback_id = models.IntegerField(primary_key=True)
    description = models.CharField(db_column='Description', max_length=200, blank=True, null=True)  # Field name made lowercase.
    rating = models.IntegerField()
    traveller = models.ForeignKey('Traveller',  blank=True, null=True, on_delete=models.CASCADE)
    package = models.ForeignKey('TourPackage',  blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Feedback'


class Booking(models.Model):
    booking_id = models.IntegerField(primary_key=True)
    booking_date = models.DateField()
    no_of_seats = models.IntegerField()
    booking_status = models.CharField(max_length=20)
    traveller = models.ForeignKey('Traveller',  blank=True, null=True, on_delete=models.SET_NULL)
    package_detail = models.ForeignKey('ScheduledOn',  blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'Booking'


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    transaction_id = models.BigIntegerField(primary_key=True)
    payment_date = models.DateField()
    payment_time = models.TimeField(db_column='Payment_time')  # Field name made lowercase.
    payment_amount = models.FloatField()
    payment_mode = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20)

    class Meta:
        db_table = 'Payment'
        unique_together = (('booking', 'transaction_id', 'payment_date', 'payment_mode', 'payment_status'),)


class Cancelled(models.Model):
    booking = models.OneToOneField(Booking,  primary_key=True, on_delete=models.RESTRICT)
    cancel_date = models.DateField()
    cancel_time = models.TimeField()

    class Meta:
        db_table = 'Cancelled'


class RefundDetails(models.Model):
    booking = models.OneToOneField(Booking,  primary_key=True, on_delete=models.RESTRICT)
    refund_amount = models.FloatField(blank=True, null=True)
    refund_date = models.DateField(db_column='refund_ date')  # Field renamed to remove unsuitable characters.
    refund_time = models.TimeField()

    class Meta:
        db_table = 'Refund_details'


class RecommendedTo(models.Model):
    traveller = models.OneToOneField('Traveller',  on_delete=models.CASCADE)
    package_detail = models.ForeignKey('ScheduledOn',  on_delete=models.CASCADE)
    expires_on = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'Recommended_to'
        unique_together = (('traveller', 'package_detail'),)

