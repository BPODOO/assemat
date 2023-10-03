# -*- coding: utf-8 -*-

from odoo import models, fields, api, Command
import logging
import re
from odoo.tools import float_is_zero
from itertools import groupby

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    name_without_html = fields.Html(string='Description bis')