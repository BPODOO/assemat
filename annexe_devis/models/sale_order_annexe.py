# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrderAnnexe(models.Model):
    _name = 'sale.order.annexe'

    def _default_name_annexe(self, context):
        num = 0
        if 'params' in context.keys():
            id = context['params']['id']
            num = self.env['sale.order.annexe'].search_count([('bp_sale_order_id','=',id)])
        return f"Annexe {num + 1} - numéro du devis - Assemat Agencements"

    sequence = fields.Integer()
    name = fields.Char(string='Titre', default=lambda self: self._default_name_annexe(self.env.context))
    bp_image = fields.Binary(string="Fichier")
    bp_name_annexe = fields.Char()
    bp_sale_order_id = fields.Many2one('sale.order')
    bp_ir_attachment_id = fields.Many2one('ir.attachment', ondelete="cascade", string="Document")

    @api.onchange('bp_ir_attachment_id')
    def onchange_bp_ir_attachment_id(self):
        for record in self:
            if record.bp_ir_attachment_id:
                record.bp_name_annexe = record.bp_ir_attachment_id.name
                record.bp_image = record.bp_ir_attachment_id.datas
        
    
    @api.model_create_multi   
    def create(self, vals_list):
        res = super(SaleOrderAnnexe, self).create(vals_list)
        for annexe in res:
            annexe['sequence'] += 1 
            attachment_create_vals = {
                    'name': annexe.bp_name_annexe,
                    'datas': annexe.bp_image,
                    'res_model': 'sale.order.annexe',
                    'res_id': annexe.id,
                    'type': 'binary',
                    "public": True,
            }
            ir_attachement = self.env['ir.attachment'].create(attachment_create_vals)
            res.bp_ir_attachment_id = ir_attachement.id
        return res

    def unlink(self):
        res = super(SaleOrderAnnexe, self).unlink()
        return res


        