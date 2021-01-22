# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "Product Dimensions(Height/Width) on Sales, Purchase, Invoice and Manufacturing in odoo",
    "version" : "14.0.0.2",
    'category' : 'Sales',
    'summary': 'Sale product Dimensions purchase product Dimensions Manufacturing product Dimensions height and width on product height on product width on product height attribute product Width attribute Product Dimension on orders Product Dimension on sale Dimension',
    "description": """
    Product Dimension (Height/Width) Value on Sales, Purchase, Invoice and Manufacturing

    dimension
	Product Dimension on Sales, Purchase, Invoice and Manufacturing , product measurements in odoo, product size in odoo, product parameter in odoo
    Product Dimension on Purchase, Invoice and Manufacturing
    Product Dimension on Invoice and Manufacturing, measurement of products , measurement of item ,item dimension , calculate product size
    Product Dimension on Manufacturing , openerp
    Product Dimension on orders

    Product Height/Width on Sales, Purchase, Invoice and Manufacturing
    Product Height/Width on Purchase, Invoice and Manufacturing
    Product Height/Width on Invoice and Manufacturing
    Product Height/Width on Manufacturing
    Product Height/Width on orders

    height and widht on product
    height on product
    widht on product
    product height attribute
    product Width attribute
    product Width parameter
    product height parameter
    product height and widht

    length on product
    dimension on product
    product dimension attribute
    product variable lenght and height attribute
    product height and Width parameter
    product length and height parameter
    product variable height and widht attribute
    product variable Width attribute
    product variable height parameter
    product dimension parameter
    Product Dimensions
    item Dimensions
    Dimensions product


    """,
    "author" : "BrowseInfo",
    "website" : "https://www.browseinfo.in",
    "price": 89,
    "currency": 'EUR',
    "depends" : ['sale_management','account','purchase','mrp','base','base_vat'],
    "data" : [
              'views/res_company_view.xml',
              'views/sale_view.xml',
              'views/sale_order_report_view.xml',
              'views/mrp_production_report_templates.xml',
              'views/purchase_order_report_templates.xml',
              'views/invoice_report_view.xml',
              'views/mo_extended.xml',
              'views/setting_config_view.xml',
              ],
    "auto_install": False,
    "installable": True,
    "live_test_url":'https://youtu.be/eXM_6QEYpbQ',
    "images":["static/description/Banner.png"],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
