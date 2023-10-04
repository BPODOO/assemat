# -*- coding: utf-8 -*-

from odoo import models, fields, api, Command
import logging
import re
from odoo.tools import float_is_zero
from itertools import groupby

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
       
    bp_name_without_html = fields.Html(string='Description bis')
    bp_path_img = fields.Json()
    
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
        html_to_str = str(self.bp_name_without_html)
        notes_custom = html_to_str.split('<p>')
        if 'img' in self.bp_name_without_html:
            list_path_img = []
            for object in notes_custom:
                if 'img' in object:
                    src_img = object[object.find('/')+len('/'):object.find('?')]
                    list_path_img.append(src_img)
            self.bp_path_img = {'data':list_path_img}
            self.name = f"{len(list_path_img)} images"
        else:
            self.name = self.remove_html(self.bp_name_without_html)
        return {'type': 'ir.actions.act_window_close'}
        