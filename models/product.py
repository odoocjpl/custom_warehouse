import itertools
import psycopg2

import odoo.addons.decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    long_name = fields.Char('Detailed Specification',track_visibility="onchange")
    short_name = fields.Char('Short Name',track_visibility="onchange")
    current_name = fields.Char('Current Name')
    short_name_product = fields.Char('Short Name for Component in Bom',track_visibility="onchange")