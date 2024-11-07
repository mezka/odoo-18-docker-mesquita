import os
import pandas as pd

class SpreadsheetDataRepository():
    def __init__(self, xlsx_path):
        self.xlsx = pd.ExcelFile(xlsx_path)
        
        self._product_template_df = self.xlsx.parse('product.template')
        self._product_attribute_df = self.xlsx.parse('product.attribute')
        self._product_attribute_value_df = self.xlsx.parse('product.attribute.value')
    
    def get_product_attributes(self):
        return self._product_attribute_df.to_dict(orient='records')
    
    def get_product_attribute_names(self):
        return self._product_attribute_df['name'].to_list()

    def get_product_attribute_ids(self):
        return self._product_attribute_df['id'].to_list()

    def get_product_attribute_values(self):
        return self._product_attribute_value_df.to_dict(orient='records')
    
    def get_product_attribute_value_ids(self):
        return self._product_attribute_value_df['id'].to_list()
    
    def get_product_templates(self):
        return self._product_template_df.to_dict()