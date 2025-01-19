import typer
from models import Idea, IdeaList
import json
from settings import settings
import weaviate
import weaviate.auth
import weaviate.classes.config as wvcc

app = typer.Typer()

def load_ideas() -> IdeaList:
    with open('src/creative_ideas.json', 'r') as file:
        data = json.load(file)
        ideas = data.get('creative_writing_ideas', [])
        return [Idea(**idea) for idea in ideas]

@app.command()
def save_ideas_to_weaviate():
    """
    Save creative writing ideas to a Weaviate instance.

    This command connects to a Weaviate instance using the provided settings,
    checks if the 'CreativeIdea' class exists, and creates it if not. It then
    loads ideas from a JSON file and inserts them into the Weaviate collection.
    """
    # Connect to Weaviate using settings
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=settings.weaviate_endpoint.unicode_string(),
        auth_credentials=weaviate.auth.AuthApiKey(api_key=settings.weaviate_api_key),
        headers={'X-Cohere-Api-Key': settings.cohere_api_key},
    )

    # Define the class schema for CreativeIdea
    collection_name = "CreativeIdea"
    vectorizer_config = wvcc.Configure.Vectorizer.text2vec_cohere()
    generative_config = wvcc.Configure.Generative.cohere()
    properties = [
        wvcc.Property(name="idea", data_type=wvcc.DataType.TEXT),
        wvcc.Property(name="tags", data_type=wvcc.DataType.TEXT_ARRAY),
        wvcc.Property(name="inspiration", data_type=wvcc.DataType.TEXT)
    ]

    # Check if the class already exists
    if not client.collections.exists(name=collection_name):
        client.collections.create(
            name=collection_name,
            vectorizer_config=vectorizer_config,
            generative_config=generative_config,
            properties=properties
        )

    # Load ideas
    ideas = load_ideas()

    collection = client.collections.get(collection_name)

    # Iterate over each idea and insert into Weaviate
    for idea in ideas:
        collection.data.insert(
            properties={
                "idea": idea.idea,
                "tags": idea.tags,
                "inspiration": idea.inspiration
            }
        )
    client.close()
    print("All ideas have been saved to Weaviate.")

if __name__ == "__main__":
    app()
