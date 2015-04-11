from openerp.osv import orm, fields
# encoding:UTF-8


class project_category(orm.Model):
    _name = 'project.category'
    _columns = {
        'name': fields.char('اﻻسم', size=30, required=True),
        'description': fields.text('الوصف'),
        'subcategory_ids': fields.one2many('project.subcategory', 'category_id', 'اﻻقسام الفرعيه'),
    }


class project_subcategory(orm.Model):
    _name = 'project.subcategory'
    _columns = {
        'name': fields.char('اﻻسم', size=30, required=True),
        'description': fields.text('الوصف'),
        'category_id': fields.many2one('project.category', ' اﻻقسام'),
        'subsubcategory_ids': fields.one2many('project.subsubcategory', 'subcategory_id', 'اﻻقسام تحت الفرعيه')

    }


class project_subsubcategory(orm.Model):
    _name = 'project.subsubcategory'
    _columns = {
        'name': fields.char('اﻻسم', size=30),
        'description': fields.text('الوصف'),
        'subcategory_id': fields.many2one('project.subcategory', 'اﻻقسام الفرعيه')

    }


class project_product(orm.Model):
    _name = 'project.product'

    def _calc_salary(self, cr, uid, ids, name, arg, context):
        result = {}
        products = self.browse(cr, uid, ids, context)
        for product in products:
            product.code = (
                (" %02d" % product.subsubcatid.subcategory_id.category_id.id) + "" + "%02d" % product.subsubcatid.subcategory_id.id
                + "" + "%02d" % product.subsubcatid.id + "%02d" % product.id)
            result[product.id] = product.code

        return result

    def check_keeper(self, cr, uid, ids, name, arg, context):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            keeper_id = product.warehouse_id.keeper_id.id
            if keeper_id == uid:
                res[product.id] = True
            else:
                res[product.id] = False
        return res


    def check_commit(self, cr, uid, ids, name, arg, context):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            commit1_id = product.warehouse_id.commit1_id.id
            commit2_id = product.warehouse_id.commit2_id.id
            commit3_id = product.warehouse_id.commit3_id.id
            if (commit1_id == uid ) or (commit2_id == uid ) or (commit3_id == uid ):
                res[product.id] = True
            else:
                res[product.id] = False
        return res

    def check_manger(self, cr, uid, ids, name, arg, context):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            manger_id = product.warehouse_id.manager_id.id
            if manger_id == uid:
                res[product.id] = True
            else:
                res[product.id] = False
        return res

    def check_supermanger(self, cr, uid, ids, name, arg, context):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            supermanger_id = product.warehouse_id.supermanager_id.id
            if supermanger_id == uid:
                res[product.id] = True
            else:
                res[product.id] = False
        return res

    _columns = {
        'name': fields.char('اسم '),
        'type': fields.char('النوع'),
        'company_name': fields.char('اسم الشركه'),
        'image': fields.binary('صورة'),
        'quantity': fields.integer("الكميه"),
        'price': fields.char('السعر'),
        'production_date': fields.date('تاريخ اﻻنتاج'),
        'expiry_date': fields.date('تاريخ اﻻنتهاء'),
        'subsubcatid': fields.many2one('project.subsubcategory', 'القسم تحت الفرعى', required=True),
        'code': fields.function(_calc_salary, method=True, type='string', string='الكود'),
        'warehouse_id': fields.many2one("project.warehouse", "المخزن", required=True),
        'min': fields.integer("اقل كميه "),
        'max': fields.integer("اكبر كميه  "),
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
        'is_keeper': fields.function(check_keeper, type='boolean', store=False),
        'is_commit': fields.function(check_commit, type='boolean', store=False),
        'is_manger': fields.function(check_manger, type='boolean', store=False),
        'is_supermanger': fields.function(check_supermanger, type='boolean', store=False),


    }
    _defaults = {
        'state': 'new',
        'min': 500,
        'max': 50000,
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
        'product_ids': fields.one2many('project.product', 'warehouse_id', string="المنتجات"),
        'keeper_id': fields.many2one('res.users', 'امين المخزن', select=True, required=True),
        'manager_id': fields.many2one('res.users', 'مدير ', select=True, required=True),
        'supermanager_id': fields.many2one('res.users', 'الرئيس', select=True, required=True),
        'commit1_id': fields.many2one('res.users', 'عضولجنه', select=True, required=True),
        'commit2_id': fields.many2one('res.users', 'عضولجنه', select=True, required=True),
        'commit3_id': fields.many2one('res.users', 'عضولجنه', select=True, required=True),

    }


class project_el3hda(orm.Model):
    t = [('request', 'طلب'), ('return', 'ارجاع')]
    _name = "project.el3hda"
    _columns = {
        'name': fields.char("الاسم", size=265),
        'type': fields.selection(t, "النوع"),
        'user_id': fields.many2one("res.users", "المستخدم"),
        'state': fields.selection(string="الحاله", selection=[
            ('draft', 'Draft'),
            ('managerConfirm', 'Manager Confirm'),
            ('warehouseConfirm', 'Warehouse Manger Confirm'),
            ('done', 'Done'),
        ], readonly=True),

    }
    _defaults = {
        'state': 'draft',
        # 'user_id': lambda self, cr, uid, c: self.pool.get('res.users').browse(cr, uid, uid, c)[0],
    }

    def product_draft(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'draft'})
        return True

    def product_managerConfirm(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'managerConfirm'})
        return True

    def product_warehouseConfirm(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'warehouseConfirm'})
        return True

    def product_done(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'done'})
        return True


class project_employees(orm.Model):
    gender = [('f', 'female'), ('m', 'male')]
    _name = 'project.employees'
    _columns = {
        'name': fields.char('Name'),
        'age': fields.integer('Age'),
        'salary': fields.integer('Salary'),
        'gender': fields.selection(gender, 'Gender'),
        'pic': fields.binary('Image', widget='Image'),
        "manger_id": fields.many2one("project.employees", "Manger"),
        'warehouse_id': fields.many2one('project.warehouse', 'Warehouse'),
        'user_system': fields.many2one("res.users", "User System"),

    }
