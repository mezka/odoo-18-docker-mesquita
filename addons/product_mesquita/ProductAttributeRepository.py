from typing import Union, List, Dict
import logging
from .get_module_name import get_module_name

_logger = logging.getLogger(__name__)

class ProductAttributeRepository:
    def __init__(self, env):
        self.env = env

    def load_product_attributes(self, product_attributes: List[Dict]):

        created_product_attributes = []

        try:
            for product_attribute in product_attributes:
                product_attribute_without_ext_id = {key: product_attribute[key] for key in product_attribute if key != 'id'}
                created_product_attribute = self.env['product.attribute'].create(product_attribute_without_ext_id)
                self.env['ir.model.data'].create({
                    'name': product_attribute['id'],
                    'model': 'product.attribute',
                    'res_id': created_product_attribute.id,
                    'module': get_module_name()
                })
                created_product_attributes.append(created_product_attribute)
        except Exception as e:
            _logger.exception("Error during load_product_attributes")
            raise e
        return created_product_attributes
    
    def delete_all_product_attributes(self):
        try:
            product_attributes_to_delete = self.env['product.attribute'].search([])

            for attribute in product_attributes_to_delete:
                external_ids = self.env['ir.model.data'].search([
                    ('model', '=', 'product.attribute'),
                    ('res_id', '=', attribute.id),
                    ('module', '=', get_module_name())
                ])
                external_ids.unlink()

            deleted_product_attributes = product_attributes_to_delete.unlink()
        except Exception as e:
            _logger.exception("Error while running delete_all_product_attributes")
            raise e
        return deleted_product_attributes

    def load_product_attribute_values(self, product_attribute_values: List[Dict]):

        created_product_attribute_values = []

        try:
            for product_attribute_value in product_attribute_values:
                
                product_attribute = self.env.ref(f'{get_module_name()}.{product_attribute_value["attribute_id"]}')
                product_attribute_value['attribute_id'] = product_attribute.id
                
                product_attribute_value_without_ext_ids = {key: product_attribute_value[key] for key in product_attribute_value if key != 'id'}

                created_product_attribute_value = self.env['product.attribute.value'].create(product_attribute_value_without_ext_ids)

                self.env['ir.model.data'].create({
                        'name': product_attribute_value['id'],
                        'model': 'product.attribute.value',
                        'res_id': created_product_attribute_value.id,
                        'module': get_module_name()
                    })
                
                created_product_attribute_values.append(created_product_attribute_value)
        except Exception as e:
            _logger.exception("Error during load_product_attribute_values")
            raise e

        return created_product_attribute_values
    
    def delete_all_product_attribute_values(self):
        try:
            product_attribute_values_to_delete = self.env['product.attribute.value'].search([])

            for attribute in product_attribute_values_to_delete:
                external_ids = self.env['ir.model.data'].search([
                    ('model', '=', 'product.attribute.value'),
                    ('res_id', '=', attribute.id),
                    ('module', '=', get_module_name())
                ])
                external_ids.unlink()

            deleted_product_attributes = product_attribute_values_to_delete.unlink()
        except Exception as e:
            _logger.exception("Error while running delete_all_product_attribute_values")
            raise e
        return deleted_product_attributes
