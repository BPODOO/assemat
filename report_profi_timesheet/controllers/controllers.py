# -*- coding: utf-8 -*-
import logging
try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO
# import zipfile
from datetime import datetime
from odoo import http
from odoo.http import request
from odoo.http import content_disposition
import ast
import base64
import io

from PyPDF2 import PdfFileReader, PdfFileWriter
_logger = logging.getLogger(__name__)

class Binary(http.Controller):
    @http.route('/web/binary/print_report_renta_timesheet', type='http', auth="public")
    def print_report_renta_timesheet(self, project_ids, **kw):
        project_ids =  ast.literal_eval(project_ids)

        projects = request.env['project.project'].browse(project_ids)
        
        pdf_files_merged = list()

        for project in projects:
            
            # Récupération du rapport Rentabilité détaillé
            report_output_profi = request.env['ir.actions.report'].sudo()._render_qweb_pdf('report_profi_details.report_profitability_details', [project.id])
            pdf_files_merged.append(io.BytesIO(report_output_profi[0]))

            # Récupération du rapport Feuilles de temps
            report_output_timesheet = request.env['ir.actions.report'].sudo()._render_qweb_pdf('hr_timesheet.report_timesheet_project', [project.id])
            pdf_files_merged.append(io.BytesIO(report_output_timesheet[0]))
        
        #Parcours PDFBytes par PDF
        writer = PdfFileWriter()
        for pdf in pdf_files_merged:
            reader = PdfFileReader(pdf, strict=False, overwriteWarnings=False)
            for page_number in range(reader.getNumPages()):
                writer.addPage(reader.getPage(page_number))
            
        filename = datetime.now()
        filename = "Rapport Renta detaille - Feuille de temps %s.pdf" % filename
        
        _buffer = io.BytesIO()
        writer.write(_buffer)
        merged_pdf = _buffer.getvalue()
        _buffer.close()
        
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(merged_pdf)),('Content-Disposition', content_disposition(filename))]
        return request.make_response(merged_pdf, headers=pdfhttpheaders)




            
