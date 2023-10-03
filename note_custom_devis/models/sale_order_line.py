# -*- coding: utf-8 -*-

from odoo import models, fields, api, Command
import logging
import re
from odoo.tools import float_is_zero
from itertools import groupby

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
       
    name_without_html = fields.Html(string='Description bis')

    @api.onchange('name')
    def load_name_desc_devis(self):
        if self.name:
            html = "<p>" + self.name.replace("\n", "<br>") + "</p>"
            self.name_without_html = html
    
    def action_show_details(self):
        view = self.env.ref('note_custom_devis.view_sale_order_line_desc_details_form_bp')
        action = {
            'name': 'Description details',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sale.order.line',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id,
        }
        return action
    
    def remove_html(self, string):
        string = str(string).replace("<br>", "\n")
        regex = re.compile(r'<[^>]+>|&nbsp;')
        return regex.sub('', string)
    
    def action_save(self):
        note_custom = self.name_without_html
        if 'img' in note_custom:
            src_img = note_custom[note_custom.find('/')+len('/'):note_custom.find('?')].split('/').pop()
            self.name = src_img
        else:
            self.name = self.remove_html(self.name_without_html)
        return {'type': 'ir.actions.act_window_close'}