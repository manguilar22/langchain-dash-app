# Conversational UniProt Knowledge Base

## Abstract

UniProt serves as a comprehensive knowledge base for gene and protein data, made accessible to developers through a REST API. 
With the biological information present, text embeddings are created for each protein and gene within UniProt.
These embeddings enhance Chat-GPT's responses by providing a rich contextual foundation when addressing user queries. 
A methodology known as a retrieval-augmented generation chain, or simply RAG.

## Deployment 

```
docker-compose -f docker-compose.yaml up -d
```

Set the `OPENAI_SECRET_KEY` environment variable to enable Chat-GPT interaction. 

### Deployment with Authentication

In the docker-compose.yaml file you will have to set the **REDIS_PASSWORD** environment variable for the python container.
The password must match the command-line argument passed into redis. As an example: 

```yaml
...
    environment:
      REDIS_ARGS: "--requirepass myRedisPasswordHere"
```


## Prompt Engineering - Text Embeddings 

Create the statements to be used by Chat-GPT as context. - [recipe](https://python.langchain.com/docs/expression_language/cookbook/retrieval#conversational-retrieval-chain)

### Entry 

Template. 
```
the {} {} (UniProt: {}) in {} ({}) encodes a protein of {} amino acids with a molecular weight of {} Daltons. Found in the UniProt database as {}, the protein sequence is {}
```

Example Text
```
the EIF3C gene (UniProt: B5DFC8) in Rattus norvegicus (Rat) encodes a protein of 911 amino acids with a molecular weight of 105435 Daltons. Found in the UniProt database as UniProtKB reviewed (Swiss-Prot), the protein sequence is MMM....
```

### Comments

```
the {} {} (UniProt: {}) in the {} ({}) species has the following comment: \"{}\"
```

Example Text
```
"the FOXM1 gene (UniProt: Q08050) in the Homo sapiens (Human) species has the following comment: "Interacts with...""
```

### Cross References 
```
the {} {} (UniProt: {}) in the {} ({}) species has the following reference in the {} database: {}
```

Example Text:
```
"the EIF3C gene (UniProt: Q4QR58) in the Xenopus laevis (African clawed frog) species has the following reference in the AlphaFoldDB database: Q4QR58"
```

## UniProt

### Bioinformatics Datasource 

https://www.uniprot.org/help/programmatic_access

### [UniProt website REST API](https://www.uniprot.org/help/query-fields)

Lists all entries for proteins encoded by gene HPSE, but excluding variations like HPSE2 or HPSE_0.

```
https://rest.uniprot.org/uniprotkb/search?&query=gene_exact:MACO1
```

Lists all entries whose cluster of differentiation number is CD233.
```
https://rest.uniprot.org/uniprotkb/search?query=protein_name:CD233
```