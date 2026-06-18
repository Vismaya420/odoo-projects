
{
    'name': 'Purchase Rentals',
    'version': '18.0.1.0.0',
    'summary': 'Manage rental-based purchases',
    'category': 'Purchase',
    'depends': ['purchase', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/purchase_rental_views.xml',
        'views/account_move_views.xml',
        'views/menu.xml',
        'report/report.xml',
        'report/purchase_rental_template.xml',
        
        
        
    ],
    
    'installable': True,
    'application': True,
}
