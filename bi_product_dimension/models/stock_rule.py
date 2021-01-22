# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare

class StockRuleDetail(models.Model):
    _inherit = 'stock.rule'

    width = fields.Float('Width')
    height =  fields.Float('Height')

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        result = super(StockRuleDetail, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, company_id, values)
        result.update({
            'width':values.get('width'),
            'height':values.get('height'),
        })
        return result


    def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values, bom):
        result = super(StockRuleDetail, self)._prepare_mo_vals(product_id, product_qty, product_uom, location_id, name, origin, company_id, values, bom)
        result.update({
            'width': values.get('width'),
            'height': values.get('height'),    
        })
        return result


    def _update_purchase_order_line(self, product_id, product_qty, product_uom, company_id, values, line):
        result = super(StockRuleDetail, self)._update_purchase_order_line(product_id, product_qty, product_uom, company_id, values, line)
        result.update({
            'width': values.get('width'),
            'height': values.get('height'),    
        })
        return result    


    @api.model
    def _prepare_purchase_order_line(self, product_id, product_qty, product_uom, company_id, values, po):
        result = super(StockRuleDetail, self)._prepare_purchase_order_line(product_id, product_qty, product_uom, company_id, values, po)
        result.update({
            'width': values.get('width'),
            'height': values.get('height'),    
        })
        return result