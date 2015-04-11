{
    'name': 'project',
    'version': '1.0',
    'summary': 'iti openerp project first version',
    'website': 'http://wwww.iti.gov.eg',
    'description': 'Basic example of  iti module',
    'auther': 'niven-ahmed-aya-tahany-fatma',
    'depends': ['base','report_webkit'],
    'data': [
        'project_view.xml',
        'project_workflow.xml',
        'security/iti_security.xml',
        'security/ir.model.access.csv',
        'report/product_max_min.xml',
    ],
    'installable': True,
    'auto_install': False,
}
