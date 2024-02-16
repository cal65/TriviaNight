from django.db import models


class Sessions(models.Model):
    session_id = models.AutoField(primary_key=True)


class Question(models.Model):
    game_id = models.CharField(max_length=250)
    round = models.IntegerField()
    number = models.IntegerField()
    question = models.CharField(max_length=2500)
    answer = models.CharField(max_length=2500)


class Answer(models.Model):
    session_id = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=250)
    answer = models.CharField(max_length=2500)
    timestamp = models.DateTimeField()
