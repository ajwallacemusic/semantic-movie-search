# semantic-movie-search
Semantic Movie Search is a simple python app powered by Elasticsearch and txtai. 

It takes in a user input, gets the top 50 Elasticsearch results, then runs a txtai semantic similarity function on the top 500 Elasticsearch results, reranks them, and returns the new top 50 to compare.

----

[![Semantic Movie Search Demo](https://user-images.githubusercontent.com/24554274/231806338-1bd7d1f4-d8bd-4da5-9775-98508a1df94f.gif)]([https://user-images.githubusercontent.com/24554274/231801642-79ab1fa5-a444-4977-8f58-572aa70e25ad.mp4](https://user-images.githubusercontent.com/24554274/231801642-79ab1fa5-a444-4977-8f58-572aa70e25ad.mp4))

----

## Setup/Installation
You need Python installed, and a few dependencies, specifically [Streamlit](https://docs.streamlit.io/) (for running the app), Elasticsearch, and [txtai](https://github.com/neuml/txtai).

This project assumes you have a local Elasticsearch cluster running on port 9200. You can run a local cluster and setup a movies index via docker-compose from the [simple-reranker project repo](https://github.com/ajwallacemusic/simple-reranker).

## Improvements
The searching and reranking is not fast. That's because a similarity function is ran against each Elasticsearch result (essentially converting text to vector embeddings on the fly.) This works well for a proof of concept, but ideally, you would convert the data to vectors and add to a new Elasticsearch index, or vector database.

