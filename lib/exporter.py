import pandas as pd


def parse_cross_references(data:dict):
    cross_references = list()

    for type in data.keys():
        # ['geneName', 'entryType', 'primaryAccession', 'scientificName', 'commonName', 'sequence', 'length', 'molWeight', 'comments', 'features', 'uniProtKBCrossReferences']
        for record in data.get(type):
            if 'uniProtKBCrossReferences' not in record:
                print('uniProtKBCrossReferences is not present in summary.')
                return []
            else:
                uniProtKBCrossReferences = record['uniProtKBCrossReferences']
                geneName = record['geneName']
                primaryAccession = record['primaryAccession']
                scientificName = record['scientificName']
                commonName = record['commonName']
                entryType = record['entryType']

                labels = ['GO', 'InterPro', 'Pharos', 'ChEMBL', 'Reactome', 'KEGG', 'AlphaFoldDB']

                for label in labels:
                    x = [i['id'] for i in uniProtKBCrossReferences if i['database'] == label]
                    if x:
                        references = dict(id=geneName,
                                          type=type,
                                          entryType=entryType,
                                          primaryAccession=primaryAccession,
                                          scientificName=scientificName,
                                          commonName=commonName, crossReferences=label,
                                          uniProtKBCrossReferences="|".join(x))
                        cross_references.append(references)

    return cross_references


def parse_comments(data:dict):
    results = []
    for k in data.keys():
        for record in data.get(k):
            if 'comments' not in record:
                pass
            else:
                geneName = record['geneName']

                comments = sum([[j['value'] for j in i.get("texts", [])] for i in record['comments']], [])
                value = "|".join(comments)
                results.append({"id":geneName,"type": k,
                                'primaryAccession':record['primaryAccession'],
                                'scientificName': record['scientificName'],
                                'commonName': record['commonName'],
                                'comments': value})

    return results


def summary_dataset(data:dict):
    results = []
    for k in data.keys():
        for record in data.get(k):
            del record['comments']
            del record['features']
            del record['uniProtKBCrossReferences']

            record.update({"type":k})
            results.append(record)
    return results


def csv_text(data:dict, columns:list=None):

    if columns:
        df = pd.DataFrame(data, columns=columns)
    else:
        df = pd.DataFrame(data)

    header = ",".join(df.columns)

    txt = f'{header}\n'

    for _, row in df.iterrows():
        line = ",".join(str(v) for v in row.tolist())
        txt += '{}\n'.format(line)

    return txt

