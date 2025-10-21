from diagrams import Diagram
from diagrams.custom import Custom
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.analytics import Spark
from diagrams.onprem.search import Solr
from diagrams.generic.database import SQL

with Diagram("NLP4L Architecture", show=False):
    client = Client("NLP4LILoop")
    repl = Custom("NLP4L REPL", "./icons/repl.png")
    schema_loader = Custom("SchemaLoader", "./icons/schema_loader.png")
    schema = Custom("Schema", "./icons/schema.png")
    iwriter = Custom("IWriter", "./icons/iwriter.png")
    ireader = Custom("IReader", "./icons/ireader.png")
    isearcher = Custom("ISearcher", "./icons/isearcher.png")
    analyzer = Custom("Analyzer", "./icons/analyzer.png")
    hmm_model = Custom("HmmModel", "./icons/hmm_model.png")
    corpus = Custom("Corpora", "./icons/corpus.png")
    synonym_records = Custom("SynonymRecords", "./icons/synonym_records.png")
    feature_selector = Custom("FeatureSelector", "./icons/feature_selector.png")
    transliteration_model = Custom("TransliterationModel", "./icons/transliteration_model.png")
    simple_fst = Custom("SimpleFST", "./icons/simple_fst.png")
    spark_mllib = Spark("Spark MLlib")
    lucene = Solr("Apache Lucene")
    sql_db = SQL("SQL Database")
    server = Server("Server")

    client >> repl
    repl >> schema_loader
    schema_loader >> schema
    schema >> iwriter
    iwriter >> lucene
    schema >> ireader
    ireader >> lucene
    lucene >> isearcher
    isearcher >> schema
    schema >> analyzer
    analyzer >> hmm_model
    hmm_model >> corpus
    corpus >> synonym_records
    synonym_records >> feature_selector
    feature_selector >> transliteration_model
    transliteration_model >> simple_fst
    simple_fst >> spark_mllib
    spark_mllib >> sql_db
    server << [sql_db, spark_mllib, lucene]