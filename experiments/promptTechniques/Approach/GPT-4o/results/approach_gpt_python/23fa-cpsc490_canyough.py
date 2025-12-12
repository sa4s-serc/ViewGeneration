from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.aws.general import User

with Diagram("Twitter Recommendation System Architecture", direction="LR", outformat="png"):
    
    user = User("User")
    
    with Cluster("Microservices"):
        product_mixer = Custom("Product Mixer", "./icons/service.png")
        cr_mixer = Custom("CR Mixer", "./icons/service.png")
        frs = Custom("Follow Recommendations Service", "./icons/service.png")
        home_mixer = Custom("Home Mixer", "./icons/service.png")
    
    with Cluster("Data Sources"):
        uss = Custom("User Signal Service", "./icons/database.png")
        real_graph = Custom("Real Graph", "./icons/database.png")
        earlybird = Custom("Earlybird", "./icons/database.png")
        tweetypie = Custom("TweetyPie", "./icons/database.png")
        manhattan = Custom("Manhattan", "./icons/database.png")
        memcached = Custom("Memcached", "./icons/database.png")
        strato = Custom("Strato", "./icons/database.png")
    
    with Cluster("Components"):
        with Cluster("Candidate Sources"):
            sim_clusters = Custom("SimClustersANN", "./icons/component.png")
            user_tweet_graph = Custom("UserTweetGraph", "./icons/component.png")
            earlybird_candidate = Custom("EarlybirdCandidateSource", "./icons/component.png")
        
        with Cluster("Feature Hydrators"):
            tweetypie_feature = Custom("TweetypieFeatureHydrator", "./icons/component.png")
            in_network_feature = Custom("InNetworkFeatureHydrator", "./icons/component.png")
            gizmoduck_user = Custom("GizmoduckUserQueryFeatureHydrator", "./icons/component.png")
        
        with Cluster("Filters"):
            urt_filter = Custom("UrtUnorderedExcludeIdsCursorFilter", "./icons/component.png")
            excluded_ids = Custom("ExcludedIdsFilter", "./icons/component.png")
            tweet_lang = Custom("TweetLanguageFilter", "./icons/component.png")
        
        with Cluster("Scorers & Transformers"):
            scorers = Custom("Scorers", "./icons/component.png")
            transformers = Custom("Transformers", "./icons/component.png")
        
        with Cluster("Gates & Cursors"):
            gates = Custom("Gates", "./icons/component.png")
            cursors = Custom("Cursors", "./icons/component.png")
    
    user >> Edge(label="Requests") >> product_mixer
    product_mixer >> Edge(label="gRPC/Thrift") >> cr_mixer
    cr_mixer >> Edge(label="Recommendation Data") >> frs
    frs >> Edge(label="Account Suggestions") >> home_mixer
    home_mixer >> Edge(label="Home Timeline") >> user
    
    product_mixer >> Edge(label="Data Access") >> uss
    product_mixer >> Edge(label="Data Access") >> real_graph
    product_mixer >> Edge(label="Data Access") >> earlybird
    product_mixer >> Edge(label="Data Access") >> tweetypie
    product_mixer >> Edge(label="Data Access") >> manhattan
    product_mixer >> Edge(label="Data Access") >> memcached
    product_mixer >> Edge(label="Data Access") >> strato
    
    product_mixer >> Edge(label="Uses") >> sim_clusters
    product_mixer >> Edge(label="Uses") >> user_tweet_graph
    product_mixer >> Edge(label="Uses") >> earlybird_candidate
    
    product_mixer >> Edge(label="Uses") >> tweetypie_feature
    product_mixer >> Edge(label="Uses") >> in_network_feature
    product_mixer >> Edge(label="Uses") >> gizmoduck_user
    
    product_mixer >> Edge(label="Uses") >> urt_filter
    product_mixer >> Edge(label="Uses") >> excluded_ids
    product_mixer >> Edge(label="Uses") >> tweet_lang
    
    product_mixer >> Edge(label="Uses") >> scorers
    product_mixer >> Edge(label="Uses") >> transformers
    
    product_mixer >> Edge(label="Uses") >> gates
    product_mixer >> Edge(label="Uses") >> cursors