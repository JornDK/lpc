# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import literal_eval

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    price_calculation = fields.Selection(related='company_id.price_calculation', 
        string="Calculate Unit Price based on Height/Width", store=True, readonly=False)
    
