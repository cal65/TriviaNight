import Levenshtein
import pandas as pd
import plotly.figure_factory as ff

def format_answers(df):
    df["Correct_Numeric"] = df["Correct"].astype(int)
    df["Question_Formatted"] = df["Question_Formatted"].str.replace("\\n", "<br>")
    df["Team_Number"] = pd.factorize(df["Name"])[0]
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
        correct_num = round(sim*2)/2
        correct_num = max(0, correct_num)
    return correct_num


def objects_to_df(objects):
    df = pd.DataFrame.from_records(objects.values())
    return df


def match_questions_to_answers(questions, answers):


    return

def answer_heatmap(df):
    fig = ff.create_annotated_heatmap(
        x=list(df["Team_Number"].unique()),
        y=list(df["Question_Formatted"].unique()),
        z=df["Correct_Numeric"].values.reshape(
            len(df["Question_Formatted"].unique()), -1
        ),
        annotation_text=list(
            df["Answer"].values.reshape(len(df["Question_Formatted"].unique()), -1)
        ),
        colorscale="Viridis",
    )
    # Replace y-axis labels with Team Names
    team_names = df.groupby("Team_Number")["Name"].first().tolist()
    fig.update_xaxes(
        tickvals=list(df["Team_Number"].unique()),
        ticktext=team_names,
        title="Team Name",
    )

    # Add labels
    fig.update_layout(
        xaxis=dict(title="Question_Formatted"),
        title="Heatmap of Correct_Numeric values",
    )
    return fig


def run_heatmap(answers, round_number):
    answers = format_answers(answers)
    fig = answer_heatmap(answers)
    fig.write_html(f"templates/Graphs/heatmap_{round_number}.html")
    return fig

