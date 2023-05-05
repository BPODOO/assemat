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

import logging
_logger = logging.getLogger(__name__)

from PyPDF2 import PdfFileReader, PdfFileWriter

class MailComposer(models.TransientModel):
    _inherit = "mail.compose.message"
    
    def action_generate_report_quotation(self):
        report_name = "sale.report_saleorder"
        report_id = self.env["ir.actions.report"]._get_report_from_name(report_name)

        sale_order = self.env['sale.order'].browse(self.res_id)

        pdf_files_merged = []

        #Récupération du rapport OF
        report = self.env["ir.actions.report"].browse(report_id.id)

        report_output = self.env['ir.actions.report']._render_qweb_pdf('sale.action_report_saleorder', [self.res_id])

        #Récupération des PDF provenant de l'article de l'OF
        attachment_ids = sale_order.bp_upload_annexes

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
        
        sale_order.bp_regenerate_report_annexe = False
        sale_order.env.context = dict(sale_order.env.context)
        sale_order.env.context.update({
        'regenerate_report': True
        })
        if sale_order.bp_report_annexe:
            sale_order.bp_report_annexe.unlink()
            sale_order.bp_report_annexe = [(6, 0, [attachment_pdf.id])]
        else:
            sale_order.bp_report_annexe = [(6, 0, [attachment_pdf.id])]
            
        self.attachment_ids = [(6, 0, [attachment_pdf.id])]
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'res_id': self.id,
            'context': self._context,
        }

        