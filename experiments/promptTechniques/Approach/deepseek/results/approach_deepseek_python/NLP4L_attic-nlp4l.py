from diagrams import Diagram
from diagrams.programming.language import Java, Scala
from diagrams.generic.blank import Blank
from diagrams.aws.ml import MachineLearning
from diagrams.generic.os import LinuxGeneral
from diagrams.elastic.elasticsearch import Elasticsearch

with Diagram("NLP4L Library Architecture", show=False, direction="TB"):
    with Diagram("Core Layer"):
        lucene = Elasticsearch("Apache Lucene")
        schema = Blank("Schema Management")
        indexing = Blank("Indexing")
        search = Blank("Searching")
        
        lucene >> schema
        schema >> indexing
        schema >> search

    with Diagram("Analysis Layer"):
        text_analysis = Blank("Text Analysis")
        japanese_analysis = Blank("Japanese Analysis")
        nlp_algorithms = Blank("NLP Algorithms")
        
        text_analysis >> japanese_analysis
        text_analysis >> nlp_algorithms

    with Diagram("Application Layer"):
        repl = Blank("REPL")
        corpus = Blank("Corpus Handling")
        features = Blank("Feature Extraction")
        synonyms = Blank("Synonym Management")
        
        repl - corpus
        repl - features
        repl - synonyms

    core_layer = [lucene, schema, indexing, search]
    analysis_layer = [text_analysis, japanese_analysis, nlp_algorithms]
    application_layer = [repl, corpus, features, synonyms]
    
    for core in core_layer:
        for analysis in analysis_layer:
            core >> analysis
            
    for analysis in analysis_layer:
        for app in application_layer:
            analysis >> app