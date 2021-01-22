# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare

class stock_move(models.Model):
    
    _inherit = "stock.move"
    
    width = fields.Float('Width (Mt.)', required='True', default=0.0)
    height =  fields.Float('Height (Mt.)', required='True', default=0.0)


    def _prepare_procurement_values(self):
        result = super(stock_move, self)._prepare_procurement_values()
        result.update({
            'width' : self.width,
            'height' :  self.height,
        })
        return result
