import os
import pandas as pd

xlsx_path = os.path.join(os.path.dirname(__file__), 'data', 'product_data.xlsx')

class ProductData():
    def __init__(self, xlsx_path):
        self.xlsx = pd.ExcelFile(xlsx_path)
        
        self._product_attribute_df = None
        self._product_attribute_dict = None

        self._product_attribute_value_df = None
        self._product_attribute_value_dict = None
        
        self._product_template_df = None
        self._product_template_dict = None

    
    def get_product_attributes(self):
        if not self._product_attribute_value_dict:
            self._product_attribute_df = self.xlsx.parse('product.attribute')
            self._product_attribute_dict = self._product_attribute_df.to_dict()
        
        return self._product_attribute_dict

    def get_product_attribute_values(self):
        if not self._product_attribute_value_dict:
            self._product_attribute_value_df = self.xlsx.parse('product.attribute.value')
            self._product_attribute_value_dict = self._product_attribute_value_df.to_dict()
        
        return self._product_attribute_value_dict
    
    def get_product_templates(self):
        if not self._product_template_dict:
            self._product_template_df = self.xlsx.parse('product.template')
            self._product_template_dict = self._product_template_df.to_dict()
        
        return self._product_template_dict