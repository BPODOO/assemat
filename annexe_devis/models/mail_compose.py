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
        attachment_pdf = sale_order.action_generate_report_quotation_sale()
            
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

        