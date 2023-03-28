# -*- coding: utf-8 -*-
from odoo import http

import ast
from werkzeug.urls import url_join

import logging
_logger = logging.getLogger(__name__)

class OuvrageLine(http.Controller):
    
    @http.route('/lines/monitoring', type='http', auth='user', website=True)
    def redirectToMonitoringSale(self, order_id, **kwargs):
        order_id = ast.literal_eval(order_id)
        
        menu_id = http.request.env.ref('sale.sale_menu_root').id
        
        action_id = http.request.env.ref('ouvrage_line.action_open_line_monitoring')
        action_data = action_id.read()[0]
        
        action_data['domain'] = [('order_id', '=', order_id)]
        
        action_id.write(action_data)
        
        url = "/web?#view_type=list&model=sale.order.line&&menu_id=%s&action=%s" % (menu_id, action_id.id)
        return http.request.redirect(url)