
from django.db import models

# Create your models here.
class Home(models.Model):
    title       = models.CharField(max_length=50, verbose_name="Başlık")
    description = models.CharField(max_length=500, verbose_name="Açıklama")
    link        = models.CharField(max_length=50, verbose_name="Web Site Linki")
    email       = models.CharField(max_length=50, verbose_name="E-Posta")
    image = models.ImageField(upload_to='uploads/form',verbose_name="Resim")
    statu       = models.BooleanField(verbose_name="Statu")
    code        = models.CharField(max_length=32, verbose_name="Form Doğrulama Kodu")

    def __str__(self) -> str:
        return self.title

