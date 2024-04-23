# PubMedium

PubMedium is a Python API for a number of features of the PubMed REST API (but not all of them!)

## Scope
The mini-library consists of two major classes, `PubMedFetcher` and `PubMedCorpusCreator`, and a few data classes, namely:
* PubMedAuthor
* PubMedPublication
* PubMedPublicationDate
* PubMedReference
* PubmedSelection
* XValues

## Class `PubMedFetcher`
Holds functionality to fetch PubMed publications by topics.
Its only public method, `fetch_by_topics(topics: list[str], from_year: int)` returns a list of instances of `PubMedPublication`. 
### Parameters
* `topics`: List of topics, e.g. `['dicom', 'prostate', 'mri']`. At the moment, the topics are combined by the AND operator for the PubMed REST query.
* `from_year`: The starting year of the publication. If omitted, the value 1800 is assumed (which hopefully guarantees the whole of the entries available).

### Code Snippet
The following snippet will fetch and print all Pubmed publications requested by 'dicom+prostate+mri' and print them.

```
topics = ['dicom', 'prostate', 'mri']

fetcher = PubMedFetcher()
publications = fetcher.fetch_by_topics(topics)

for publication in publications:
	print(publication)
```

### Tasks where `PubMedFetcher` can be of use

* Onomastics. Researches about human names. Huge lists of real human names (the authors of the articles) can be obtained (and have already been created in some applications).
* Using article abstracts to create corpora of medical and healthcare relevant texts. 
* Bibliography. Fetching bibliographic data from articles.
* Still not defined. There are certainly more potential use cases...

## Class `PubMedCorpusCreator`
Holds functionality for the creation of corpora based on full article texts.

Its only public method is 

```create_corpus(size: int, topics: list[str], output_folder: str, corpus_name: str,               create_abstracts: bool, create_bibtex: bool)```

### Parameters
* `size`: The maximum size of the corpus to create (if there are fewer articles for the combination of the topics, this number may not be reached)
* `topics`: List of topics to create the corpus from (combined by AND).
* `output_folder`: The name of the folder in which to create the corpus.                             If the folder does not exist, it will be created.
* `corpus_name`: The name of the subfolder of output_folder in which to write the text files.
                            If left empty, the corpus name will be created using the topics.
* `create_abstracts`: If set to true, a subfolder named "Abstracts" will be created in the corpus folder with the abstracts of the articles stored under their PMC IDs as file names.
* `create_bibtex`: If set to True, a file named `corpus_name.bib` will be created in the corpus folder with the BibTeX references to the articles.

### Purpose
The purpose of the class is to create corpora of medical and healthcare-relevant text from full texts of PubMed articles following topics.

### Code Snippet
The following code snippet will cause creation of a corpus named "dicom_pacs" in the directory `"C:/Temp"` as well as a subfolder with the article abstracts in it and a BibTeX file `dicom_pacs.bib`.
```
fetcher = PubMedCorpusCreator()
fetcher.create_corpus(50, ["dicom", "pacs"], "C:/Temp", "", True, True)
```
