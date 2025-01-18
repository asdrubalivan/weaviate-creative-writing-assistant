from models import Idea, IdeaList
import json


def load_ideas() -> IdeaList:
    with open('src/creative_ideas.json', 'r') as file:
        data = json.load(file)
        ideas = data.get('creative_writing_ideas', [])
        return [Idea(**idea) for idea in ideas]

