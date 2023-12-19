import requests


def _gene_summary_request(gene_id):
    uniprotUrl = f'https://rest.uniprot.org/uniprotkb/search?&query=gene_exact:{gene_id}'
    request = requests.get(uniprotUrl)
    jsonData = request.json()

    return jsonData if 'results' in jsonData else dict(results=[])


def _protein_summary_request(protein_id):
    uniprotURL = f'https://rest.uniprot.org/uniprotkb/search?query=protein_name:{protein_id}'
    request = requests.get(uniprotURL)
    jsonData = request.json()

    return jsonData if 'results' in jsonData else dict(results=[])


def _summary_parse(id, jsonResponse):
    results = jsonResponse['results']
    summary = []

    for record in results:
        print(f'({id}) JSON records={len(results)}, summary={len(summary) + 1}')

        entryType = record['entryType']
        primaryAccession = record['primaryAccession']
        scientificName = record['organism']['scientificName']
        commonName = record['organism']['commonName'] if 'commonName' in record['organism'] else ""
        sequence = record['sequence']
        geneName = id

        comments = record['comments'] if 'comments' in record else []
        features = record['features'] if 'features' in record else []
        uniProtKBCrossReferences = record['uniProtKBCrossReferences']

        summary.append(dict(geneName=geneName.upper(),
                            entryType=entryType,
                            primaryAccession=primaryAccession,
                            scientificName=scientificName,
                            commonName=commonName,
                            sequence=sequence['value'],
                            length=sequence['length'],
                            molWeight=sequence['molWeight'],
                            comments=comments,
                            features=features,
                            uniProtKBCrossReferences=uniProtKBCrossReferences
                            ))

    return summary


def summary(id):

    gene = _gene_summary_request(gene_id=id)
    protein = _protein_summary_request(protein_id=id)
    summary = dict()

    if gene['results']:
        summary.update({'gene':_summary_parse(id, gene)})

    if protein['results']:
        summary.update({'protein': _summary_parse(id, protein)})

    return summary

