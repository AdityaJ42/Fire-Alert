from django.db import models


class Volunteer(models.Model):
	name = models.CharField(max_length=150, blank=False)
	contact = models.CharField(max_length=10, blank=False)
	address = models.TextField()
	area = models.CharField(max_length=50)
	picture = models.ImageField(upload_to='pics/', blank=False)

	def __str__(self):
		return self.name


class FireStation(models.Model):
	name = models.CharField(max_length=200, blank=False)
	address = models.TextField()
	contact = models.CharField(max_length=10)

	def __str__(self):
		return self.name
