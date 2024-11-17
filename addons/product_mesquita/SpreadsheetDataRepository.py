import os
import pandas as pd

class SpreadsheetDataRepository():
    def __init__(self, xlsx_path):
        self.xlsx = pd.ExcelFile(xlsx_path)
        
        self._product_template_df = self.xlsx.parse('product.template')
        
        self._product_attribute_df = self.xlsx.parse('product.attribute')
        self._product_attribute_value_df = self.xlsx.parse('product.attribute.value')
        self._product_attribute_value_df = self._product_attribute_value_df.rename(columns={'attribute_id/id': 'attribute_id'})

        self._product_template_attribute_lines_df = self.xlsx.parse('product.template.attribute.line')
        self._product_template_attribute_lines_df['value_ids/id'] = self._product_template_attribute_lines_df['value_ids/id'].str.split(',')

    
    def get_product_attributes(self):
        return self._product_attribute_df.to_dict(orient='records')

    def get_product_attribute_values(self):
        return self._product_attribute_value_df.to_dict(orient='records')
    
    def get_product_templates(self):
        return self._product_template_df.to_dict(orient='records')

    def get_product_template_attribute_lines(self):
        return self._product_template_attribute_lines_df.to_dict('records')
