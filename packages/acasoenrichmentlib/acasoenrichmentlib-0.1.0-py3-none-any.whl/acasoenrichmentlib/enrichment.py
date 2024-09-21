import pandas as pd
from classes.googlesearch import GoogleSearchAPI
from classes.proxycurl import LinkedInDataProcessor
from classes.openai import OpenAIService
from lib.functions import validate_emails

class DataFrameProcessor:
    def __init__(self, google_search_api: GoogleSearchAPI, linkedin_data_processor: LinkedInDataProcessor):
        self.google_search_api = google_search_api
        self.linkedin_data_processor = linkedin_data_processor

    def process_emails(self, df: pd.DataFrame, email_col: str) -> pd.DataFrame:
        if email_col not in df.columns:
            raise ValueError(f"DataFrame must contain an '{email_col}' column")

        df = validate_emails(df, email_col)

        def fetch_and_enrich_data(row):
            if not row['is_valid_email']:
                return row

            email = row[email_col]
            linkedin_url = row.get('linkedin_url') if 'linkedin_url' in row and row['linkedin_url'] else self.google_search_api.search_linkedin_by_email(email)
            if linkedin_url:
                linkedin_data = self.linkedin_data_processor.get_linkedin_data_from_url(linkedin_url)
                if linkedin_data:
                    enriched_data = self.linkedin_data_processor.enrich_linkedin_data(linkedin_data)
                    row.update(enriched_data)
            return row

        df = df.apply(fetch_and_enrich_data, axis=1)
        return df

# Example usage:
# google_search_api = GoogleSearchAPI(cse_id="your_cse_id", api_key="your_api_key")
# open_ai_service = OpenAIService()
# linkedin_data_processor = LinkedInDataProcessor(open_ai_client=open_ai_service)
# df_processor = DataFrameProcessor(google_search_api, linkedin_data_processor)
# df = pd.DataFrame({'email': ['example@example.com']})
# processed_df = df_processor.process_emails(df)
# print(processed_df)
