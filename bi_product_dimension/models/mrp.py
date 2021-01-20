# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare


class mrp_production(models.Model):
    _inherit = "mrp.production"
    
    @api.depends('height','width')
    def _get_squaremeter(self):
        for record in self:
            if record.width == 0.00 or record.height == 0.00:
                square_meter = 1.00
            else:
                square_meter = record.width * record.height
            record.update({
                'square_meter' : square_meter
            })
 
    width = fields.Float('Width (Mt.)', required='True', default=0.0)
    height =  fields.Float('Height (Mt.)', required='True',default=0.0)
    square_meter =  fields.Float(compute='_get_squaremeter',string='(Mt.)2',store=True)