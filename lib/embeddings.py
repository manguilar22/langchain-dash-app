

def datasets_embeddings(datasetsArray):
    datasetsStr = []

    for dataset in datasetsArray:
        phrase = "the {} {} (UniProt: {}) in {} ({}) encodes a protein of {} amino acids with a molecular weight of {} Daltons. Found in the UniProt database as {}, the protein sequence is {}".format(
            dataset['geneName'],
            dataset['type'],
            dataset['primaryAccession'],
            dataset['scientificName'],
            dataset['commonName'],
            dataset['length'],
            dataset['molWeight'],
            dataset['entryType'],
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
                phrase = "the {} {} from the {} {} species with a primary accession code of {} has the following comment: \"{}\"".format(
                record['id'],
                record['type'],
                record['scientificName'],
                record['commonName'],
                record['primaryAccession'],
                geneComment
            )
                embeddingsStr.append(phrase)

    return embeddingsStr