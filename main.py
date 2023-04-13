from IPython.display import display, HTML
from elasticsearch import Elasticsearch
from txtai.pipeline import Similarity
import streamlit as st

# Create similarity instance for re-ranking
similarity = Similarity("valhalla/distilbart-mnli-12-3", crossencode=True)

def ranksearch(query, limit):
  results = [text for _, text in search(query, limit * 10)]
  return [(score, results[x]) for x, score in similarity(query, results)][:limit]

# Connect to ES instance
es = Elasticsearch(hosts=["<url>"], request_timeout=60, retry_on_timeout=True)

def table(category, query, rows):
    st.write(category, query)

    for score, text in rows:
        st.write(score, text)



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
  for result in es.search_template(index="assets", body=body)["hits"]["hits"]:
    source = result["_source"]
    text = source["name"] + "\n" + source["description"]
    results.append((result["_score"], text))
  return results


def main():
    st.title("Semantic Search")
    # User search   
    user_input = st.text_area("Search box", "toys come alive")
    limit = 50


    table("Elasticsearch", user_input, search(user_input, limit))
    table("Elasticsearch + txtai", user_input, ranksearch(user_input, limit))

if __name__ == "__main__":
   main()
