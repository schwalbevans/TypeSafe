from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine


class checkForPii:   
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()


    def analyze_text_for_pii(self, text):
        results = self.analyzer.analyze(text=text, language='en')
        finalResults = self.anonymizer.anonymize(text=text, analyzer_results=results)
        return finalResults.text