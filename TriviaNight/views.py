from django.shortcuts import render, redirect
from .sheet import grade_answers_from_sheets
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def index(request):
    """
    return templates/landing.html
    """
    t = "landing.html"
    return render(request, t)


def run_answers(request):
    """
    grab answers from googlesheets and grade
    """
    print(request)
    sheet_id = request.POST.get('sheet_id')
    round_number = request.POST.get('round_number')
    grade_answers_from_sheets(sheet_id, game_id='test', round_number=round_number, sheet_name='Form Responses 1')
    t = "landing.html"

    return JsonResponse({'message': 'Success'})




def heatmap_view(request):
    """
    return templates/heatmap.html
    """
    return render(request, "Graphs/heatmap_test.html")


def plot_heatmap(request):
    """
    return templates/heatmap.html
    """
    round_number = request.POST.get('round_number')
    heatmap_url = f"Graphs/heatmap_{round_number}.html"
    return redirect('heatmap')


