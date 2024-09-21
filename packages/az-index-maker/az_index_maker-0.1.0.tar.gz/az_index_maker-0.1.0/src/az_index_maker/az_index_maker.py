import os
import pandas as pd
import PyPDF2
import openai
import logging
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.search.documents import SearchClient
from azure.core.exceptions import HttpResponseError, ClientAuthenticationError


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PDFProcessor:
    def __init__(self, pdf_path):
        """
        Initializes the PDFProcessor class to handle PDF file processing.

        Parameters:
            pdf_path (str): The path to the PDF file to be processed.
        """
        if not os.path.isfile(pdf_path):
            raise FileNotFoundError(f"PDF file not found at {pdf_path}")
        
        if not pdf_path.endswith(".pdf"):
            raise ValueError("The file provided is not a PDF.")
        
        self.pdf_path = pdf_path
        self.pages = []

    def divide_pdf(self):
        """
        Splits the PDF into individual pages and extracts text from each page.
        
        This method reads the PDF and stores the extracted text of each page in the `self.pages` list.
        """
        try:
            pdf_reader = PyPDF2.PdfReader(self.pdf_path)
            num_pages = len(pdf_reader.pages)
            if num_pages == 0:
                raise ValueError(f"The PDF at {self.pdf_path} contains no pages.")
            
            for i in range(num_pages):
                page_text = pdf_reader.pages[i].extract_text()
                if page_text:
                    self.pages.append(page_text)
                else:
                    logging.warning(f"No text found on page {i+1} of {self.pdf_path}")
        except Exception as e:
            logging.error(f"Error while processing PDF: {e}")
            raise

class AzureFormRecognizer:
    def __init__(self, azure_fr_key, azure_fr_endpoint):
        """
        Initializes the AzureFormRecognizer class to handle form recognition using Azure Form Recognizer.

        Parameters:
            azure_fr_key (str): The Azure Form Recognizer API key.
            azure_fr_endpoint (str): The endpoint URL for the Azure Form Recognizer service.
        """
        if not azure_fr_key or not azure_fr_endpoint:
            raise ValueError("Azure Form Recognizer API key and endpoint must be provided.")

        try:
            self.client = DocumentAnalysisClient(endpoint=azure_fr_endpoint, credential=AzureKeyCredential(azure_fr_key))
        except ClientAuthenticationError as e:
            logging.error(f"Authentication error with Azure Form Recognizer: {e}")
            raise

    def extract_data(self, page_text):
        """
        Extracts text content and table data from a page using Azure Form Recognizer.

        Parameters:
             page_text (str): The text content of a PDF page to analyze.

         Returns:
             tuple: Contains text content and table data (as HTML) extracted from the page.
        """
        if not page_text:
            raise ValueError("Page text cannot be empty.")

        try:
            poller = self.client.begin_analyze_document("prebuilt-layout", document=page_text)
            result = poller.result()
        except HttpResponseError as e:
            logging.error(f"Error while analyzing document: {e}")
            raise
        
        text_content = ""
        tables = []
        try:
            for page in result.pages:
                text_content += page.content
                for table in page.tables:
                    table_data = [[cell.content for cell in row.cells] for row in table.rows]
                    df = pd.DataFrame(table_data)
                    tables.append(df.to_html())
        except Exception as e:
            logging.error(f"Error while extracting text or tables: {e}")
            raise
        
        return text_content, tables if tables else ""

class EmbeddingGenerator:
    def __init__(self, openai_key, openai_endpoint, deployment_name):
        """
        Initializes the EmbeddingGenerator class to generate embeddings using OpenAI's API.

        Parameters:
             openai_key (str): OpenAI API key for authentication.
             openai_endpoint (str): The endpoint URL for the OpenAI API.
             deployment_name (str): The deployment name for the embedding model to be used.
        """
        if not openai_key or not openai_endpoint:
            raise ValueError("OpenAI API key and endpoint must be provided.")
        
        openai.api_key = openai_key
        self.deployment_name = deployment_name

    def generate_embedding(self, text):
        """
        Generates embeddings (vectors) for the input text using OpenAI's API.

        Parameters:
             text (str): The input text for which the embedding needs to be generated.

        Returns:
             list: A list containing the embedding (vector) for the input text.
        """
        if not text:
            raise ValueError("Input text for embedding generation cannot be empty.")

        try:
            response = openai.Embedding.create(input=text, engine=self.deployment_name)
            return response['data'][0]['embedding']
        except openai.error.OpenAIError as e:
            logging.error(f"OpenAI API error: {e}")
            raise

