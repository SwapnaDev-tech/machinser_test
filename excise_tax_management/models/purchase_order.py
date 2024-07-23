from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """Override the function for recalculating the order rotal with
        excise tax"""
        for order in self:
            amount_untaxed = amount_tax = amount_excise_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                amount_excise_tax += line.excise_tax
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax + amount_excise_tax,
            })


