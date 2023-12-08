# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrderAnnexe(models.Model):
    _name = 'sale.order.annexe'

    def _default_name(self, context):
        return "Assemat Agencements"
    
    sequence = fields.Integer()
    name = fields.Char(string='Titre', default=lambda self: self._default_name(self.env.context), readonly=False)
    bp_name_annexe = fields.Char()
    bp_image = fields.Binary(string="Fichier")
    bp_sale_order_id = fields.Many2one('sale.order', store=True)
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
        note_annexe_exist = res.bp_sale_order_id.order_line.filtered(lambda x: x.bp_is_note_annexe == True)
        if len(note_annexe_exist) == 0 :
            self.env['sale.order.line'].create({
                    'sequence': 0,
                    'display_type': 'line_note',
                    'order_id': res.bp_sale_order_id.id,
                    'name':'Voir images et croquis en annexe du devis qui font parties intégrantes de celui-ci',
                    'bp_is_note_annexe': True,
                })
        for annexe in res:
            _logger.info(annexe)
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
            annexe.bp_ir_attachment_id = ir_attachement.id
        return res

    def unlink(self):
        sale_id = self.bp_sale_order_id
        res = super(SaleOrderAnnexe, self).unlink()
        if not sale_id.bp_sale_order_annexe_ids:
            note_annexe_exist = sale_id.order_line.filtered(lambda x: x.bp_is_note_annexe == True)
            _logger.info(note_annexe_exist)
            note_annexe_exist.unlink()
        return res


        