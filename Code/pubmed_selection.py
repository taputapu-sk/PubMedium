from enum import Enum


class PubmedSelection(Enum):
    """
    Different use cases depending on what you want to do with the fetched data.
    TODO: Update use cases and enable output selection in PubMedFetcher.fetch_by_topics().
    """
    FULL = 1                # Fetches all information if possible.
    ABSTRACT = 2            # Fetches abstracts only.
    AUTHORS_SHORT = 3       # Fetches only the authors' names.
    AUTHORS_FULL = 4        # Fetches all authors' information, including affiliations and IDs.
    BIBLIO = 5              # Fetches only data needed for bibliography.
