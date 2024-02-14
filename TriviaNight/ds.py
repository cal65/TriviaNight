import pandas as pd
import plotly.figure_factory as ff


def format_answers(df):
    df['Correct_Numeric'] = df['Correct'].astype(int)
    df['Question_Formatted'] = df['Question_Formatted'].str.replace('\\n', '<br>')
    df['Team_Number'] = pd.factorize(df['Name'])[0]
    return df

def answer_heatmap(df):
    fig = ff.create_annotated_heatmap(
        x=list(df['Team_Number'].unique()),
        y=list(df['Question_Formatted'].unique()),
        z=df['Correct_Numeric'].values.reshape(len(df['Question_Formatted'].unique()), -1),
    annotation_text = list(df['Answer'].values.reshape(len(df['Question_Formatted'].unique()), -1)),
    colorscale='Viridis',
    )
    # Replace y-axis labels with Team Names
    team_names = df.groupby('Team_Number')['Name'].first().tolist()
    fig.update_xaxes(tickvals=list(df['Team_Number'].unique()), ticktext=team_names, title='Team Name')

    # Add labels
    fig.update_layout(
        xaxis=dict(title='Question_Formatted'),
        title='Heatmap of Correct_Numeric values',
    )
    return fig

