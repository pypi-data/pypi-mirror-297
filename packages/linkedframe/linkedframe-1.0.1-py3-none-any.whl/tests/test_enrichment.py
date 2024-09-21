import pandas as pd
from unittest.mock import Mock, patch
from linkedframe.enrichment import DataFrameProcessor
from lib.functions import validate_emails

def test_validate_emails():
    df = pd.DataFrame({'email': ['example@example.com', 'invalid-email', 'user@domain.co']})
    df = validate_emails(df, 'email')
    assert df['is_valid_email'].tolist() == [True, False, True]

@patch('linkedframe.enrichment.GoogleSearchAPI')
@patch('linkedframe.enrichment.LinkedInDataProcessor')
@patch('linkedframe.enrichment.OpenAIService')
def test_process_emails(MockGoogleSearchAPI, MockLinkedInDataProcessor, MockOpenAIService):
    df = pd.DataFrame({'email': ['example@example.com']})
    mock_google_search_api = MockGoogleSearchAPI.return_value
    mock_linkedin_data_processor = MockLinkedInDataProcessor.return_value
    mock_openai_service = MockOpenAIService.return_value

    mock_google_search_api.search_linkedin_by_email.return_value = 'https://linkedin.com/in/example'
    mock_linkedin_data_processor.get_linkedin_data_from_url.return_value = {'name': 'Example Name'}
    mock_linkedin_data_processor.enrich_linkedin_data.return_value = {'linkedin_url': 'https://linkedin.com/in/example', 'education_level': 'Bacharelado'}
    mock_linkedin_data_processor.process_linkedin_data.return_value = pd.DataFrame([{
        'email': 'example@example.com',
        'is_valid_email': True,
        'education_level': 'Bacharelado'
    }])

    df_processor = DataFrameProcessor(cse_id="new_cse_id", google_console_api_key="new_google_key", openai_key="new_openai_key", proxycurl_api_key="new_proxycurl_key")
    df_processor.google_search_api = mock_google_search_api
    df_processor.linkedin_data_processor = mock_linkedin_data_processor
    df_processor.open_ai_service = mock_openai_service

    df = df_processor.process_emails(df, 'email')
    assert 'is_valid_email' in df.columns
    assert df.loc[0, 'education_level'] == 'Bacharelado'
