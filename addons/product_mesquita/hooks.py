import os
import logging
from .SpreadsheetDataRepository import SpreadsheetDataRepository
from .ProductAttributeRepository import ProductAttributeRepository
from .get_module_name import get_module_name

_logger = logging.getLogger(__name__)

xlsx_path = os.path.join(os.path.dirname(__file__), 'data', 'product_data.xlsx')
spreadsheet_data_repo = SpreadsheetDataRepository(xlsx_path)


def post_init_hook(env, registry=None):

    product_attribute_repository = ProductAttributeRepository(env)
    product_attribute_repository.delete_all_product_attributes()
    product_attribute_repository.delete_all_product_attribute_values()

    try:
        product_attributes = spreadsheet_data_repo.get_product_attributes()
        created_product_attributes = product_attribute_repository.load_product_attributes(product_attributes)

        product_attribute_values = spreadsheet_data_repo.get_product_attribute_values()
        product_attribute_repository.load_product_attribute_values(
            product_attribute_values)
    except Exception as e:
        _logger.exception("Error during post-init hook")
        raise e


def uninstall_hook(env, registry=None):

    product_attribute_repository = ProductAttributeRepository(env)

    try:
        product_attribute_repository.delete_all_product_attributes()
        product_attribute_repository.delete_all_product_attribute_values()

        external_ids = env['ir.model.data'].search([('model', '=', 'product.attribute'), ('module', '=', get_module_name())])
        external_ids.unlink()

        external_ids = env['ir.model.data'].search([('model', '=', 'product.attribute.value'), ('module', '=', get_module_name())])
        external_ids.unlink()
    except Exception as e:
        _logger.exception("Error during uninstall hook")
        raise e
