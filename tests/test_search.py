import unittest
from search import SearchIndex, DOCUMENTS
class RetrievalTests(unittest.TestCase):
    def test_relevance(self):
        self.assertEqual(SearchIndex(DOCUMENTS).search('remote schedules')[0]['id'],'remote')
    def test_no_evidence(self):
        self.assertEqual(SearchIndex(DOCUMENTS).search('astronomy telescope'),[])
    def test_empty(self):
        self.assertEqual(SearchIndex([]).search('remote'),[])
    def test_empty_text(self):
        self.assertEqual(SearchIndex([{'id':'x','title':'','text':''}]).search('remote'),[])
    def test_limit(self):
        self.assertEqual(len(SearchIndex(DOCUMENTS).search('remote leave',1)),1)
    def test_normalization(self):
        idx=SearchIndex(DOCUMENTS)
        self.assertEqual(idx.search('REMOTE!'),idx.search('remote'))
if __name__=='__main__':unittest.main()
