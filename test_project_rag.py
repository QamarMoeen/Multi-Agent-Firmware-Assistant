
from firmware_assistant.project_rag import search_projects

questions = [
    "Which project involved environmental monitoring?",
    "Have I built anything using programmable logic?",
    "Which project used a microcontroller with sensors?",
]

for question in questions:
    print(f"\nQuestion: {question}")
    print(search_projects(question))
    print("-" * 50)