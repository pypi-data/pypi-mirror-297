import re
import pandas as pd

def validate_emails(df: pd.DataFrame, email_col: str) -> pd.DataFrame:
    """
    Validates the emails in the specified column of the DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the emails to validate.
        email_col (str): The name of the column containing the emails.
    
    Returns:
        pd.DataFrame: The DataFrame with an additional column 'is_valid_email' indicating the validity of each email.
    """
    if email_col not in df.columns:
        raise ValueError(f"DataFrame must contain an '{email_col}' column")
    
    email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    
    def is_valid_email(email):
        return bool(email_pattern.match(email))
    
    df['is_valid_email'] = df[email_col].apply(is_valid_email)
    return df
