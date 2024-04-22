# PubMedium

PubMedium is a Python API over a number of features of the PubMed REST API.

## First steps
In the following code snippet a list of instances of class `PubMedPublication` will be fetched that correspond to a PubMed REST search by the three topics: 'dicom', 'prostate', 'mri' (combined by 'AND').

```
topics = ['dicom', 'prostate', 'mri']

fetcher = PubMedFetcher()
publications = fetcher.fetch_by_topics(topics)

for publication in publications:
	print(publication)
```

fetcher = PubMedFetcher()
## Tasks where `PubMedFetcher` can be of use

* Onomastics. Researches about human names. Huge lists of real human names (the authors of the articles) have been created in applications.
* Creation of corpora on medical and healthcare relevant texts. 
* Bibliography. Fetching bibliographic data from articles.
* Still not defined. There are certainly more potential use cases...
