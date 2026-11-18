"""Dependency-free BM25 search demo; no LLM, embeddings, credentials or paid API."""
import math
import re
from collections import Counter

def tokens(text):
    return re.findall(r'[a-z0-9]+', text.lower())

class SearchIndex:
    def __init__(self, documents):
        self.documents = list(documents)
        self.terms = [Counter(tokens(d['title'] + ' ' + d['text'])) for d in self.documents]
        self.lengths = [sum(t.values()) for t in self.terms]
        self.average = sum(self.lengths) / len(self.lengths) if self.lengths else 0
        self.df = Counter(term for terms in self.terms for term in terms)

    def search(self, query, limit=3):
        if limit < 1 or not self.average:
            return []
        hits = []
        for doc, terms, length in zip(self.documents, self.terms, self.lengths):
            score = 0
            for term in set(tokens(query)):
                frequency = terms.get(term, 0)
                if frequency:
                    idf = math.log(1 + (len(self.documents)-self.df[term]+0.5)/(self.df[term]+0.5))
                    score += idf * frequency * 2.5 / (frequency + 1.5*(0.25+0.75*length/self.average))
            if score:
                hits.append({**doc, 'score':round(score,4)})
        return sorted(hits, key=lambda x:(-x['score'],x['id']))[:limit]

DOCUMENTS = [
 {'id':'remote','title':'Remote working policy','text':'Remote schedules require manager agreement and team availability.'},
 {'id':'expenses','title':'Expense claims','text':'Submit expense receipts with a business justification for review.'},
 {'id':'leave','title':'Leave requests','text':'Request planned leave through the approval process before confirming dates.'}
]
if __name__ == '__main__':
    import argparse,json
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query')
    args=parser.parse_args()
    print(json.dumps(SearchIndex(DOCUMENTS).search(args.query),indent=2))
