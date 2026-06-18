from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_rental_item = fields.Boolean(string='Is Rental Item')
