# -*- coding: utf-8 -*-

from odoo import models, fields, api

try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO
# import zipfile
from datetime import datetime
import ast
import base64
import io
import img2pdf
import mimetypes
from odoo.tools.mimetypes import guess_mimetype
from PIL import Image
import os

import logging
_logger = logging.getLogger(__name__)

from PyPDF2 import PdfFileReader, PdfFileWriter

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    bp_upload_annexes = fields.Many2many('ir.attachment','ir_attachment_sale_order_rel_1','sale_order_id','ir_attachment_id',string='Charger fichiers')
    bp_report_annexe = fields.Many2many('ir.attachment','ir_attachment_sale_order_rel_2','sale_order_id','ir_attachment_id',string='')
    bp_regenerate_report_annexe = fields.Boolean()
    
    @api.onchange('bp_upload_annexes')
    def onchange_upload_annexes(self):
        for record in self:
            attachment = record.bp_upload_annexes._origin
            attachment.res_model = ''
            attachment.res_id = 0
            attachment.res_name = ''

    def action_quotation_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id = self._find_mail_template()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id.id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
            'report_with_annexe': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def action_generate_report_quotation_sale(self):
        report_name = "sale.report_saleorder"
        report_id = self.env["ir.actions.report"]._get_report_from_name(report_name)

        pdf_files_merged = []

        #Récupération du rapport OF
        report = self.env["ir.actions.report"].browse(report_id.id)

        report_output = self.env['ir.actions.report']._render_qweb_pdf('sale.action_report_saleorder', [self.id])

        #Récupération des PDF provenant de l'article de l'OF
        attachment_ids = self.bp_upload_annexes

        writer = PdfFileWriter()
        #Création d'un seul tableau avec les PDF du produit et les PDF des OT, en BytesIO
        pdf_files = [{'filename':attachment_id.name,'data': io.BytesIO(base64.b64decode(attachment_id.datas))} for attachment_id in attachment_ids]
        pdf_files.insert(0, {'filename': False,'data': io.BytesIO(report_output[0])})
        pdf_files_merged = pdf_files_merged + pdf_files
        #Parcours PDFBytes par PDF
        for pdf in pdf_files_merged:
            if pdf['filename'] != False:
                type_file = mimetypes.guess_type(pdf['filename'])
                name_type = type_file[0].split('/')
                if name_type[0] == 'image':
                    #page size format A4
                    a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
                    # Mode shrink pour concerver la taille des images
                    layout_fun = img2pdf.get_layout_fun(a4inpt, fit=img2pdf.FitMode.shrink ,auto_orient=True)
                    # Convert image to PDF
                    document = img2pdf.convert(pdf['data'],layout_fun=layout_fun)
                    reader = PdfFileReader(io.BytesIO(document), strict=False)
                else:
                    reader = PdfFileReader(pdf['data'], strict=False, overwriteWarnings=False)
            else:
                reader = PdfFileReader(pdf['data'], strict=False, overwriteWarnings=False)
            
            for page_number in range(reader.getNumPages()):
                writer.addPage(reader.getPage(page_number))
                
        filename = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = "Devis & Annexes %s.pdf" % filename
        
        _buffer = io.BytesIO()
        writer.write(_buffer)
        merged_pdf = _buffer.getvalue()
        _buffer.close()

        attachment_pdf = self.env['ir.attachment'].create({
            'name': filename,
            'datas': base64.b64encode(merged_pdf),
            'mimetype': 'application/pdf'})
        
        self.bp_regenerate_report_annexe = False
        self.env.context = dict(self.env.context)
        self.env.context.update({
        'regenerate_report': True
        })
        if self.bp_report_annexe:
            self.bp_report_annexe.unlink()
            self.bp_report_annexe = [(6, 0, [attachment_pdf.id])]
        else:
            self.bp_report_annexe = [(6, 0, [attachment_pdf.id])]
    
    
    @api.model
    def write(self, vals):
        _logger.info(self._context)
        if 'regenerate_report' in self._context and self._context.get('regenerate_report'):
            vals['bp_regenerate_report_annexe'] = False
        else:
            vals['bp_regenerate_report_annexe'] = True
        res = super(SaleOrder, self).write(vals)
        return res



