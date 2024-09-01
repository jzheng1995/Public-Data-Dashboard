import pandas as pd


class MappingEncoder:
    def __init__(self):
        """
        Initialize with a dictionary of mappings for each column.

        Parameters:
        mappings (dict): A dictionary where keys are column names and values are dictionaries
                         that map numeric values to string codes.
        """
        self.mappings  = {
    'SURVMNTH': {1:'January', 2:'February', 3:'March', 4:'April',
                 5:'May',6:'June',7:'July', 8:'August', 9:'September',
                 10:'October', 11:'November', 12:'December'}
}

    def fit(self, df):
        """
        Fit the encoder by setting up the mappings for each column.

        Parameters:
        df (pd.DataFrame): The DataFrame to fit on (not used in this example, but included for consistency).
        """
        pass  # In this example, no fitting is required as mappings are provided directly

    def transform(self, df):
        """
        Transform the DataFrame by replacing numeric values with string codes.

        Parameters:
        df (pd.DataFrame): The DataFrame to transform.

        Returns:
        pd.DataFrame: The transformed DataFrame with string codes.
        """
        df_transformed = df.copy()
        for column, mapping in self.mappings.items():
            if column in df_transformed.columns:
                df_transformed[column] = df_transformed[column].map(mapping)
        return df_transformed

    def fit_transform(self, df):
        """
        Fit and transform the DataFrame.

        Parameters:
        df (pd.DataFrame): The DataFrame to fit and transform.

        Returns:
        pd.DataFrame: The transformed DataFrame with string codes.
        """
        self.fit(df)
        return self.transform(df)