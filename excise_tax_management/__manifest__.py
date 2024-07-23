{
    'name': 'Excise Tax',
    'version': '1.0',
    'author': 'Swapna',
    'summary': 'Excise Tax',
    'description': 'Excise Tax',
    'depends': ['purchase', 'web', 'account', 'account_accountant', 'base'],
    'data': [
        'views/purchase_order_line.xml',
        'views/account_move.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
