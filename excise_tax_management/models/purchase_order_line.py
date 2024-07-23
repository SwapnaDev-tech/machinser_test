from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    company_currency_id = fields.Many2one('res.currency',
                                          related='company_id.currency_id',
                                          string="Company Currency",
                                          readonly=True)
    excise_tax = fields.Monetary(string='Excise Tax',
                                 help="Used for adding excise tax manually",
                                 currency_field='company_currency_id')
    price_total = fields.Monetary(compute='_compute_amount', string='Total')

    @api.depends('excise_tax')
    def _compute_amount(self):
        """Override the function _compute_amount for adding the
        excise tax with price_total and price_subtotal"""
        for line in self:
            line_price = line.price_unit * line.product_qty
            taxes = line.taxes_id.compute_all(line_price,
                                              line.order_id.currency_id,
                                              line.product_qty,
                                              product=line.product_id,
                                              partner=line.order_id.partner_id)
            excise_tax = line.excise_tax or 0.0
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'] + excise_tax,
                'price_subtotal': taxes['total_excluded'] + excise_tax,
            })

    def _prepare_account_move_line(self, move=False):
        """To get excise tax to vendor bill"""
        res = super()._prepare_account_move_line(move=move)
        res.update({'excise_tax': self.excise_tax})
        return res

