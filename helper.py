import pandas as pd
import ast
import re
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium


@st.cache_data


# Loads and encodes statscan data
@st.cache_data
def load_data():
    df = pd.read_csv('data/2024-07-CSV/pub0724.csv')
    encoder = MappingEncoder()
    df = encoder.transform(df)
    return df

# Converts string(dictionary) into dictionary
def convert_to_dict(dict_string):
    # Add curly braces to make it a valid Python dictionary syntax
    dict_string = '{' + dict_string + '}'
    dict_string = re.sub(r"(?<=\w)'(?=\w)", r"\'", dict_string)
    return ast.literal_eval(dict_string)

# Loads string mapping for statcan numerical codes
@st.cache_data
def load_mapper():
    mapper = pd.read_excel('data/2024-07-CSV/column_map.xlsx')
    mapper['Column mappings'] = mapper['Column mappings'].apply(convert_to_dict)
    map_dict = {}
    for i in mapper['Column mappings']:
        map_dict.update(i)
    return map_dict

# Encodes mapping for statcan numerical codes
class MappingEncoder:
    def __init__(self, mapping_dict=None):
        """
        Initialize with a dictionary of mappings for each column.

        Parameters:
        mappings (dict): A dictionary where keys are column names and values are dictionaries
                         that map numeric values to string codes.
        """
        if mapping_dict is None:
            self.mappings = load_mapper()
        else:
            self.mappings  = mapping_dict
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
@st.cache_data
def geo_data():
    prov_data = gpd.read_file("data/georef-canada-province@public.geojson")
    prov_dict = {'Québec': 'Quebec',
                 'Île-du-Prince-Édouard': 'Prince Edward Island',
                 'Nouveau-Brunswick': 'New Brunswick',
                 'Terre-Neuve-et-Labrador': 'Newfoundland and Labrador',
                 'Colombie-Britannique': 'British Columbia',
                 'Nouvelle-Écosse': 'Nova Scotia'}

    for key in prov_dict.keys():
        prov_data['prov_name_fr'] = prov_data['prov_name_fr'].replace(key, prov_dict[key])
    return prov_data


def fmap(df = None, width = 725):
    if df is None:
        df = load_data()
    else:
        df = df

    province_count = df['PROV'].value_counts().reset_index()
    prov_data = geo_data()
    df_geocode = province_count.merge(prov_data, left_on = 'PROV',
                                      right_on = 'prov_name_fr', how = 'left')
    df_geocode = gpd.GeoDataFrame(df_geocode)
    m = folium.Map(location=[50, -90], zoom_start=3)

    choropleth = folium.Choropleth(
        geo_data=df_geocode,
        data=df_geocode,
        name="choropleth",
        columns=["PROV", "count"],
        key_on="feature.properties.PROV",
        fill_color="YlGn",
        fill_opacity=0.5,
        line_opacity=.1,
        highlight=True,
        legend_name="Sample count",
    ).add_to(m)

    folium.LayerControl().add_to(m)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['PROV', 'count'],
                                       aliases=['Province: ', "Count: "],
                                       labels=True,
                                       localize=True,
                                       sticky=False,
                                       style="""
                                       background-color: #F0EFEF;
                                       border: 2px solid black;
                                       border-radius: 3px;
                                       box-shadow: 3px;
                                       """, )
    )
    return st_folium(m, width = width)

