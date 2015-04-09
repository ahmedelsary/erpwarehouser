from openerp.osv import orm, fields
# encoding:UTF-8


class project_category(orm.Model):
    _name = 'project.category'
    _columns = {
        'name': fields.char('اﻻسم', size=30, required=True),
        'description': fields.text('الوصف'),
        'code': fields.integer('الكود', required=True),
        'subcategory_ids': fields.one2many('project.subcategory', 'category_id', 'اﻻقسام الفرعيه'),
    }


class project_subcategory(orm.Model):
    _name = 'project.subcategory'
    _columns = {
        'name': fields.char('اﻻسم', size=30, required=True),
        'description': fields.text('الوصف'),
        'code': fields.integer('الكود', required=True),
        'category_id': fields.many2one('project.category', ' اﻻقسام'),
        'subsubcategory_ids': fields.one2many('project.subsubcategory', 'subcategory_id', 'اﻻقسام تحت الفرعيه')

    }


