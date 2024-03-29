import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd
from .models import Answer, Sessions, Question
from .ds import score_question, objects_to_df

# initiate google sheets read objects
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

service = build("sheets", "v4", credentials=creds)
# Call the Sheets API
sheet = service.spreadsheets()


def get_spreadsheet_data(sheet_id, sheet_name):
    data_range = f"{sheet_name}!A1:Z20"
    result = sheet.values().get(spreadsheetId=sheet_id, range=data_range).execute()
    df = pd.DataFrame(result["values"][1:], columns=result["values"][0])
    return df


def ingest_answers(df, correct_answers, points, game_id, round, session):
    for i, row in df.iterrows():
        team_name = row[1]
        timestamp = pd.to_datetime(row["Timestamp"])
        for j in range(2, len(row)):
            answer = Answer()
            correct_answer = correct_answers[j-2]
            answer.timestamp = timestamp
            answer.team_name = team_name
            answer.game_id = game_id
            answer.round = round
            answer.answer = row[j]
            answer.session_id = session
            answer.number = j - 1
            answer.correct_numeric = score_question(row[j], correct_answer)
            answer.points = answer.correct_numeric * points[j-2]
            answer.save()


def ingest_questions(
    df,
    game_id,
    round_col="Round",
    number_col="Number",
    question_col="Question",
    point=1,
):
    for i, row in df.iterrows():
        question = Question()
        question.round = row[round_col]
        question.number = row[number_col]
        question.question = row[question_col]
        question.answer = row['Answer']
        question.game_id = game_id
        question.points = point
        question.save()

def score_round(game_id, session_id):
    answers = Answer.objects.filter(game_id=game_id, session_id=session_id)
    return answers


def grade_answers_from_sheets(sheet_id, game_id, round_number, sheet_name = 'Form Responses 1',
                              ):
    responses = get_spreadsheet_data(sheet_id, sheet_name)
    answers = objects_to_df(Question.objects.filter(game_id=game_id, round=round_number))
    session = Sessions.objects.get(session_id=2)
    ingest_answers(responses, correct_answers=answers['answer'],
                   points=answers['points'], game_id=game_id,
                   round=round_number,
                   session=session)

    return