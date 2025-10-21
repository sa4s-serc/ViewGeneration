from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.programming.framework import Vue, React
from diagrams.onprem.client import Client
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Mongodb

with Diagram("Today Real Estate Front-End Architecture", show=False):
    client = Client("User")

    with Cluster("Vue.js Application"):
        vue_app = Vue("Vue.js App")
        vue_router = Custom("Vue Router", "./icons/vue-router.png")
        vuex = Custom("Vuex", "./icons/vuex.png")
        axios = Custom("Axios", "./icons/axios.png")

        client >> vue_app
        vue_app >> vue_router
        vue_app >> vuex
        vue_app >> axios

    with Cluster("Backend Services"):
        server = Server("Backend Server")
        api = Custom("Axios API", "./icons/axios.png")
        db = Mongodb("Database")

        vue_app >> server
        server >> api
        api >> db

    with Cluster("External Services"):
        kakao_maps = Custom("Kakao Maps", "./icons/kakao-maps.png")
        news_api = Custom("News API", "./icons/news-api.png")

        vue_app >> kakao_maps
        vue_app >> news_api

    nginx = Nginx("Nginx")
    client >> nginx
    nginx >> vue_app