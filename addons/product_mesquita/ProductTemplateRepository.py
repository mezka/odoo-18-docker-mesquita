from .get_module_name import get_module_name

class ProductTemplateRepository:

    def __init__(self, env):
        self.env = env

    def load_product_templates_and_their_attribute_lines(self, product_templates, product_template_attribute_lines):

        created_product_templates = []

        for product_template in product_templates:
            product_template_without_ext_ids = {key: product_template[key] for key in product_template if key not in ['id', 'attribute_line_ids/id']}
            created_product_template = self.env['product.template'].create(product_template_without_ext_ids)

            self.env['ir.model.data'].create({
                'name': product_template['id'],
                'model': 'product.template',
                'res_id': created_product_template.id,
                'module': get_module_name()
            })

            created_product_templates.append(created_product_template)

            elegible_attribute_lines = filter(lambda pt_attr_ln: pt_attr_ln['product_tmpl_id/id'] == product_template['id'], product_template_attribute_lines)

            for attribute_line in elegible_attribute_lines:

                product_attribute = self.env.ref(f'{get_module_name()}.{attribute_line['attribute_id/id']}')
                value_ids = list(map(lambda value_id: self.env.ref(f'{get_module_name()}.{value_id}').id, attribute_line['value_ids/id']))

                created_attribute_line = self.env['product.template.attribute.line'].create({
                    'product_tmpl_id': created_product_template.id,
                    'attribute_id': product_attribute.id,
                    'value_ids': [(6, 0, value_ids)]
                })

                self.env['ir.model.data'].create({
                    'name': attribute_line['id'],
                    'model': 'product.template.attribute.line',
                    'res_id': created_attribute_line.id,
                    'module': get_module_name()
                })

        return created_product_templates

    def delete_all_product_templates(self):
        product_templates_to_delete = self.env['product.template'].search([])

        for product_template in product_templates_to_delete:
            self.delete_product_template_attribute_lines(product_template)
            external_ids = self.env['ir.model.data'].search([
                ('model', '=', 'product.template'),
                ('res_id', '=', product_template.id),
                ('module', '=', get_module_name())
            ])
            external_ids.unlink()
            product_template.unlink()

        return True

    def delete_product_template_attribute_lines(self, product_template):

        product_template_attribute_lines_to_delete = self.env['product.template.attribute.line'].search([
            ('product_tmpl_id', '=', product_template.id)
        ])

        for product_template_attribute_line in product_template_attribute_lines_to_delete:
            external_ids = self.env['ir.model.data'].search([
                ('model', '=', 'product.template.attribute.line'),
                ('res_id', '=', product_template_attribute_line.id),
                ('module', '=', get_module_name())
            ])
            external_ids.unlink()
            product_template_attribute_line.unlink()

        return True