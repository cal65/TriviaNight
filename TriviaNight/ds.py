import Levenshtein
import pandas as pd
import textwrap
import plotly.figure_factory as ff
from plotly import graph_objects as go
from TriviaNight.models import Answer, Question


def format_answers(df, n=40):
    df["question_formatted"] = df["question"].apply(lambda x: textwrap.fill(x, 30))
    df["question_formatted"] = df["question_formatted"].str.replace("\\n", "<br>")
    df["answer"] = df["answer"].apply(lambda x: textwrap.fill(x, 20))
    df["answer"] = df["answer"].str.replace("\\n", "<br>")
    df["team_number"] = pd.factorize(df["team_name"])[0]
    return df


def jaccard_similarity(str1, str2):
    a = set(str1)
    b = set(str2)
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def score_question(question, answer):
    # Merge the two dataframes on the question
    if answer in question:
        correct_num = 1
    else:
        # string distance between question and answer
        # help me
        sim = 1 - (Levenshtein.distance(question, answer) / len(answer))
        # find if closest to 0, 0.5 or 1 and return
        correct_num = round(sim * 2) / 2
        correct_num = max(0, correct_num)
    return correct_num


def objects_to_df(objects):
    df = pd.DataFrame.from_records(objects.values())
    return df


def match_questions_to_answers(questions, answers):
    return


def answer_heatmap(df):
    df.sort_values(["number", "team_number"], inplace=True, ascending=False)
    df.reset_index(drop=True)
    print(df)
    fig = ff.create_annotated_heatmap(
        x=list(df["team_number"].unique())[::-1],
        y=list(df["question_formatted"].unique()),
        z=df["points"].values.reshape(
            len(df["question_formatted"].unique()), -1
        ),
        text=df["answer"].values.reshape(len(df["question_formatted"].unique()), -1),
        annotation_text=list(
            df["answer"].values.reshape(len(df["question_formatted"].unique()), -1)
        ),
        hoverinfo='text',
        colorscale="Viridis",
    )
    # Replace y-axis labels with Team Names
    team_names = df.groupby("team_number")["team_name"].first().tolist()
    fig.update_xaxes(
        tickvals=list(df["team_number"].unique()),
        ticktext=team_names,
        title="Team Name",
    )

    # Add labels
    fig.update_layout(
        xaxis=dict(title="Question_Formatted"),
        title="Heatmap of Graded Responses",
    )
    line_count = sum(s.count("<br>") for s in df["question_formatted"].unique()) + len(
        df["question_formatted"].unique()
    )
    fig.update_layout(
        width=100 * df.shape[1],  # Adjust width as needed
        height=25 * line_count,  # Adjust height as needed
    )
    return fig


def get_data_for_heatmap(round_number, game_id):
    answers_df = objects_to_df(
        Answer.objects.filter(round=round_number, game_id=game_id)
    )
    questions_df = objects_to_df(
        Question.objects.filter(round=round_number, game_id=game_id)
    )
    answer_cols = [
        "team_name",
        "round",
        "number",
        "points",
        "correct_numeric",
        "answer",
        "game_id",
    ]
    questions_df.rename(columns={"answer": "correct_answer"}, inplace=True)
    q_cols = ["game_id", "round", "number", "correct_answer", "question"]
    combined_df = pd.merge(
        answers_df[answer_cols],
        questions_df[q_cols],
        on=["game_id", "round", "number"],
        how="left",
    )
    return combined_df


def run_heatmap(round_number, game_id):
    df = get_data_for_heatmap(round_number, game_id)
    df = format_answers(df)
    fig = answer_heatmap(df)
    fig.write_html(f"TriviaNight/templates/Graphs/heatmap_{round_number}.html")
    return fig


def plot_team_scores(game_id):
    game = objects_to_df(Answer.objects.filter(game_id=game_id))
    round_scores = pd.pivot_table(
        game, index=["team_name", "round"], values="points", aggfunc="sum"
    ).reset_index()
    fig = go.Figure()
    for r in [1, 2, 3, 4, 5]:
        rdf = round_scores.loc[round_scores["round"] == r]
        fig.add_trace(
            go.Bar(y=rdf["team_name"],
                   x=rdf["points"],
                   customdata=rdf["round"],
                   hovertemplate="<b>Team:</b> %{y}<br><b>Round:</b> %{customdata}</b><br><b>Points:</b> %{x}<br><extra></extra>",
                   name=r, orientation="h"),
        )
    fig.update_layout(barmode="stack", title="Team Scores", legend=dict(title="Round"))
    fig.write_html(f"TriviaNight/templates/Graphs/team_scores_{game_id}.html")
    return fig
