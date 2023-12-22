def datasets_embeddings(datasetsArray):
    datasetsStr = []

    for dataset in datasetsArray:
        phrase = "the {} {} (UniProt: {}) in {} ({}) encodes a {} of {} amino acids with a molecular weight of {} Daltons. Found in the UniProt database as {}, the {} sequence is {}".format(
            dataset['geneName'],
            dataset['type'],
            dataset['primaryAccession'],
            dataset['scientificName'],
            dataset['commonName'],
            dataset['type'],
            dataset['length'],
            dataset['molWeight'],
            dataset['entryType'],
            dataset['type'],
            dataset['sequence'],
        )
        datasetsStr.append(phrase)

    return datasetsStr


def comments_embeddings(commentsArray):
    embeddingsStr = []

    for record in commentsArray:
        for geneComment in record['comments'].split("|"):
            if geneComment == '' or geneComment is None:
                print(f'comment = {geneComment}')
            else:
                phrase = "the {} {} (UniProt: {}) in the {} ({}) species has the following comment: \"{}\"".format(
                    record['id'],
                    record['type'],
                    record['primaryAccession'],
                    record['scientificName'],
                    record['commonName'],
                    geneComment
                )
                embeddingsStr.append(phrase)

    return embeddingsStr


def references_embeddings(referencesArray):
    embeddings = []

    for record in referencesArray:
        if record == '' or record is None:
            print(f'cross_references = {record}')
        else:
            phrase = "the {} {} (UniProt: {}) in the {} ({}) species has the following reference in the {} database: {}".format(
                record['id'],
                record['type'],
                record['primaryAccession'],
                record['scientificName'],
                record['commonName'],
                record['crossReferences'],
                record['uniProtKBCrossReferences'].replace('|', ',')
            )
            embeddings.append(phrase)

    return embeddings
