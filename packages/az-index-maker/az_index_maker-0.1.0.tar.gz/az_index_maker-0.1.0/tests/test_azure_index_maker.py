import unittest
import os
from unittest.mock import patch, MagicMock
from az_index_maker.az_index_maker import AzureIndexMaker, PDFProcessor, AzureFormRecognizer, EmbeddingGenerator, SearchIndexUploader

class TestAzureIndexMaker(unittest.TestCase):
    
    def setUp(self):
        self.folder_path = "sample_folder"
        self.column_mapping = {
            'id': 'id',
            'text_content': 'text_content',
            'table': 'table',
            'vectors': 'vectors',
            'document_name': 'document_name'
        }
        self.index_maker = AzureIndexMaker(self.folder_path, "fake_fr_key", "fake_fr_endpoint",
                                           "fake_openai_key", "fake_openai_endpoint", "fake_deployment_name",
                                           "fake_search_key", "fake_search_endpoint", "fake_index_name", self.column_mapping)

    @patch('os.path.isdir')
    def test_init_folder_not_exist(self, mock_isdir):
        mock_isdir.return_value = False
        with self.assertRaises(FileNotFoundError):
            AzureIndexMaker("nonexistent_folder", "fake_fr_key", "fake_fr_endpoint",
                            "fake_openai_key", "fake_openai_endpoint", "fake_deployment_name",
                            "fake_search_key", "fake_search_endpoint", "fake_index_name", self.column_mapping)

    @patch('os.listdir')
    @patch('os.path.isfile')
    def test_process_folder(self, mock_isfile, mock_listdir):
        mock_listdir.return_value = ['file1.pdf', 'file2.pdf']
        mock_isfile.return_value = True
        with patch.object(self.index_maker, 'process_pdf', return_value=None) as mock_process_pdf:
            self.index_maker.process_folder()
            self.assertEqual(mock_process_pdf.call_count, 2)

    @patch.object(PDFProcessor, 'divide_pdf', return_value=None)
    @patch.object(AzureFormRecognizer, 'extract_data', return_value=("Sample text", "<table></table>"))
    @patch.object(EmbeddingGenerator, 'generate_embedding', return_value=[0.1, 0.2, 0.3])
    @patch.object(SearchIndexUploader, 'upload_to_index', return_value=None)
    def test_process_pdf(self, mock_upload, mock_embed, mock_extract, mock_divide):
        mock_pdf_processor = MagicMock()
        mock_pdf_processor.pages = ["Page 1", "Page 2"]
        with patch('az_index_maker.az_index_maker.PDFProcessor', return_value=mock_pdf_processor):
            self.index_maker.process_pdf("sample.pdf")
            self.assertEqual(self.index_maker.dataframe.shape[0], 2)  # Two pages processed
            self.assertTrue(mock_upload.called)

    def test_pdf_processor_init_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            PDFProcessor("nonexistent_file.pdf")

    def test_pdf_processor_non_pdf_file(self):
        with self.assertRaises(ValueError):
            PDFProcessor("not_a_pdf.txt")

    def test_column_mapping(self):
        self.assertIn('id', self.index_maker.column_mapping)
        self.assertIn('text_content', self.index_maker.column_mapping)

if __name__ == '__main__':
    unittest.main()

#---------------------------------old simple test------------------
# import unittest
# from az_index_maker.az_index_maker import AzureIndexMaker

# class TestAzureIndexMaker(unittest.TestCase):
#     def test_init(self):
        
#         index_maker = AzureIndexMaker("sample.pdf", "fake_fr_key", "fake_fr_endpoint",
#                                       "fake_openai_key", "fake_openai_endpoint", "fake_deployment_name",
#                                       "fake_search_key", "fake_search_endpoint", "fake_index_name")
#         self.assertIsNotNone(index_maker)

# if __name__ == '__main__':
#     unittest.main()
