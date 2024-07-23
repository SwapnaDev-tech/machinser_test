from odoo import models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _post(self, soft=True):
        """To create separate journal for excise tax."""
        res = super(AccountMove, self)._post(soft)
        for move in self:
            excise_tax_total = sum(line.excise_tax for line in move.invoice_line_ids)
            if excise_tax_total:
                self.env['account.move.line'].create({
                    'move_id': move.id,
                    'name': 'Excise Tax',
                    'account_id': self.env['account.account'].search([('name', '=', 'Expenses')], limit=1).id,
                    'debit': excise_tax_total if move.move_type in ('in_invoice', 'out_refund') else 0,
                    'credit': excise_tax_total if move.move_type in ('out_invoice', 'in_refund') else 0,
                })
        return res

    @api.onchange('invoice_line_ids.excise_tax')
    def _onchange_invoice_line_ids_excise_tax(self):
        """Allow the user to update the excise tax in the vendor bill lines and
        recalculate the journal entries."""
        self._compute_amount()
        self._post(False)
