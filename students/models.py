from django.db import models

EXAM_CHOICES = [
    ('HP Police', 'HP Police'),
    ('SSC', 'SSC'),
    ('Army', 'Army'),
    ('Home Guard', 'Home Guard'),
    ('Railway', 'Railway'),
    ('Banking', 'Banking'),
]

class Student(models.Model):

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    exam = models.CharField(
        max_length=50,
        choices=EXAM_CHOICES
    )

    aadhaar = models.FileField(upload_to='aadhaar/')
    marksheet = models.FileField(upload_to='marksheets/')
    photo = models.ImageField(upload_to='photos/')
    signature = models.ImageField(upload_to='signatures/')

    # NEW CHECKBOXES
    widow = models.BooleanField(default=False)
    bpl = models.BooleanField(default=False)
    irdp = models.BooleanField(default=False)

    physical_training = models.BooleanField(default=False)

    undertaking = models.BooleanField(default=False)
    training_type = models.CharField(max_length=50, default="Written")
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name