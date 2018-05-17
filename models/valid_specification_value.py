import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
import odoo.addons.decimal_precision as dp

class valid_specification_value(models.Model):
    _name="valid.specification.value"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    @api.model
    def create(self,vals):
        if vals.get('short_name'):
            if re.match("^[a-zA-Z0-9]*$", vals['short_name']):
                print"fbdbn"
            else:
                raise UserError(_('You can not use any special symbol.'))
            valid = self.env['valid.specification.value'].search([('short_name','=',vals['short_name'])])
            if valid:
                raise UserError(_('You can not use the duplicate short name.'))
        if vals.get('product_category_id') and vals.get('specification_id') and vals.get('name'):
            valid = self.env['valid.specification.value'].search([('product_category_id','=',vals['product_category_id']),('specification_id','=',vals['specification_id']),('name','=',vals['name'])])
            if valid:
                raise UserError(_('You can not repeat the valid value for same specification.'))
        product_id =  super(valid_specification_value,self).create(vals)
        return product_id
    
    @api.multi
    def write(self,vals):
        if 'short_name' in vals and vals['short_name']:
            if re.match("^[a-zA-Z0-9]*$", vals['short_name']):
                print"fbdbn"
            else:
                raise UserError(_('You can not use any special symbol.'))
            valid = self.env['valid.specification.value'].search([('short_name','=',vals['short_name'])])
            if valid:
                raise UserError(_('You can not use the duplicate short name.'))
        if 'product_category_id' in vals and vals['product_category_id'] and 'specification_id' in vals and vals['specification_id'] and 'name' in vals and vals['name']:
            valid = self.env['valid.specification.value'].search([('product_category_id','=',vals['product_category_id']),('specification_id','=',vals['specification_id']),('name','=',vals['name'])])
            if valid:
                raise UserError(_('You can not repeat the valid value for same specification.'))
        product_id =  super(valid_specification_value,self).write(vals)
        return product_id

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        if 'name' not in default:
            default['name'] = _("%s (copy)") % (self.name)
        if 'short_name' not in default:
            default['short_name'] = 'a'
        return super(valid_specification_value, self).copy(default=default)

    product_category_id = fields.Many2one('product.category','Product Category')
    specification_id = fields.Many2one('specification.line','Specification')
    name = fields.Char('Valid Value')
    short_name  = fields.Char('Short Name')
#     