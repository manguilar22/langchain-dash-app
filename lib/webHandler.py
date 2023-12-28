import os

from .service import summary as getSummary
from .cache import Cache
from .exporter import summary_dataset, parse_comments, parse_cross_references
from .embeddings import comments_embeddings, datasets_embeddings, references_embeddings


REDIS_HOST = os.getenv('REDIS_HOST','127.0.0.1')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)


def _stripInput(inputValueStr):
    return inputValueStr.replace(" ","").replace("\"","")


def createEmbeddings(inputValue):
    datasetEmbeddings = createCommentsEmbeddings(inputValue)
    commentsEmbeddings = createDatasetEmbeddings(inputValue)
    referencesEmbeddings = createCrossReferenceEmbeddings(inputValue)

    stringEmbeddings = sum([datasetEmbeddings,commentsEmbeddings,referencesEmbeddings], [])
    return stringEmbeddings


def createDatasetEmbeddings(inputValue):
    print(f'dataset embeddings input: {inputValue}')

    try:
        cache = Cache(REDIS_HOST, REDIS_PASSWORD)

        embeddings = []

        for key in _stripInput(inputValue).split(","):
            commentEmbeddings = cache.db.json().get(f'dataset_embeddings:{key.strip()}')

            if commentEmbeddings:
                print(f'cache hit for dataset_embeddings:{key.strip()}')
                embeddings.extend(commentEmbeddings)
            elif key != '':
                print(f'cache miss for dataset_embeddings:{key.strip()}')
                dataset = cache.db.json().get(f'dataset:{key.strip()}')
                vectors = datasets_embeddings(datasetsArray=dataset)
                cache.db.json().set(f'dataset_embeddings:{key.strip()}', '$', vectors)
                embeddings.extend(vectors)
            else:
                print(f'empty string: {key}')

        return embeddings
    except Exception as err:
        print(f'comments embeddings, error={err}')
        return []
    finally:
        cache.db.close()


def createCrossReferenceEmbeddings(inputValue):
    print(f'cross references embeddings input: {inputValue}')

    try:
        cache = Cache(REDIS_HOST, REDIS_PASSWORD)

        embeddings = []

        for key in _stripInput(inputValue).split(","):
            commentEmbeddings = cache.db.json().get(f'references_embeddings:{key.strip()}')

            if commentEmbeddings:
                print(f'cache hit for references_embeddings:{key.strip()}')
                embeddings.extend(commentEmbeddings)
            elif key != '':
                print(f'cache miss for references_embeddings:{key.strip()}')
                references = cache.db.json().get(f'references:{key.strip()}')
                vectors = references_embeddings(references)
                cache.db.json().set(f'references_embeddings:{key.strip()}','$',vectors)
                embeddings.extend(vectors)
            else:
                print(f'empty string: {key}')

        return embeddings

    except Exception as err:
        print(f'cross references embedding={err}')
        return []
    finally:
        cache.db.close()


def createCommentsEmbeddings(inputValue):
    print(f'comments embeddings input: {inputValue}')

    try:
        cache = Cache(REDIS_HOST, REDIS_PASSWORD)

        embeddings = []

        for key in _stripInput(inputValue).split(","):
            commentEmbeddings = cache.db.json().get(f'comments_embeddings:{key.strip()}')

            if commentEmbeddings:
                print(f'cache hit for comments_embeddings:{key.strip()}')
                embeddings.extend(commentEmbeddings)
            elif key != '':
                print(f'cache miss for comments_embeddings:{key.strip()}')
                comments = cache.db.json().get(f'comments:{key.strip()}')
                vectors = comments_embeddings(commentsArray=comments)
                cache.db.json().set(f'comments_embeddings:{key.strip()}','$',vectors)
                embeddings.extend(vectors)
            else:
                print(f'empty string: {key}')

        return embeddings
    except Exception as err:
        print(f'comments embeddings, error={err}')
        return []
    finally:
        cache.db.close()


def handleDatasets(inputValue):
    try:
        cache = Cache(REDIS_HOST, REDIS_PASSWORD)

        summaries = []
        for record in _stripInput(inputValue).split(","):
            cacheHit = cache.db.json().get(f'summary:{record}')
            if cacheHit:
                print(f'cache hit for summary of {record}')
                datasetHit = cache.db.json().get(f'dataset:{record}')

                if datasetHit:
                    print(f'cache hit for dataset of {record}')
                    summaries.extend(datasetHit)
                else:
                    x = summary_dataset(cacheHit)
                    summaries.extend(x)
                    cache.db.json().set(f'dataset:{record}','$',x)

        return summaries

    except Exception as err:
        print(err)
        return summaries
    finally:
        cache.db.close()


def handleComments(inputValue):
    try:
        cache = Cache(REDIS_HOST, REDIS_PASSWORD)

        summaries = []
        for record in _stripInput(inputValue).split(","):
            cacheHit = cache.db.json().get(f'summary:{record}')
            if cacheHit:
                print(f'cache hit for summary of {record}')
                datasetHit = cache.db.json().get(f'comments:{record}')

                if datasetHit:
                    print(f'cache hit for comments of {record}')
                    summaries.extend(datasetHit)
                else:
                    print(f'cache miss for comments of {record}')
                    x = parse_comments(cacheHit)
                    summaries.extend(x)
                    cache.db.json().set(f'comments:{record}', '$', x)

        return summaries

    except Exception as err:
        print(err)
        return []
    finally:
        cache.db.close()


def handleCrossReferences(inputValue):
    try:
        cache = Cache(REDIS_HOST, REDIS_PASSWORD)

        summaries = []
        for record in _stripInput(inputValue).split(","):
            cacheHit = cache.db.json().get(f'summary:{record}')
            if cacheHit:
                print(f'cache hit for summary of {record}')
                datasetHit = cache.db.json().get(f'references:{record}')

                if datasetHit:
                    print(f'cache hit for references of {record}')
                    summaries.extend(datasetHit)
                else:
                    print(f'cache miss for references of {record}')
                    x = parse_cross_references(cacheHit)
                    summaries.extend(x)
                    cache.db.json().set(f'references:{record}', '$', x)

        return summaries

    except Exception as err:
        print(err)
        return []
    finally:
        cache.db.close()


def handleGeneInput(inputValue):
    try:
        db = Cache(REDIS_HOST,REDIS_PASSWORD).db
        if ',' in inputValue:
            summaries = []
            for i in _stripInput(inputValue).split(","):
                stripString = i.strip().replace("\"","")
                cacheHit = db.json().get(f'summary:{stripString}')
                if cacheHit:
                    print(f'cache hit for {stripString}')
                    summaries.append(cacheHit)
                else:
                    print(f'cache miss for {stripString}')
                    summary = getSummary(stripString)
                    summaries.append(summary)
                    db.json().set(f"summary:{stripString}","$",summary)
            return summaries
        else:
            strString = inputValue.strip().replace("\"","")
            cacheHit = db.json().get(f'summary:{strString}')
            if cacheHit:
                return [cacheHit]
            else:
                summary = getSummary(strString)
                if summary:
                    db.json().set(f'summary:{strString}', '$', summary)
                    return [summary]
    except Exception as err:
        raise err
    finally:
        db.close()