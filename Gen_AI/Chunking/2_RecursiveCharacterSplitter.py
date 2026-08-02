from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
Su Gu.

Navya Gavarasana.

Is Gu.

Ha Ko.

Su Ka.
"""

#text = "Sudheer Ishitha Navya Vijaya Prasad NagaRatnam Srinu Hari"

splitter = RecursiveCharacterTextSplitter(
     separators=[
        "\n\n",
        "\n",
        ".",
        " ",
        ""
    ],
    chunk_size=10,
    chunk_overlap=5
)

chunks = splitter.split_text(text)

for i,chunk in enumerate(chunks):
    print(f"\nChunk {i+1}")
    print(chunk)