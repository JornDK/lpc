# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare

class SaleOrder(models.Model):
    
    _inherit = "sale.order"
    
    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)
        if self.env.user.company_id.price_calculation == 'qty':
            res['hide_net_price'] = True
        return res

    dispatch_type =  fields.Selection([
        ('deliver','Deliver'),
        ('collect','Collect'),
        ('Courier','courier')],string='Dispatch Type')
    hide_net_price = fields.Boolean(string='Hide net price')

class  sale_order_line(models.Model):    
    _inherit = "sale.order.line"

    @api.depends('height', 'width', 'product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            if line.order_id.company_id.price_calculation == 'dimension':
                quantity = line.product_uom_qty * line.m2
            else:
                quantity = line.product_uom_qty

            price = line.price_unit * (1 - (line.discount or 0.0)/100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id,quantity , product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
    
    @api.depends('height','width')
    def _get_m2(self):
        for record in self:
            if record.width == 0.0 or record.height == 0.0:
                m2 = 1.00
            else:
                m2 = record.width * record.height

            record.update({
                'm2' : m2
            })
    
    @api.depends('height','width','price_unit','product_uom_qty')
    def _get_net_price(self):
        for record in self:
            if record.width == 0.00 or record.height == 0.00:
                net_price = record.price_unit * record.product_uom_qty
            else:
                net_price = (record.width * record.height) * record.price_unit * record.product_uom_qty

            record.update({
                'net_price' : net_price
            })

    width = fields.Float('Width (Mt.)', required='True',default=0.0 )
    height = fields.Float('Height (Mt.)', required='True', default=0.0)
    m2 = fields.Float(compute='_get_m2',string='(Mt.)2', store=True)
    net_price = fields.Float(compute='_get_net_price', string="Net Price", store=True)
    hide_net_price = fields.Boolean(string='Hide net price', 
        related='order_id.hide_net_price', store=True)

    def _prepare_invoice_line(self, **optional_values):
        res = super(sale_order_line, self)._prepare_invoice_line(**optional_values)
        
        res.update({
            'width':self.width,
            'height':self.height,
            'm2':self.m2,
        })
        return res

    def _prepare_procurement_values(self, group_id=False):
        res = super(sale_order_line, self)._prepare_procurement_values(group_id=group_id)
        res.update({
            'width':self.width,
            'height':self.height
        })
        return res