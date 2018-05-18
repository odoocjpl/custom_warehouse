import logging

from odoo import api, fields, models
from odoo import tools, _
import time
import math
import odoo.addons.decimal_precision as dp
from datetime import datetime,timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT,DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError
from odoo.modules.module import get_module_resource


class wiz_add_product(models.TransientModel):
    _name="wiz.add.product"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.model
    def create(self,vals):
        prefix =  ''
        short_name = ''
        long_name = ''
        category_id = ''
        categ_list = []
        categ_list1 = []
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
                    prefix = category_obj.prefix + prefix
            else:
                category_id = ''
                if prefix == '':
                    prefix = category_obj.prefix
                else:
                    prefix = category_obj.prefix + prefix
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
        if vals.get('category_id1'):
            category_id = vals.get('category_id1')
        if vals.get('category_template_lines'):
            product_list = self.env['category.template.line'].search([('wiz_add_product_id','=',product_obj.id)])
            for each1 in product_list:
                categ_list.append(each1.seq_no)
            if categ_list:
                categ_list1 = sorted(categ_list)
            if categ_list1:
                for val in categ_list1:
                    prod_list = self.env['category.template.line'].search([('wiz_add_product_id','=',product_obj.id),('seq_no','=',val),('part_name','=',True)])
                    if prod_list:
                        for val1 in prod_list:
                            if val1.product_id.short_name_product:
                                if short_name == '':
                                    short_name = val1.product_id.short_name_product
                                else:
                                    short_name = short_name + '-' + val1.product_id.short_name_product
                    prod_list1 = self.env['category.template.line'].search([('wiz_add_product_id','=',product_obj.id),('seq_no','=',val)])
                    if prod_list1:
                        for val2 in prod_list1:
                            if val2.product_id.short_name_product:
                                if long_name == '':
                                    long_name = val2.product_id.short_name_product
                                else:
                                    long_name = long_name + '-' + val2.product_id.short_name_product
            product_obj.write({'short_name':short_name,'long_name':long_name})
        return product_id
     
    @api.multi
    def write(self,vals):
        short_name = ''
        long_name = ''
        category_id = ''
        prefix = ''
        categ_list = []
        catreg_list1 = []
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
                    prefix = category_obj.prefix + prefix
            else:
                category_id = ''
                if prefix == '':
                    prefix = category_obj.prefix
                else:
                    prefix = category_obj.prefix + prefix
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
        if 'category_id1' in vals and vals['category_id1']:
             category_id = vals['category_id1']
        if 'category_template_lines' in vals and vals['category_template_lines']:
            product_list = self.env['category.template.line'].search([('wiz_add_product_id','=',product_obj.id)])
            for each1 in product_list:
                categ_list.append(each1.seq_no)
            if categ_list:
                categ_list1 = sorted(categ_list)
            if categ_list1:
                for val in categ_list1:
                    prod_list = self.env['category.template.line'].search([('wiz_add_product_id','=',product_obj.id),('seq_no','=',val),('part_name','=',True)])
                    if prod_list:
                        for val1 in prod_list:
                            if val1.product_id.short_name_product:
                                if short_name == '':
                                    short_name = val1.product_id.short_name_product
                                else:
                                    short_name = short_name + '-' +val1.product_id.short_name_product
                    prod_list1 = self.env['category.template.line'].search([('wiz_add_product_id','=',product_obj.id),('seq_no','=',val)])
                    if prod_list1:
                        for val2 in prod_list1:
                            if val2.product_id.short_name_product:
                                if long_name == '':
                                    long_name = val2.product_id.short_name_product
                                else:
                                    long_name = long_name + '-' + val2.product_id.short_name_product
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
                prod1 = self.env['product.template'].search([('name','=',each.short_name)])
                if prod1:
                    raise UserError(_('Product with the same name alrady exist'))
                elif product_obj.category_id:
                    if product_obj.category_id.numbered == True:
                        product_data = {
                                        'name':each.short_name,
                                        'long_name':each.long_name,
                                        'short_name':each.short_name,
                                        'categ_id':each.category_id.id,
                                        'tracking':'serial',
                                        'type':'product'
                                        }
                    else:
                        product_data = {
                                        'name':each.short_name,
                                        'long_name':each.long_name,
                                        'short_name':each.short_name,
                                        'categ_id':each.category_id.id,
                                        'tracking':'none',
                                        'type':'product'
                                        }
                elif product_obj.category_id1:
                    if product_obj.category_id1.numbered == True:
                        product_data = {
                                        'name':each.short_name,
                                        'long_name':each.long_name,
                                        'short_name':each.short_name,
                                        'categ_id':each.category_id1.id,
                                        'tracking':'serial',
                                        'type':'product'
                                        }
                    else:
                        product_data = {
                                        'name':each.short_name,
                                        'long_name':each.long_name,
                                        'short_name':each.short_name,
                                        'categ_id':each.category_id1.id,
                                        'tracking':'none',
                                        'type':'product'
                                        }
        prod_id = prod_obj.create(product_data)
        value_list = [ ]
        if prod1:
            for each in prod1:
                prod1_obj = self.env['product.product'].browse(each.id)
        if product_obj.category_id.attribute_lines:
            for each in product_obj.category_id.attribute_lines:
                value_list = []
                attribute_list = self.env['product.attribute.value'].search([('attribute_id','=',each.attribute_id.id)])
                for each1 in attribute_list:
                    value_list.append(each1.id)
                self.env['product.attribute.line'].create({'product_tmpl_id':prod_id.id,'attribute_id':each.attribute_id.id,'value_ids':[(6,0,value_list)]})
                prod_id.create_variant_ids()
        elif product_obj.category_id1.attribute_lines:
            for each in product_obj.category_id1.attribute_lines:
                value_list = []
                attribute_list = self.env['product.attribute.value'].search([('attribute_id','=',each.attribute_id.id)])
                for each1 in attribute_list:
                    value_list.append(each1.id)
                self.env['product.attribute.line'].create({'product_tmpl_id':prod_id.id,'attribute_id':each.attribute_id.id,'value_ids':[(6,0,value_list)]})
                prod_id.create_variant_ids()
        if prod_id:
            self.write({'state':'product_created'})  
        return prod_id
              
    @api.onchange('category_id')
    def _onchange_category_id(self):
        bom_list = []
        if self.category_id:
            if self.name == 'non-altered':
                if self.category_id.numbered == True:
                    self.numbered = True
                if self.category_id.specification_lines:
                    for val in self.category_id.specification_lines:
                         bom_list.append((0,False,{'category_id':self.category_id,'seq_no':val.seq_no,'specification':val.name}))
                self.add_product_lines = bom_list
    
    @api.onchange('category_id1')
    def _onchange_category_id1(self):
        bom_list = []
        if self.category_id1:
            if self.name == 'altered':
                if self.category_id1.numbered == True:
                    self.numbered = True
                if self.category_id1.category_template_lines:
                    for val in self.category_id1.category_template_lines:
                         bom_list.append((0,False,{'category_id':val.category_id,'seq_no':val.seq_no,'part_name':val.part_name,
                                                   'mandatory':val.mandatory}))
                self.category_template_lines = bom_list
    name = fields.Selection([('altered','Altered'),('non-altered','Non-Altered')],'Category Type',default='non-altered',track_visibility="onchange")
    category_id = fields.Many2one('product.category','Product Category',track_visibility="onchange")
    numbered = fields.Boolean('Numbered',track_visibility="onchange")
    category_id1 = fields.Many2one('product.category','Product Category',track_visibility="onchange") 
    add_product_lines  = fields.One2many('add.product.line','wiz_add_product_id','Add Product',track_visibility="onchange")
    short_name = fields.Char('Short Name',track_visibility="onchange")
    long_name = fields.Char('Long Name',track_visibility="onchange")
    date = fields.Date('Date',default=lambda *a: datetime.now(),track_visibility="onchange")
    created_by = fields.Many2one('res.users','Created By',readonly=True,default=lambda self: self.env.user,track_visibility="onchange")
    state = fields.Selection([('draft','Draft'),('product_created','Product Created')],'State',default="draft",track_visibility="onchange")
    category_template_lines = fields.One2many('category.template.line','wiz_add_product_id','Add Category',track_visibility="onchange")
    
