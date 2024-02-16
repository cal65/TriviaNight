import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd
from models import Answer, Sessions, Question

# initiate google sheets read objects
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

service = build("sheets", "v4", credentials=creds)
# Call the Sheets API
sheet = service.spreadsheets()


def get_spreadsheet_data(sheet_id, sheet_name):
    data_range = f"{sheet_name}!A1:M20"
    result = sheet.values().get(spreadsheetId=sheet_id, range=data_range).execute()
    df = pd.DataFrame(result["values"][1:], columns=result["values"][0])
    return df


def create_answers_objects(df, session):
    for i, row in df.iterrows():
        answer = Answer()
        team_name = row[1]
        timestamp = pd.to_datetime(row["Timestamp"])
        for j in range(2, len(row)):
            answer.timestamp = timestamp
            answer.team_name = team_name
            answer.answer = row[j]
            answer.session_id = session
            answer.number = j - 1
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
        question.answer = row["Answer"]
        question.game_id = game_id
        question.point = point
        question.save()
