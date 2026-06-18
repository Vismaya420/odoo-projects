from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    purchase_rental_id = fields.Many2one(
        'purchase.rental',
        string='Purchase Rental',
        readonly=True
    )