class add_product_line(models.TransientModel):
    _name="add.product.line"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    @api.onchange('valid_value')
    def _onchange_valid_value(self):
        short_name = ''
        if self.valid_value:
            valid = self.env['valid.specification.value'].browse(self.valid_value.id)
            self.short_name = valid.short_name
            
    wiz_add_product_id = fields.Many2one('wiz.add.product','Add Product',track_viisbility="onchange")
    seq_no = fields.Integer('Seq No',track_visibility="onchange")
    specification_id = fields.Many2one('specification.line','Specifications',track_visibility="onchange")
    specification = fields.Char('Specification',track_visibility="onchange")
    short_name = fields.Char('Short Name',track_visibility="onchange")
    category_id = fields.Many2one('product.category','Product Category',track_visibility="onchange")
    valid_value = fields.Many2one('valid.specification.value','Valid Value',track_visibility="onchange")

class category_template_line(models.TransientModel):
    _name="category.template.line"
    _inherit = ['mail.thread', 'ir.needaction_mixin']  
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        bom_list = []
        if self.product_id:
            self.short_name = self.product_id.short_name_product
           
#     
    wiz_add_product_id = fields.Many2one('wiz.add.product','Add Product',track_visibility="onchange")
    category_id = fields.Many2one('product.category','Category',track_visibility="onchange")
    seq_no = fields.Integer('Sequence No',track_visibility="onchange")
    short_name = fields.Char('Short Name for Product',track_visibility="onchange")
    part_name = fields.Boolean('Part of Name',track_visibility="onchange")
    mandatory = fields.Boolean('Mandatory',track_visibility="onchange")
    product_id = fields.Many2one('product.product','Product',track_visibility="onchange")
