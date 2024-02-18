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
    list_display = ("game_id", "round", "question", "answer", "points")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields = ("session_id__contains", "team_name__contains", "answer__contains")
    list_display = ("session_id", "round", "number", "team_name", "answer", "points", "correct_numeric", "timestamp")

@admin.register(Sessions)
class SessionAdmin(admin.ModelAdmin):
    search_fields = ("session_id__contains",)
    list_display = ("session_id",)


