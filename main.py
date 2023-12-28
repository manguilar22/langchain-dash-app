import json
import os

from dash import Dash, html, dcc, Output, Input, State
from lib import exporter, webHandler, llm

DASH_DEBUG_FLAG = os.getenv('DEBUG', True)
OPENAPI_KEY = os.getenv('OPENAI_SECRET_KEY', None)
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')

app = Dash(__name__, suppress_callback_exceptions=True, assets_folder='assets')

app.layout = html.Div([
    html.Title(children='Conversational Tool'),
    html.H1(children='UniProt Conversational Portal'),
    html.A(id='uniprot-link', children='www.uniprot.org',href='https://www.uniprot.org/',target='_blank'),
    html.Div(children=[
        dcc.Input(id='gene-input-1', placeholder='type gene id or list of ids',name='gene-input-1'),
        html.Button(id='gene-button-submit', children='Submit', n_clicks=0, type='submit', name='gene-button-submit'),
        dcc.Loading(type='default', fullscreen=True, children=html.Div(id='loading-output-1',children=[]))
    ])
])


@app.callback(
    Output('loading-output-1', 'children'),
    Input('gene-button-submit', 'n_clicks'),
    State('gene-input-1', 'value'),
    prevent_initial_call=True
)
def loading_datasets(n_clicks, value):
    cleanString = value

    print(f'logs: n_clicks={n_clicks}, search_term={cleanString}')

    if cleanString is None or cleanString == '':
        return [
            html.P(
                children="Please provide a gene id or a comma-separated list of gene ids (eg. EIF3C or EIF4A1,FOXM1,EIF3C)"),
        ]

    data = webHandler.handleGeneInput(cleanString)
    datasets = sum(list(map(lambda x: exporter.summary_dataset(x), data)), [])
    txt = exporter.csv_text(data=datasets,
                            columns=["geneName", "type", "entryType", "primaryAccession", "scientificName",
                                     "commonName", "length", "molWeight"])

    return [
        dcc.Textarea(id='dataset', value=txt),
        html.P(id='dataset-closure', children='Note: The gene sequence was removed from the dataset above.'),
        html.Button(id='dataset-download-button', children='Download Dataset'),
        dcc.Download(id='dataset-download-output'),
        html.Button(id='comments-download-button', children='Download Comments'),
        dcc.Download(id='comments-download-output'),
        html.Button(id='cross-references-download-button', children='Download Cross References'),
        dcc.Download(id='cross-references-download-output'),
        html.Hr(),
        html.Div(id="chatgpt-operations", children=[
            html.H3(children='ChatGPT Interaction'),
            dcc.Input(id='chatgpt-input',name='chatgpt-input',type='text',placeholder='Talk to ChatGPT about your dataset.'),
            html.Button(id='chatgpt-button-submit', name='chatgpt-button-submit', type='submit', n_clicks=0, children='Ask'),
            html.Div(id='chatgpt-response', children=[])
        ])]


@app.callback(Output('chatgpt-response', 'children'),
              Input('chatgpt-button-submit', 'n_clicks'),
              State('gene-input-1', 'value'),
              State('chatgpt-input', 'value'),
              prevent_initial_call=True
              )
def chatgpt_response(chatGptButtonClick,geneInputValue,humanInputValue):
    print(f'chatgpt response: button_submit={chatGptButtonClick}, gene-input={geneInputValue}, humanInputValue={humanInputValue}')

    if humanInputValue is None or humanInputValue == '':
        webHandler.handleDatasets(geneInputValue)
        webHandler.handleComments(geneInputValue)
        webHandler.handleCrossReferences(geneInputValue)

        return [dcc.Markdown("""### Talk to ChatGPT about your dataset.""")]
    else:
        try:
            #datasets = webHandler.handleDatasets(geneInputValue)
            #comments = webHandler.handleComments(geneInputValue)
            #references = webHandler.handleCrossReferences(geneInputValue)

            stringEmbeddings = webHandler.createEmbeddings(geneInputValue)

            if OPENAPI_KEY:
                print(f'Langchain Enabled, embeddings size={len(stringEmbeddings)}')
                chatGPT = llm.LLM(OPENAPI_KEY)
                chain = chatGPT.embeddings_chain(processedVectors=stringEmbeddings)
                content = chain.invoke(dict(question=humanInputValue))
                print(f'Langchain Response Done')
            else:
                content = "OPENAI API key has not been provided, chat-gpt is disabled."

            return [
                html.H3(children=f'Question: {humanInputValue}'),
                html.H4(children=f'Answer:'),
                dcc.Markdown(children=content),
                html.Button(id='chatgpt-context-download-button', children='Download Context Given'),
                dcc.Download(id='chatgpt-context-download-output'),
            ]
        except Exception as err:
            logMessage = html.P(children=f'error computing with text embeddings: {err}')
            return [logMessage]


# Downloads

@app.callback(Output('chatgpt-context-download-output', 'data'),
              Input('chatgpt-context-download-button', 'n_clicks'),
              State('gene-input-1', 'value'))
def downloadChatGptContext(n_clicks, value):
    if not n_clicks is None:
        embeddings = webHandler.createEmbeddings(value)

        txt = json.dumps(embeddings)

        return dict(filename='context.json', content=txt)


@app.callback(Output('dataset-download-output','data'),
              Input('dataset-download-button','n_clicks'),
              State('gene-input-1', 'value'))
def datasetDownload(n_clicks, value):
    if not n_clicks is None:
        print(f'n_clicks: {n_clicks}, value:{value}')
        datasets = webHandler.handleDatasets(value)
        txt = exporter.csv_text(data=datasets)
        return dict(content=txt, filename='dataset.csv')


@app.callback(Output('comments-download-output', 'data'),
              Input('comments-download-button', 'n_clicks'),
              State('gene-input-1', 'value'))
def commentsDownload(n_clicks, value):
    if not n_clicks is None:
        print(f'n_clicks: {n_clicks}, value:{value}')
        comments = webHandler.handleComments(value)
        txt = json.dumps(comments)
        return dict(content=txt, filename='comments.json')


@app.callback(Output('cross-references-download-output','data'),
              Input('cross-references-download-button', 'n_clicks'),
              State('gene-input-1', 'value'))
def crossReferencesDownload(n_clicks, value):
    if not n_clicks is None:
        print(f'n_clicks: {n_clicks}, value:{value}')
        references = webHandler.handleCrossReferences(value)
        txt = exporter.csv_text(data=references)
        return dict(content=txt, filename='references.csv')


if __name__ == '__main__':
    app.run(debug=DASH_DEBUG_FLAG, host='0.0.0.0', port='8080')