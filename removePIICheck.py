from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine


class checkForPii:   
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()


    def analyze_text_for_pii(self, text):
        results = self.analyzer.analyze(text=text, language='en')
        print(results)
        return results
    
    def anonymize_text_for_pii(self, text): 
        results = self.analyze_text_for_pii(text)
        finalResults = self.anonymizer.anonymize(text=text, analyzer_results=results)
        return finalResults.text