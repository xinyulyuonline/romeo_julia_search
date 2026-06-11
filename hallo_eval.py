import asyncio
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

async def create_eval():
    response = await asyncio.to_thread(
        requests.post,
        os.getenv("AZURE_AI_PROJECT_ENDPOINT") + "/evals",
        headers={
            'api-key': os.getenv("AZURE_OEPNAI_KEY"),
        },
        json={
            'name': 'My Evaluation',
            'data_source_config': {
                'type': 'custom',
                'item_schema': {
                'type': 'object',
                'properties': {
                    'question': {
                    'type': 'string'
                    },
                    'subject': {
                    'type': 'string'
                    },
                    'A': {
                    'type': 'string'
                    },
                    'B': {
                    'type': 'string'
                    },
                    'C': {
                    'type': 'string'
                    },
                    'D': {
                    'type': 'string'
                    },
                    'answer': {
                    'type': 'string'
                    },
                    'completion': {
                    'type': 'string'
                    }
                }
                }
            },
            'testing_criteria': [
                {
                'type': 'string_check',
                'reference': '{{item.completion}}',
                'input': '{{item.answer}}',
                'operation': 'eq',
                'name': 'string check'
                }
            ]
        })

    print(response.status_code)
    print(json.dumps(response.json(), indent=2))
