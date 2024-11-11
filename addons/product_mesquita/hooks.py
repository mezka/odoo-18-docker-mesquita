import os
import logging
from .SpreadsheetDataRepository import SpreadsheetDataRepository
from .ProductAttributeRepository import ProductAttributeRepository
from .ProductTemplateRepository import ProductTemplateRepository
from .get_module_name import get_module_name

_logger = logging.getLogger(__name__)

xlsx_path = os.path.join(os.path.dirname(__file__), 'data', 'product_data.xlsx')
spreadsheet_data_repo = SpreadsheetDataRepository(xlsx_path)

def post_init_hook(env, registry=None):

    env['ir.config_parameter'].set_param('product_variant_count', True)

    product_attribute_repository = ProductAttributeRepository(env)
    product_template_repository = ProductTemplateRepository(env)

    try:
        product_attributes = spreadsheet_data_repo.get_product_attributes()
        
        created_product_attributes = product_attribute_repository.load_product_attributes(product_attributes)

        product_attribute_values = spreadsheet_data_repo.get_product_attribute_values()
        
        product_attribute_repository.load_product_attribute_values(product_attribute_values)

        product_templates = spreadsheet_data_repo.get_product_templates()
        product_template_attribute_lines = spreadsheet_data_repo.get_product_template_attribute_lines()
        
        product_template_repository.load_product_templates_and_their_attribute_lines(product_templates, product_template_attribute_lines)
        
    except Exception as e:
        _logger.exception("Error during post-init hook")
        raise e


def uninstall_hook(env, registry=None):

    product_attribute_repository = ProductAttributeRepository(env)
    product_template_repository = ProductTemplateRepository(env)

    try:
        product_attribute_lines = env['product.template.attribute.line'].search([])
        product_attribute_lines.unlink()

        product_attribute_values_external_ids = env['ir.model.data'].search([('model', '=', 'product.template.attribute.line'), ('module', '=', get_module_name())])
        product_attribute_values_external_ids.unlink()


        product_attribute_repository.delete_all_product_attributes()
        product_attribute_external_ids = env['ir.model.data'].search([('model', '=', 'product.attribute'), ('module', '=', get_module_name())])
        product_attribute_external_ids.unlink()

        product_attribute_repository.delete_all_product_attribute_values()

        product_attribute_values_external_ids = env['ir.model.data'].search([('model', '=', 'product.attribute.value'), ('module', '=', get_module_name())])
        product_attribute_values_external_ids.unlink()

        product_template_repository = ProductTemplateRepository(env)
        product_template_repository.delete_all_product_templates()

        product_template_external_ids = env['ir.model.data'].search([('model', '=', 'product.template'), ('module', '=', get_module_name())])
        product_template_external_ids.unlink()

        env['ir.config_parameter'].set_param('product_variant_count', False)

    except Exception as e:
        _logger.exception("Error during uninstall hook")
        raise e
