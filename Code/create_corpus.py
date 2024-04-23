from pubmed_corpus_creator import PubMedCorpusCreator


print("Welcome at Pubmedium Corpus Creator!")

string_size = input("Size=")
try:
    size = int(string_size)
except:
    print("You were supposed to input an integer number. Please try again!")
    exit(1)

string_topics = input("Topics (comma separated):")
topics = string_topics.split(',')

output_folder = input("Output folder=")
corpus_name = input("Corpus name (Enter to use the default value)")
string_create_abstracts = input("Create abstracts (y/n)? Enter to use default (True)")
create_abstracts = bool(string_create_abstracts)
string_create_bibtex = input("Create BibTeX (y/n)? Enter to use default (True)")
create_bibtex = bool(string_create_bibtex)

fetcher = PubMedCorpusCreator()

fetcher.create_corpus(size, topics, output_folder, corpus_name, create_abstracts, create_bibtex)



