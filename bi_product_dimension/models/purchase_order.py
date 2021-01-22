# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare

class purchase_order(models.Model):
    _inherit = "purchase.order"
    
    @api.model
    def default_get(self, fields):
        res = super(purchase_order, self).default_get(fields)
        if self.env.user.company_id.price_calculation == 'qty':
            res['hide_net_price'] = True
        return res

    @api.depends('order_line.price_total',
        'order_line.height',
        'order_line.width',
        'order_line.taxes_id')
    def _amount_all(self):
        return super(purchase_order, self)._amount_all()

    hide_net_price = fields.Boolean(string='Hide net price')
    dispatch_type =  fields.Selection([
        ('deliver','Deliver'),
        ('collect','Collect'),
        ('Courier','courier')],string='Dispatch Type')


class purchase_order_line(models.Model):
    _inherit = "purchase.order.line"


    @api.depends('product_qty', 'price_unit', 'taxes_id', 'width', 'height')
    def _compute_amount(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            if line.order_id.company_id.price_calculation == 'dimension':
                quantity = vals['product_qty'] * line.square_meter
            else:
                quantity = vals['product_qty']

            taxes = line.taxes_id.compute_all(
                vals['price_unit'],
                vals['currency_id'],
                quantity,
                vals['product'],
                vals['partner'])
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    def _create_stock_moves(self, picking):
        values = []
        for line in self.filtered(lambda l: not l.display_type):
            for val in line._prepare_stock_moves(picking):
                val.update({
                    'width':line.width,
                    'height':line.height,
                })
                values.append(val)
        return self.env['stock.move'].create(values)
    
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

    @api.depends('height','width', 'product_qty', 'price_unit')
    def _compute_net_price(self):
        for record in self:
            if record.width == 0.00 or record.height == 0.00:
                net_price = record.price_unit * record.product_qty
            else:
                net_price = (record.width * record.height) * record.price_unit * record.product_qty

            record.update({
                'net_price_pur' : net_price
            })

    width=fields.Float('Width (Mt.)', required='True', default=0.0)
    height= fields.Float('Height (Mt.)', required='True',default=0.0)
    square_meter= fields.Float(compute='_get_squaremeter',string='(Mt.)2', store=True)
    net_price_pur = fields.Float(string='Net Price',compute='_compute_net_price', store=True)
    hide_net_price = fields.Boolean(string='Hide net price', 
        related='order_id.hide_net_price', store=True)


    def _prepare_account_move_line(self,move=False):
        res = super(purchase_order_line,self)._prepare_account_move_line(move)
        res.update({
            'width':self.width, 'height':self.height, 
        })
        return res
