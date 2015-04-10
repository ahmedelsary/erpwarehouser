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
    
    
class project_subsubcategory(orm.Model):
    _name = 'project.subsubcategory'
    _columns = {
        'name': fields.char('اﻻسم', size=30),
        'description': fields.text('الوصف'),
        'code': fields.integer('الكود', required=True),
        'subcategory_id': fields.many2one('project.subcategory', 'اﻻقسام الفرعيه')

    }

class project_product(orm.Model):
    _name = 'project.product'

    # def _get_concatenate_values(self, cr, uid, ids, field_name, arg, context=None):
    # result = {}
    # products=self.browse(cr,uid,ids)
    # for product in products:
    # result[product.id] = str(product.catid)+str(product.subcat)+str(product.subsubcatid)+str(product.prod_id)


    # result = dict((x,'') for x in ids)
    # for r in records:
    # if(r.catid and r.subcat):
    #         result[r.id] = "%s %f" % \
    #                  (r.catid.name or '', r.subcat.name or 0.0)
    #                   # (r.field1.field1 or '', r.field2.field2 or 0.0)
    # return result
    def _get_concatenate_values(self, cr, uid, ids, name, arg, context=None):
        result = {}
        ids = self.search(cr, uid, [])
        product = self.browse(cr, uid, ids, context)
        #for product in products:
        #print self._columns['catid'].code
        result[product.prod_id] = str(product.code) + " " + str(product.catid.code) + " " + str(
            product.subcat.code) + " " + str(product.subsubcatid.code)
        return result
        # for product in products:
        # if (product.catid and product.subcat and product.subsubcatid):
        # result[product.prod_id] = str(product.code) + str(product.catid.code) + str( product.subcat.code) + str(product.subsubcatid.code)


    def _calc_salary(self, cr, uid, ids, name, arg, context):
        result = {}
        students = self.browse(cr, uid, ids, context)
        for student in students:
            student.code=long(str(student.catid.code)+ "" + str(
            student.subcat.code) + "" + str(student.subsubcatid.code)+str(student.id) )
            result[student.id] = student.code

        return result


    _columns = {
        'name': fields.char('اﻻسم'),
        'prod_id': fields.integer('Product_ID'),
        'price': fields.char('السعر'),

        'type': fields.char('النوع'),
        'company_name': fields.char('اسم الشركه'),
        'image': fields.binary('صورة'),
        'production_date': fields.date('تاريخ اﻻنتاج'),
        'expiry_date': fields.date('تاريخ اﻻنتهاء'),
        'catid': fields.many2one('project.category', 'القسم', required=True),
        'subcat': fields.many2one('project.subcategory', 'القسم الفرعى', required=True),
        'subsubcatid': fields.many2one('project.subsubcategory', 'القسم تحت الفرعى', required=True),
        'code': fields.function(_calc_salary, string='الكود'),
        'warehouse_id': fields.many2one("project.warehouse", "المخزن"),
        'min': fields.integer("اقل كميه موجوده"),
        'max': fields.integer("اكبر كميه موجوده "),
        'status': fields.selection(string="الحاله", selection=[
            ("new", "جديده"),
            ('used', "مستعمله"),
            ('damaged', 'هالكه'),
        ]),
        'state': fields.selection(string="الحاله", selection=[
            ('new', 'New'),
            ('recieved', 'Recieved'),
            ('underReview', 'Under Review'),
            ('approved', 'Approved'),
            ('keeperConfirm', 'Keeper Confirm'),
            ('managerConfirm', 'Manager Confirm'),
            ('inStock', 'In Stock'),
        ], readonly=True),
    }


    def product_new(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'new'})
        return True


    def product_recieved(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'recieved'})
        return True


    def product_underReview(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'underReview'})
        return True


    def product_approved(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'approved'})
        return True


    def product_keeper_confirm(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'keeperConfirm'})
        return True


    def product_manager_confirm(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'managerConfirm'})
        return True


    def product_in_stock(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'inStock'})
        return True

    


class project_warehouse(orm.Model):
    _name = 'project.warehouse'
    _columns = {
        'name': fields.char('اﻻسم', size=30, required=True),
        'address': fields.char('العنوان', size=100),
        # 'keeper_id':fields.many2one('hr','امين المخزن',select=True),
        # 'manager_id':fields.many2one('hr','مدير ',select=True),
        # 'supermanager_id':fields.many2one('hr','الرئيس',select=True ,domain="[('id','=','ref('ourwarehouse.group_iti_warehouse_supermanager')')]"),),
        'product_ids': fields.one2many('project.product', 'warehouse_id', string="المنتجات"),

    }
