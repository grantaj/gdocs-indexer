from googleapiclient.discovery import build
from google.oauth2 import service_account
import re

# Step 1: Authenticate and set up the API client
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'
DOCUMENT_ID = '1pZk2z4xjii-3xlew51eDNVyjOEGQZtcBy5ulLdxyhnk'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('docs', 'v1', credentials=credentials)

# Step 2: Retrieve document content
def retrieve_document_content(doc_id):
    document = service.documents().get(documentId=doc_id).execute()
    return document

# Step 3: Process content to generate an index
def generate_index(content):
    word_index = {}
    current_page = 1
    for element in content['body']['content']:
        if 'paragraph' in element:
            for elem in element['paragraph']['elements']:
                if 'textRun' in elem:
                    text = elem['textRun']['content']
                    words = re.findall(r'\b\w+\b', text.lower())
                    for word in words:
                        if word not in word_index:
                            word_index[word] = set()
                        word_index[word].add(current_page)
        elif 'sectionBreak' in element:
            current_page += 1
    return word_index

# Step 4: Main function to put everything together
def main():
    document = retrieve_document_content(DOCUMENT_ID)
    content = document
    index = generate_index(content)
    sorted_index = {k: sorted(v) for k, v in sorted(index.items())}

    # Print or save the index
    for word, pages in sorted_index.items():
        print(f'{word}: {", ".join(map(str, pages))}')

if __name__ == '__main__':
    main()
