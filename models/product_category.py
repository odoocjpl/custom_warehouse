import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
import odoo.addons.decimal_precision as dp


class ProductCategory(models.Model):
    _inherit="product.category"

    numbered = fields.Boolean('Numbered')
    can_altered = fields.Boolean('Can Be Altered')
    category_template_lines = fields.One2many('category.template','category_id1','Product Category')
    prefix = fields.Char('Prefix')
    specification_lines = fields.One2many('specification.line','category_id1','Specifications')       
    
class category_template(models.Model):
    _name="category.template"
    
    category_id = fields.Many2one('product.category','Category')
    seq_no = fields.Integer('Sequence No')
    part_name = fields.Boolean('Part of Name')
    mandatory = fields.Boolean('Mandatory')
    category_id1 = fields.Many2one('product.category','Category')
    
class specification_line(models.Model):
    _name="specification.line"
    
    seq_no = fields.Integer('Sequence No')
    name = fields.Char('Name')
    category_id1 = fields.Many2one('product.category','Category',required="1")
        