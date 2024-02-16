from django.contrib import admin
from .models import (
    Sessions,
    Question,
    Answer,
)


@admin.register(Question)
class QuestionaAdmin(admin.ModelAdmin):
    search_fields = (
        "game_id__contains",
        "round__contains",
        "question__contains",
        "answer__contains",
    )
    list_display = ("game_id", "round", "question", "answer")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields = ("session_id__contains", "team_name__contains", "answer__contains")
    list_display = ("session_id", "team_name", "answer", "timestamp")
