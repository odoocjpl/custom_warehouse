import itertools
import psycopg2

import odoo.addons.decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    long_name = fields.Char('Long Name')
    short_name = fields.Char('Short Name')