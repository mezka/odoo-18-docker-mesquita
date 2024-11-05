from odoo import api, SUPERUSER_ID
from .load_product_data import load_product_data

def post_init_hook(env, registry=None):
    load_product_data(env)

def uninstall_hook(env, registry=None):
    env['product.template'].search([]).unlink()
