# -*- coding: utf-8 -*-
from odoo import http

class OuvrageLine(http.Controller):
    
    @http.route('/none', type='http', auth='user', website=True)
    def redirectToMonitoringSale(self, **kwargs):
        _logger.info("Controller to redirect")