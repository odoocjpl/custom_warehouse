import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
import odoo.addons.decimal_precision as dp


class ProductCategory(models.Model):
    _inherit="product.category"
    
    @api.model
    def create(self,vals):
        seq_list = []
        att_list = []
        seq_list1 = []
        categ_list = []
        seq = ''
        att = ''
        categ = ' '
        seq1 = ' '
        name = ' '
        name_list = []
        count = 1
        product_categ_id =  super(ProductCategory,self).create(vals)
        categ_obj = self.env['product.category'].browse(product_categ_id)
        attribute = self.env['attribute.line'].search([('category_id1','=',categ_obj.id.id)])
        for val in attribute:
            attribute_obj = self.env['attribute.line'].browse(val.id)
            att_list.append(attribute_obj.attribute_id.id)
        if att_list:
            for val3 in att_list:
                att = val3
                count = 1
                for val4 in att_list:
                    if att == val4:
                        count = count + 1
                    else:
                        count = count
                if count != 2:
                    raise UserError(_('Attribute can not be repeat in Attribute for Grades'))    
        categ_template  = self.env['category.template'].search([('category_id1','=',categ_obj.id.id)])
        for val in categ_template:
            categ_template_obj = self.env['category.template'].browse(val.id)
            seq_list.append(categ_template_obj.seq_no)
            categ_list.append(categ_template_obj.category_id.id)
        if categ_list:
            for val3 in categ_list:
                categ = val3
                count = 1
                for val4 in categ_list:
                    if categ == val4:
                        count = count + 1
                    else:
                        count = count
                if count != 2:
                    raise UserError(_('Category can not be repeat in Category Template'))
        if seq_list:
            for val1 in seq_list:
                seq = val1
                count = 1
                for val2 in seq_list:
                    if seq == val2:
                        count = count + 1
                    else:
                        count = count
                if count != 2:
                    raise UserError(_('Sequence can not be repeat in Category Template'))
        spec_template = self.env['specification.line'].search([('category_id1','=',categ_obj.id.id)])
        for each in spec_template:
            spec_template_obj = self.env['specification.line'].browse(each.id)
            seq_list1.append(spec_template_obj.seq_no)
            name_list.append(spec_template_obj.name)
        if seq_list1:
            for each1 in seq_list1:
                seq1 = each1
                count = 1
                for each2 in seq_list1:
                    if seq1 == each2:
                        count = count + 1
                    else:
                        count = count
                if count != 2:
                    raise UserError(_('Sequence can not be repeat in Specifications'))
        if name_list:
            for each3 in name_list:
                name = each3
                count = 1
                for each4 in name_list:
                    if name == each4:
                        count = count + 1
                    else:
                        count = count
                if count != 2:
                    raise UserError(_('Name can not be repeat in Specifications'))
        return product_categ_id
     

    numbered = fields.Boolean('Numbered',track_visibility="onchange")
    can_altered = fields.Boolean('Can Be Altered',track_visibility="onchange")
    category_template_lines = fields.One2many('category.template','category_id1','Product Category',track_visibility="onchange")
    prefix = fields.Char('Prefix',track_visibility="onchange")
    specification_lines = fields.One2many('specification.line','category_id1','Specifications',track_visibility="onchange")       
    attribute_lines = fields.One2many('attribute.line','category_id1','Attribute Value',track_visibility="onchange")
    
class category_template(models.Model):
    _name="category.template"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    category_id = fields.Many2one('product.category','Category',track_visibility="onchange")
    seq_no = fields.Integer('Sequence No',track_visibility="onchange")
    part_name = fields.Boolean('Part of Name',track_visibility="onchange")
    mandatory = fields.Boolean('Mandatory',track_visibility="onchange")
    category_id1 = fields.Many2one('product.category','Category',track_visibility="onchange")
   
    
class specification_line(models.Model):
    _name="specification.line"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    seq_no = fields.Integer('Sequence No',track_visibility="onchange")
    name = fields.Char('Name',track_visibility="onchange")
    category_id1 = fields.Many2one('product.category','Category',required="1",track_visibility="onchange")
    
class attribute_line(models.Model):
    _name="attribute.line"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    attribute_id = fields.Many2one('product.attribute','Attribute',track_visibility="onchange")
    category_id1 = fields.Many2one('product.category','Category',required="1",track_visibility="onchange")
        