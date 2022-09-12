from django.db import models


class Place(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["placeId"], name="unique_placeId"
            )
        ]
    name = models.CharField(max_length=60)
    rate = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    placeId = models.CharField(max_length=70)
    latitude = models.DecimalField(max_digits=6, decimal_places=3)
    longitude = models.DecimalField(max_digits=6, decimal_places=3)


class Summary(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE)
    good = models.TextField()
    bad = models.TextField()
    neutral = models.TextField()


class Review(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["reviewId"], name="unique_reviewId"
            )
        ]
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    likes = models.IntegerField()
    reviewId = models.CharField(max_length=60)


class Token(models.Model):
    value = models.CharField(max_length=70)
    auth_to = models.CharField(max_length=50)


class QueryType(models.Model):
    sortBy = models.CharField(max_length=15)


class ReviewQuery(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    searchIndex = models.IntegerField(default=0)
    sortType = models.ForeignKey(QueryType, on_delete=models.DO_NOTHING, default=1)



