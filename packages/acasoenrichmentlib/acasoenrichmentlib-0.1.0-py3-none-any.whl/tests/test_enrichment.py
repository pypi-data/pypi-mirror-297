from acasoenrichmentlib.enrichment import DataFrameProcessor
import pandas as pd
from lib.functions import validate_emails
from unittest.mock import Mock

def test_validate_emails():
    df = pd.DataFrame({'email': ['example@example.com', 'invalid-email', 'user@domain.co']})
    df = validate_emails(df, 'email')
    assert df['is_valid_email'].tolist() == [True, False, True]

def test_fetch_and_enrich_data():
    df = pd.DataFrame({'email': ['example@example.com']})
    google_search_api = Mock()
    linkedin_data_processor = Mock()
    google_search_api.search_linkedin_by_email.return_value = 'https://linkedin.com/in/example'
    linkedin_data_processor.get_linkedin_data_from_url.return_value = {'linkedin_url': 'https://linkedin.com/in/example'}

    df_processor = DataFrameProcessor(google_search_api, linkedin_data_processor)
    df = df_processor.process_emails(df, 'email')

    assert 'is_valid_email' in df.columns
    assert df.loc[0, 'is_valid_email'] == True