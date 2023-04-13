from IPython.display import display, HTML
from elasticsearch import Elasticsearch
from txtai.pipeline import Similarity
import streamlit as st

# Connect to ES instance
es = Elasticsearch(hosts=["http://localhost:9200"], request_timeout=60, retry_on_timeout=True)

# Create similarity instance for re-ranking
similarity = Similarity("valhalla/distilbart-mnli-12-3")

def search(search_term, limit):
  body = {
    "id": "semantic_search_test",
    "params": {
        "size": limit,
        "sort": {
        "values": [
            {
            "_score": "desc"
            },
            {
            "asset_uuid": "desc"
            }
        ]
        },
        "query_string": search_term
    }
}
  
  results = []
  for result in es.search_template(index="movies", body=body)["hits"]["hits"]:
    source = result["_source"]
    text = source["title"] + "\n" + source["description"]
    results.append({"score":result["_score"], "doc":{"title": source["title"], "description": source["description"]}})
  return results

def ranksearch(query, limit):
  es_results = search(query, limit * 10)
  text = []
  for result in es_results:
    text.append(result["doc"]["title"] + "\n" + result["doc"]["description"])
  return [(score, text[x]) for x, score in similarity(query, text)][:limit]

def main():
    st.title("Semantic Movie Search")
    # User search   
    user_input = st.text_area("Search box", "toys come alive")
    limit = 50
    es_results = search(user_input, limit)
    txtai_results = ranksearch(user_input, limit)

    col1, col2, = st.columns(2)
    with col1:
       st.header("Elasticsearch Results")
       for result in es_results:
        st.write(result["score"])
        st.text(result["doc"]["title"])
        st.write(result["doc"]["description"])
    with col2:
       st.header("txtai")
       for score, text in txtai_results:
          st.write(score)
          txtArr = text.split("\n")
          st.text(txtArr[0])
          st.write(txtArr[1])

if __name__ == "__main__":
   main()
