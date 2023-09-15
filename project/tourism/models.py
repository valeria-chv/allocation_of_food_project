from django.db import models

class Tourists(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    food_weight = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tourists'
    
    def __str__(self):
    	return self.name
    	
    def get_absolute_url(self):
    	return reverse('tf_detail', args=[str(self.id)])


class Food(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    weight = models.IntegerField(blank=True, null=True)
    importance = models.IntegerField(blank=True, null=True)
    #used = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'food'
    
    def __str__(self):
    	return self.name


class Tf(models.Model):
	tour = models.ForeignKey('Tourists', models.DO_NOTHING, blank=True, null=True)
	food = models.ForeignKey(Food, models.DO_NOTHING, blank=True, null=True)
	id = models.IntegerField(primary_key=True)
	
	class Meta:
		managed = False
		db_table = 'tf'
	






