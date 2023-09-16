from django.db import models


class Historico(models.Model):
    create_at = models.CharField(max_length=30)
    hour = models.CharField(max_length=30, null=True)
    minute = models.CharField(max_length=30, null=True)
    color = models.CharField(max_length=30)
    numero = models.IntegerField()
    identificador = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.color

class Sequencia(models.Model):
    p1 = models.CharField(max_length=10)
    p2 = models.CharField(max_length=10)
    p3 = models.CharField(max_length=10)
    p4 = models.CharField(max_length=10)
    p5 = models.CharField(max_length=10)
    result = models.CharField(max_length=10)

    def __str__(self):
        return self.p1


class Configuracao(models.Model):
        api_telegram = models.CharField(max_length=2000)
        id_sala_telegram = models.CharField(max_length=200)
        
