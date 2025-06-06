
{
    'name': 'CRM Custom Follow-Up Flow',
    'version': '16.0.1.0.2',
    'category': 'Sales/CRM',
    'summary': 'Custom CRM workflow with follow-up stages and transitions',
    'description': """
        Implements a custom CRM workflow with:
        - Prospect to Follow-Up stages
        - 7 Follow-Up levels
        - Automatic stage transitions
        - SALE stage after confirming interest
    """,
    'author': 'Vismaya B',
    'depends': ['crm'],
    'data': [
        'data/crm_stages.xml',
        'data/stage_cron.xml',
        'views/crm_lead_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

