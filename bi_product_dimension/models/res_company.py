from odoo import models,fields

class res_partner(models.Model):
    
    _inherit = "res.company"
    
    vat_registration_no = fields.Char('VAT Registration No.')
    price_calculation = fields.Selection([
        ('dimension', 'Price Calculation based on Dimension(m2)'),
        ('qty', 'Price Calculation based on Qty'),
    ], string='Calculate Unit Price based on Height/Width', default='dimension')

