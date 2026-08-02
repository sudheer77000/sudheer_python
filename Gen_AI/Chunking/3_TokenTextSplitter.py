from langchain_text_splitters import TokenTextSplitter

text = "He is good boy"

#text = "Sudheer Ishitha Navya Vijaya Prasad NagaRatnam Srinu Hari"

splitter = TokenTextSplitter(
    chunk_size=4,
    chunk_overlap=2
)

chunks = splitter.split_text(text)

for i,chunk in enumerate(chunks):
    print(f"\nChunk {i+1}")
    print(chunk)