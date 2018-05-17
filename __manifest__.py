{
    "name": "Warehouse Custom",
    "version": "1.0",
    'website': 'http://www.diracerp.in',
    'images': [ ],
    "depends": ['web','base','product','stock'],
    "author": "Dirac ERP",
    "category": "Stock",
#     'sequence': 16,
    "description": """
    This module is for CJPL warehouse functionalities. 
    """,
    'data': [
            'view/product_category_view.xml',
            'view/valid_specification_value_view.xml',
            'wizard/wiz_add_product_view.xml',
            'view/product_view.xml',
                    ],
    'demo_xml': [],
     'js': [
            'static/src/js/view_list.js'
#            'static/src/js/view_list.js'
#     'static/src/js/subst.js'
    ],
    'css': [
#             'static/src/css/sample_kanban.css'
            ],
    'installable': True,
    'active': False,
    'auto_install': False,
#    'certificate': 'certificate',
}