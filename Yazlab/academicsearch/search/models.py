from djongo import models

class Makale(models.Model):
    baslik = models.CharField(max_length=200)
    yazarlar = models.CharField(max_length=200)
    aciklamalar = models.TextField()
    pdf_linki = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.baslik

    class Meta:
        db_table = 'makalebilgi'  # MongoDB koleksiyonu adı



