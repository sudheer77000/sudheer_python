from langchain_text_splitters import CharacterTextSplitter

text = """
Sentence1 one is here.
Sentence2.
Sentence3 three is here.
Sentence4 four is here.
"""

#text = "Sudheer Ishitha Navya Vijaya Prasad NagaRatnam Srinu Hari"

splitter = CharacterTextSplitter(
    separator=".",
    chunk_size=50,
    chunk_overlap=10
)

chunks = splitter.split_text(text)

for i,chunk in enumerate(chunks):
    print(f"\nChunk {i+1}")
    print(chunk)