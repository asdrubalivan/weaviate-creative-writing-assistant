from models import Idea, IdeaList
import json
from settings import settings
import weaviate
import weaviate.auth

def load_ideas() -> IdeaList:
    with open('src/creative_ideas.json', 'r') as file:
        data = json.load(file)
        ideas = data.get('creative_writing_ideas', [])
        return [Idea(**idea) for idea in ideas]

def save_ideas_to_weaviate():
    # Connect to Weaviate using settings
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=settings.weaviate_endpoint.unicode_string(),
        auth_credentials=weaviate.auth.AuthApiKey(api_key=settings.weaviate_api_key),
        headers={'X-OpenAI-Api-key': settings.openai_api_key}
    )

    # Load ideas
    ideas = load_ideas()

    # Iterate over each idea and insert into Weaviate
    for idea in ideas:
        client.data_object.create(
            data_object={
                "idea": idea.idea,
                "tags": idea.tags,
                "inspiration": idea.inspiration
            },
            class_name="CreativeIdea"
        )
    client.close()
    print("All ideas have been saved to Weaviate.")

# Call the function to save ideas
save_ideas_to_weaviate()