class SearchIndexUploader:
    def __init__(self, search_key, search_endpoint, index_name):
        """
        Initializes the SearchIndexUploader class to upload documents to Azure Cognitive Search.

        Parameters:
             search_key (str): The API key for Azure Cognitive Search.
             search_endpoint (str): The endpoint URL for Azure Cognitive Search.
             index_name (str): The name of the search index where documents will be uploaded.
        """
        if not search_key or not search_endpoint:
            raise ValueError("Azure Cognitive Search API key and endpoint must be provided.")
        
        try:
            self.client = SearchClient(endpoint=search_endpoint, credential=AzureKeyCredential(search_key), index_name=index_name)
        except ClientAuthenticationError as e:
            logging.error(f"Authentication error with Azure Search: {e}")
            raise

    def upload_to_index(self, dataframe, column_mapping):
        """
        Uploads the dataframe to the Azure Cognitive Search index, allowing custom column mappings.

        Parameters:
             dataframe (pd.DataFrame): The dataframe containing the data to be uploaded.
             column_mapping (dict): A dictionary that maps user-provided column names to the expected fields in the index.
                                    Example:
                                    {
                                        'id': 'user_id_column',
                                        'text_content': 'user_text_column',
                                        'table': 'user_table_column',
                                        'vectors': 'user_vector_column',
                                        'document_name': 'user_doc_name_column'
                                    }
        
        """
        if dataframe.empty:
            raise ValueError("The dataframe is empty. Nothing to upload.")
        
        if not column_mapping or not isinstance(column_mapping, dict):
            raise ValueError("Column mapping must be a valid dictionary.")

        try:
            documents = []
            for index, row in dataframe.iterrows():
                document = {
                    'id': row[column_mapping['id']],
                    'text_content': row[column_mapping['text_content']],
                    'table': row[column_mapping['table']] if pd.notna(row[column_mapping['table']]) else "",
                    'document_name': row[column_mapping['document_name']],
                    'vectors': row[column_mapping['vectors']]  
                }
                documents.append(document)
            
            self.client.upload_documents(documents=documents)
        except Exception as e:
            logging.error(f"Error while uploading documents to Azure Search: {e}")
            raise

class AzureIndexMaker:
    def __init__(self, folder_path, azure_fr_key, azure_fr_endpoint, openai_key, openai_endpoint, deployment_name, search_key, search_endpoint, index_name, column_mapping):
        """
        Initializes the AzureIndexMaker class to process PDFs and upload content to an Azure Search index.

        Parameters:
            folder_path (str): The path to the folder containing PDF files to be processed.
            azure_fr_key (str): Azure Form Recognizer API key.
            azure_fr_endpoint (str): The endpoint URL for Azure Form Recognizer.
            openai_key (str): OpenAI API key.
            openai_endpoint (str): The endpoint URL for the OpenAI API.
            deployment_name (str): The name of the OpenAI embedding model to be used.
            search_key (str): Azure Cognitive Search API key.
            search_endpoint (str): The endpoint URL for Azure Cognitive Search.
            index_name (str): The name of the Azure search index where documents will be uploaded.
            column_mapping (dict): A dictionary to map user-defined column names to the expected fields.
        """
        if not os.path.isdir(folder_path):
            raise FileNotFoundError(f"The folder path {folder_path} does not exist.")

        self.folder_path = folder_path
        self.form_recognizer = AzureFormRecognizer(azure_fr_key, azure_fr_endpoint)
        self.embedding_generator = EmbeddingGenerator(openai_key, openai_endpoint, deployment_name)
        self.index_uploader = SearchIndexUploader(search_key, search_endpoint, index_name)
        self.column_mapping = column_mapping
        self.dataframe = pd.DataFrame(columns=[
            column_mapping.get('id', 'id'),
            column_mapping.get('text_content', 'text_content'),
            column_mapping.get('table', 'table'),
            column_mapping.get('vectors', 'vectors'),
            column_mapping.get('document_name', 'document_name')
        ])

    def process_folder(self):
        """
        Processes all PDF files in the specified folder.
        For each PDF in the folder, it processes the PDF and uploads the extracted content and embeddings to Azure Cognitive Search.
        """
        try:
            for filename in os.listdir(self.folder_path):
                if filename.endswith(".pdf"):
                    pdf_path = os.path.join(self.folder_path, filename)
                    self.process_pdf(pdf_path)
        except Exception as e:
            logging.error(f"Error while processing folder {self.folder_path}: {e}")
            raise

    def process_pdf(self, pdf_path):
        """
        Processes a single PDF file by extracting its pages, text content, and embeddings.

        Parameters:
             pdf_path (str): The path to the PDF file to be processed.
        
        This method:
        - Extracts text and table data from each page of the PDF.
        - Generates embeddings for the extracted text.
        - Appends the data to the class dataframe.
        - Uploads the extracted data and embeddings to Azure Cognitive Search.
        """
        try:
            pdf_processor = PDFProcessor(pdf_path)
            pdf_processor.divide_pdf()

            for i, page_text in enumerate(pdf_processor.pages):
                text_content, table = self.form_recognizer.extract_data(page_text)
                embedding = self.embedding_generator.generate_embedding(text_content)

                self.dataframe = self.dataframe.append({
                    self.column_mapping['id']: f"{os.path.basename(pdf_processor.pdf_path)}_{i+1}",
                    self.column_mapping['text_content']: text_content,
                    self.column_mapping['table']: table,
                    self.column_mapping['vectors']: embedding,
                    self.column_mapping['document_name']: f"{os.path.basename(pdf_processor.pdf_path)}_{i+1}"
                }, ignore_index=True)

            self.index_uploader.upload_to_index(self.dataframe, self.column_mapping)
        except Exception as e:
            logging.error(f"Error while processing PDF {pdf_path}: {e}")
            raise

