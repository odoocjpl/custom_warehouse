import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
import odoo.addons.decimal_precision as dp


class wiz_add_product(models.TransientModel):
    _name="wiz.add.product"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.model
    def create(self,vals):
        prefix =  ''
        short_name = ''
        long_name = ''
        category_id = ''
        product_id =  super(wiz_add_product,self).create(vals)
        product_obj = self.env['wiz.add.product'].browse(product_id.id)
        if vals.get('category_id'):
            category_id = vals.get('category_id')
        while(category_id != ''):
            category_obj = self.env['product.category'].browse(category_id)
            if category_obj.parent_id:
                category_id = category_obj.parent_id.id
                if prefix == '':
                    prefix = category_obj.prefix
                else:
                    prefix = prefix + category_obj.prefix
            else:
                category_id = ''
                if prefix == '':
                    prefix = category_obj.prefix
                else:
                    prefix = prefix + category_obj.prefix
        if prefix == '':
            short_name = ''
        else:
            short_name = prefix
        if vals.get('add_product_lines'):
            product_list = self.env['add.product.line'].search([('wiz_add_product_id','=',product_obj.id)])
            for each1 in product_list:
                
                if each1.short_name:
                    if short_name == '':
                        short_name = each1.short_name
                    else:
                        short_name = short_name + each1.short_name
                else:
                    short_name = short_name
                if each1.valid_value:
                    if long_name == '':
                        long_name = each1.valid_value.name
                            
                    else:
                        long_name = long_name + '-' + each1.valid_value.name
                else:
                    long_name = long_name
        product_obj.write({'short_name':short_name,'long_name':long_name})
        return product_id
     
    @api.multi
    def write(self,vals):
        short_name = ''
        long_name = ''
        category_id = ''
        prefix = ''
        product_obj = self.env['wiz.add.product'].browse(self.id)
        product_id =  super(wiz_add_product,self).write(vals)
        if 'category_id' in vals and vals['category_id']:
             category_id = vals['category_id']
        while(category_id != ''):
            category_obj = self.env['product.category'].browse(category_id)
            if category_obj.parent_id:
                category_id = category_obj.parent_id.id
                if prefix == '':
                    prefix = category_obj.prefix
                else:
                    prefix = prefix + category_obj.prefix
            else:
                category_id = ''
                if prefix == '':
                    prefix = category_obj.prefix
                else:
                    prefix = prefix + category_obj.prefix
        if prefix == '':
            short_name = ''
        else:
            short_name = prefix
        if 'add_product_lines' in vals and vals['add_product_lines']:
            product_list = self.env['add.product.line'].search([('wiz_add_product_id','=',product_obj.id)])
            for each1 in product_list:
                
                if each1.short_name:
                    if short_name == '':
                        short_name = each1.short_name
                    else:
                        short_name = short_name + each1.short_name
                else:
                    short_name = short_name
                if each1.valid_value:
                    if long_name == '':
                        long_name = each1.valid_value.name
                            
                    else:
                        long_name = long_name + '-' + each1.valid_value.name
                else:
                    long_name = long_name
            product_obj.write({'short_name':short_name,'long_name':long_name})
        return product_id
    

    def create_product(self,ids,context=None):
        if context is None:
            context = {}
        product_data = {}
        product_obj = self.env['wiz.add.product'].browse(self.id)
        prod_obj = self.env['product.template']
        for each in self:
            if each.short_name:
                product_data = {
                                'name':each.short_name,
                                'long_name':each.long_name,
                                'short_name':each.short_name,
                                'categ_id':each.category_id.id,
                                }
        prod_id = prod_obj.create(product_data)
        if prod_id:
            self.write({'code1':True})
        view_ref = self.env['ir.model.data'].get_object_reference('warehouse_custom', 'product_template_only_form_view_inherit')
        view_id = view_ref and view_ref[1] or False,
        return {
            'name':'Products',
            'view_type':'form',
            'view_mode':'tree',
            'views' : [(view_id,'form')],
            'res_model':'product.template',
            'view_id':view_id,
            'type':'ir.actions.act_window',
            'res_id':prod_id.id,
            'target':'current',
            'context':"{}",
        }    
              

     
    @api.onchange('category_id')
    def _onchange_category_id(self):
        bom_list = []
        if self.category_id:
            if self.category_id.specification_lines:
                for val in self.category_id.specification_lines:
                     bom_list.append((0,False,{'category_id':self.category_id,'seq_no':val.seq_no,'specification':val.name}))
            self.add_product_lines = bom_list
            
    name = fields.Selection([('numbered','Numbered'),('non-numbered','Non-Numbered')],'Category Type',default='non-numbered')
    category_id = fields.Many2one('product.category','Product Category')
    category_id1 = fields.Many2one('product.category','Product Category') 
    add_product_lines  = fields.One2many('add.product.line','wiz_add_product_id','Add Product')
    short_name = fields.Char('Short Name')
    long_name = fields.Char('Long Name')
    code = fields.Boolean('Code')
    code1 = fields.Boolean('Code')
    
class add_product_line(models.TransientModel):
    _name="add.product.line"
    
    @api.onchange('valid_value')
    def _onchange_valid_value(self):
        short_name = ''
        if self.valid_value:
            valid = self.env['valid.specification.value'].browse(self.valid_value.id)
            self.short_name = valid.short_name
            
    
    wiz_add_product_id = fields.Many2one('wiz.add.product','Add Product')
    seq_no = fields.Integer('Seq No')
    specification_id = fields.Many2one('specification.line','Specifications')
    specification = fields.Char('Specification')
    short_name = fields.Char('Short Name')
    category_id = fields.Many2one('product.category','Product Category')
    valid_value = fields.Many2one('valid.specification.value','Valid Value')
