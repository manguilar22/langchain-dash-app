from dash import Dash, html
import dash_cytoscape as cyto

from lib import service
from lib import exporter

def generate_test():

    gene = service.summary('CCND1')
    ref = exporter.parse_cross_references(data=gene)

    edges = list()
    vertices = list()
    for item in ref:
        geneId = item['id']
        type = item['type']
        crossReferences = item['crossReferences']
        uniprotCrossReferences = item['uniProtKBCrossReferences'].split("|")

        edges.append({'data':{'id':geneId,'label':geneId}})
        edges.append({'data':{'id':type,'label':type.upper()}})
        edges.append(dict(data=dict(id=crossReferences,label=crossReferences)))

        vertices.append(dict(data=dict(source=geneId,target=type)))
        vertices.append(dict(data=dict(source=type,target=crossReferences)))

        for uniprot in uniprotCrossReferences:
            edges.append(dict(data=dict(id=uniprot,label=uniprot)))
            vertices.append(dict(data=dict(source=crossReferences,target=uniprot)))

    elements = sum([edges, vertices], [])
    return elements


app = Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        elements=generate_test()
    )
])

if __name__ == '__main__':
    app.run(debug=True)


