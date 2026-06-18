from odoo import models, fields, api

class PurchaseRental(models.Model):
    _name = 'purchase.rental'
    _description = 'Purchase Rental'

    name = fields.Char(
        string='Reference',
        required=True,
        readonly=True,
        default='New'
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Vendor',
        required=True
    )

    order_date = fields.Datetime(
        string='Order Date',
        default=fields.Datetime.now
    )

    scheduled_date = fields.Datetime(
        string='Scheduled Date'
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )

    note = fields.Text(string='Notes')

    user_id = fields.Many2one(
        'res.users',
        string='Responsible',
        default=lambda self: self.env.user
    )

    line_ids = fields.One2many(
        'purchase.rental.line',
        'rental_id',
        string='Purchase Rental Lines'
    )

    state = fields.Selection([
        ('requested', 'Requested'),
        ('confirmed', 'Confirmed'),
        ('received', 'Received'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    ], default='requested')
    
    
    # Sequence generation for purchase rental reference    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.rental') or 'New'
        return super().create(vals)
    
    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_receive(self):
        self.write({'state': 'received'})
    
    def action_return(self):
        self.write({'state': 'returned'})
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})
    
    def action_reset_to_requested(self):
        self.write({'state': 'requested'})

    # Create vendor bill from purchase rental
    def action_create_bill(self):
        self.ensure_one()
        move = self.env['account.move']
        bill_lines = []
        for line in self.line_ids:
            bill_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.name,
                'quantity': line.product_qty,
                'price_unit': line.price_unit,
                'tax_ids': [(6, 0, line.product_id.supplier_taxes_id.ids)],
            }))
    
        bill = move.create({
            'move_type': 'in_invoice',
            'partner_id': self.partner_id.id,
            'currency_id': self.currency_id.id,
            'company_id': self.company_id.id,
            'invoice_origin': self.name,
            'purchase_rental_id': self.id,
            'invoice_line_ids': bill_lines,
        })
    
        return {
            'type': 'ir.actions.act_window',
            'name': 'Vendor Bill',
            'res_model': 'account.move',
            'res_id': bill.id,
            'view_mode': 'form',
        }

    # Smart button to view related vendor bills
    def action_view_bills(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bills',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [
                ('purchase_rental_id', '=', self.id),
                ('move_type', '=', 'in_invoice')
            ],
        }


class PurchaseRentalLine(models.Model):
    _name = 'purchase.rental.line'
    _description = 'Purchase Rental Line'

    rental_id = fields.Many2one(
        'purchase.rental',
        string='Purchase Rental',
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        domain="[('is_rental_item','=',True)]",
        required=True
    )
    name = fields.Char(string='Description')
    product_qty = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price')
    tax_ids = fields.Many2many('account.tax',string='Taxes')
    subtotal = fields.Float(string='Subtotal',compute='_compute_subtotal')



    @api.onchange('product_id')
    def _onchange_product_id(self):
        if not self.product_id:
            return
        self.name = self.product_id.display_name
        self.price_unit = self.product_id.standard_price
      
    @api.depends('product_qty','price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.product_qty * line.price_unit
            
            
            
            
            
            
            
            
