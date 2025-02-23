from langchain.document_loaders import TextLoader


file_path = "data/data_kt.txt"

loader = TextLoader(file_path, encoding="utf-8")
documents = loader.load()

if documents:
    print("\nNội dung tài liệu:\n")
    print(documents[0].page_content)
else:
    print("Không có tài liệu nào được load.")
