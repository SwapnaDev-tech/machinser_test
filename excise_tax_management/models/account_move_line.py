from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    excise_tax = fields.Monetary(string="Excise Tax Amount")
    price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)

    @api.depends('quantity', 'price_unit', 'tax_ids', 'excise_tax')
    def _compute_amount(self):
        """Override the method to calculate amounts for invoice lines
        including the Excise Tax."""
        for line in self:
            line_price = line.price_unit * line.quantity
            taxes = line.tax_ids.compute_all(line_price,
                                             line.move_id.currency_id,
                                             line.quantity,
                                             product=line.product_id,
                                             partner=line.move_id.partner_id)
            excise_tax = line.excise_tax or 0.0
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'] + excise_tax,
                'price_subtotal': taxes['total_excluded'] + excise_tax,
            })
