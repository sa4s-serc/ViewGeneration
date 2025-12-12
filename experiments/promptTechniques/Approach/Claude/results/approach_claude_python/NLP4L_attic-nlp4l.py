from diagrams import Diagram, Cluster
from diagrams.programming.language import Java, Python, Scala
from diagrams.onprem.analytics import Spark
from diagrams.onprem.database import Mongodb
from diagrams.programming.framework import Spring

with Diagram("NLP4L Architecture", show=False, direction="TB"):
    with Cluster("Core Components"):
        core = [
            Spring("IWriter"),
            Spring("IReader"), 
            Spring("ISearcher"),
            Spring("Schema")
        ]

    with Cluster("Text Analysis"):
        analysis = [
            Spring("Analyzer"),
            Spring("AnalyzerBuilder"),
            Spring("Token")
        ]

    with Cluster("NLP Algorithms"):
        nlp = [
            Spring("HmmModel"),
            Spring("CollocationalAnalysis"),
            Spring("TermsExtractor")
        ]

    with Cluster("Languages"):
        langs = [
            Java("Java API"),
            Scala("Scala Core"),
            Python("Python Utils")
        ]

    with Cluster("Storage"):
        storage = Mongodb("Index Storage")

    # Connect components
    for c in core:
        c >> storage
    
    for a in analysis:
        a >> core[0]
        a >> core[1]

    for n in nlp:
        n >> analysis[0]
        n >> storage

    for l in langs:
        l >> core[0]
        l >> core[1]
        l >> core[2]