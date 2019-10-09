from django.db import models

# Create your models here.


class CreateStudentModel(models.Model):

	Name = models.CharField(max_length=126)
	Email = models.EmailField()
	Branch = models.CharField(max_length=126)
	Year = models.IntegerField(default=0)
	placementValue = models.CharField(max_length=126,default='none',null=True)

	def __str__(self):
		return self.Name