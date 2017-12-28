# -*- coding: utf-8 -*-
{
    'name': "SCE Wechat Plugin",

    'summary': """
        SCE wechat plugin for work weixin""",

    'description': """
        Used for SCE wechat notification and approval.
    """,

    'author': "Jin Zan",
    'website': "http://www.sce-re.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sce_sso'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable' : True,
}
