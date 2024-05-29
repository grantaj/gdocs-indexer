from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import re

# Authenticate and set up the Google Docs API client
def authenticate():
    SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
    creds = None
    if os.path.exists('credentials.json'):
        creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
    else:
        raise FileNotFoundError("Credentials file not found. Ensure you have 'credentials.json' in the working directory.")

    service = build('docs', 'v1', credentials=creds)
    return service

# Download Google Docs content as plain text and handle page breaks
def download_document(service, document_id):
    document = service.documents().get(documentId=document_id).execute()
    content = document.get('body').get('content')
    text = ''
    page_number = 0
    page_texts = {page_number: ''}
    
    for element in content:
        if 'paragraph' in element:
            for elem in element['paragraph']['elements']:
                if 'textRun' in elem:
                    page_texts[page_number] += elem['textRun']['content']
        if 'sectionBreak' in element:
            page_number += 1
            page_texts[page_number] = ''
                    
    return page_texts

# Save the document content to a text file (optional)
def save_to_text_file(content, file_path):
    with open(file_path, 'w') as file:
        file.write(content)

# Generate index from the text content
def generate_index(page_texts):
    word_index = {}
    for page_number, text in page_texts.items():
        words = re.findall(r'\b\w+\b', text.lower())
        for word in words:
            if word not in word_index:
                word_index[word] = []
            word_index[word].append(page_number)
    return word_index

# Main function to download document and generate index
def main():
    DOCUMENT_ID = '1pZk2z4xjii-3xlew51eDNVyjOEGQZtcBy5ulLdxyhnk'
    FILE_PATH = 'document.txt'

    service = authenticate()
    page_texts = download_document(service, DOCUMENT_ID)
    
    # Concatenate all pages' text for saving (optional)
    content = '\n'.join(page_texts.values())
    save_to_text_file(content, FILE_PATH)

    index = generate_index(page_texts)
    sorted_index = {k: sorted(set(v)) for k, v in sorted(index.items())}

    # Print the index
    for word, pages in sorted_index.items():
        print(f'{word}: {", ".join(map(str, pages))}')

if __name__ == '__main__':
    main()

