from basilica import Connection
import os
from dotenv import load_dotenv

load_dotenv()

BASILICA_API_KEY = os.getenv("BASILICA_API_KEY", default="OOPS")

connection = Connection(BASILICA_API_KEY)
print(type(connection))

sentences = [
    "This is a sentence!",
    "This is a similar sentence!",
    "I don't think this sentence is very similar at all...",
]
    
embeddings = list(connection.embed_sentences(sentences))
for embed in embeddings:
    print ("--------")
    print(embed) #> a list with 768 floats from -1 to 1

breakpoint()

embeddings = connection.embed_sentences("Hello, world!")
print(embedding)

#[[0.8556405305862427, ...], ...]