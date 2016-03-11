##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, osv
from tools.translate import _

from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from operator import itemgetter
from itertools import groupby

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import netsvc
from openerp import tools
from openerp.tools import float_compare, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class hr_bonus(osv.osv):
    def on_change_emp_id(self, cursor, uid, ids, emp_id, context=None):

        cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        department_id = row[0]
        cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        job_id = row[0]

        cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        employee_id = row[0]

        return {'value': {'position':job_id,'department':department_id,'employee_id':str(employee_id)}}


    def _get_name(self, cursor, user, ids, name, arg, context):
        print arg
        current_id = ids[0]
        cursor.execute("""SELECT emp_id FROM hr_bonus WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]

        if arg==1:
            cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            department_id = row[0]
            print department_id
            return {current_id:department_id}
        if arg==2:
            cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            job_id = row[0]
            print job_id
            return {current_id:job_id}
        if arg==3:
            cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            employee_id = row[0]
            print employee_id
            return {current_id:str(employee_id)}

    _name = "hr.bonus"
    _columns = {

        'emp_id':fields.many2one('hr.employee', 'Employee', required=True,),
        'date':fields.date('Date',required=True,),
        'amount':fields.float('Amount',digits=(20,2),required=True,),
        'department': fields.function(_get_name,arg=1,type='many2one',obj='hr.department',string='Department',),
        'position': fields.function(_get_name,arg=2,type='many2one',obj='hr.job',string='Position',),
        'employee_id': fields.function(_get_name,arg=3,type="char",string='Employee PIN',),
    }
hr_bonus()

class hr_special_allowance(osv.osv):
    def on_change_emp_id(self, cursor, uid, ids, emp_id, context=None):

        cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        department_id = row[0]
        cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        job_id = row[0]

        cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        employee_id = row[0]

        return {'value': {'position':job_id,'department':department_id,'employee_id':str(employee_id)}}


    def _get_name(self, cursor, user, ids, name, arg, context):
        print arg
        current_id = ids[0]
        cursor.execute("""SELECT emp_id FROM hr_special_allowance WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]

        if arg==1:
            cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            department_id = row[0]
            print department_id
            return {current_id:department_id}
        if arg==2:
            cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            job_id = row[0]
            print job_id
            return {current_id:job_id}
        if arg==3:
            cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            employee_id = row[0]
            print employee_id
            return {current_id:str(employee_id)}

    _name = "hr.special.allowance"
    _columns = {

        'emp_id':fields.many2one('hr.employee', 'Employee', required=True,),
        'date':fields.date('Date',required=True,),
        'amount':fields.float('Amount',digits=(20,2),required=True,),
        'department': fields.function(_get_name,arg=1,type='many2one',obj='hr.department',string='Department',),
        'position': fields.function(_get_name,arg=2,type='many2one',obj='hr.job',string='Position',),
        'employee_id': fields.function(_get_name,arg=3,type="char",string='Employee PIN',),

    }
hr_special_allowance()
class hr_arrear_salary(osv.osv):
    def on_change_emp_id(self, cursor, uid, ids, emp_id, context=None):

        cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        department_id = row[0]
        cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        job_id = row[0]

        cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        employee_id = row[0]

        return {'value': {'position':job_id,'department':department_id,'employee_id':str(employee_id)}}


    def _get_name(self, cursor, user, ids, name, arg, context):
        print arg
        current_id = ids[0]
        cursor.execute("""SELECT emp_id FROM hr_arrear_salary WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]

        if arg==1:
            cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            department_id = row[0]
            print department_id
            return {current_id:department_id}
        if arg==2:
            cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            job_id = row[0]
            print job_id
            return {current_id:job_id}
        if arg==3:
            cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            employee_id = row[0]
            print employee_id
            return {current_id:str(employee_id)}

    _name = "hr.arrear.salary"
    _columns = {

        'emp_id':fields.many2one('hr.employee', 'Employee', required=True,),
        'date':fields.date('Date',required=True,),
        'amount':fields.float('Amount',digits=(20,2),required=True,),
        'department': fields.function(_get_name,arg=1,type='many2one',obj='hr.department',string='Department',),
        'position': fields.function(_get_name,arg=2,type='many2one',obj='hr.job',string='Position',),
        'employee_id': fields.function(_get_name,arg=3,type="char",string='Employee PIN',),
        'arrear_type': fields.selection([
            ('absent', 'Absent'),
            ('bonus', 'Bonus'),
            ('increment', 'Increment')
            ], 'Arrear Type',)
    }
hr_arrear_salary()
class hr_other_earnings(osv.osv):
    def on_change_emp_id(self, cursor, uid, ids, emp_id, context=None):

        cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        department_id = row[0]
        cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        job_id = row[0]

        cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        employee_id = row[0]

        return {'value': {'position':job_id,'department':department_id,'employee_id':str(employee_id)}}


    def _get_name(self, cursor, user, ids, name, arg, context):
        print arg
        current_id = ids[0]
        cursor.execute("""SELECT emp_id FROM hr_other_earnings WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]

        if arg==1:
            cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            department_id = row[0]
            print department_id
            return {current_id:department_id}
        if arg==2:
            cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            job_id = row[0]
            print job_id
            return {current_id:job_id}
        if arg==3:
            cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            employee_id = row[0]
            print employee_id
            return {current_id:str(employee_id)}

    _name = "hr.other.earnings"
    _columns = {

        'emp_id':fields.many2one('hr.employee', 'Employee', required=True,),
        'date':fields.date('Date',required=True,),
        'amount':fields.float('Amount',digits=(20,2),required=True,),
        'department': fields.function(_get_name,arg=1,type='many2one',obj='hr.department',string='Department',),
        'position': fields.function(_get_name,arg=2,type='many2one',obj='hr.job',string='Position',),
        'employee_id': fields.function(_get_name,arg=3,type="char",string='Employee PIN',),

    }
hr_other_earnings()
class hr_absent_deduction(osv.osv):
    def on_change_emp_id(self, cursor, uid, ids, emp_id, context=None):

        cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        department_id = row[0]
        cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        job_id = row[0]

        cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        employee_id = row[0]

        return {'value': {'position':job_id,'department':department_id,'employee_id':str(employee_id)}}


    def _get_name(self, cursor, user, ids, name, arg, context):
        print arg
        current_id = ids[0]
        cursor.execute("""SELECT emp_id FROM hr_absent_deduction WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]

        if arg==1:
            cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            department_id = row[0]
            print department_id
            return {current_id:department_id}
        if arg==2:
            cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            job_id = row[0]
            print job_id
            return {current_id:job_id}
        if arg==3:
            cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            employee_id = row[0]
            print employee_id
            return {current_id:str(employee_id)}

    _name = "hr.absent.deduction"
    _columns = {

        'emp_id':fields.many2one('hr.employee', 'Employee', required=True,),
        'date':fields.date('Date',required=True,),
        'amount':fields.float('Amount',digits=(20,2),required=True,),
        'department': fields.function(_get_name,arg=1,type='many2one',obj='hr.department',string='Department',),
        'position': fields.function(_get_name,arg=2,type='many2one',obj='hr.job',string='Position',),
        'employee_id': fields.function(_get_name,arg=3,type="char",string='Employee PIN',),

    }
hr_absent_deduction()
class hr_pf_deduction(osv.osv):
    def on_change_emp_id(self, cursor, uid, ids, emp_id, context=None):

        cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        department_id = row[0]
        cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        job_id = row[0]

        cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        employee_id = row[0]

        return {'value': {'position':job_id,'department':department_id,'employee_id':str(employee_id)}}


    def _get_name(self, cursor, user, ids, name, arg, context):
        print arg
        current_id = ids[0]
        cursor.execute("""SELECT emp_id FROM hr_pf_deduction WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]

        if arg==1:
            cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            department_id = row[0]
            print department_id
            return {current_id:department_id}
        if arg==2:
            cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            job_id = row[0]
            print job_id
            return {current_id:job_id}
        if arg==3:
            cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            employee_id = row[0]
            print employee_id
            return {current_id:str(employee_id)}

    _name = "hr.pf.deduction"
    _columns = {

        'emp_id':fields.many2one('hr.employee', 'Employee', required=True,),
        'date':fields.date('Date',required=True,),
        'amount':fields.float('Amount',digits=(20,2),required=True,),
        'department': fields.function(_get_name,arg=1,type='many2one',obj='hr.department',string='Department',),
        'position': fields.function(_get_name,arg=2,type='many2one',obj='hr.job',string='Position',),
        'employee_id': fields.function(_get_name,arg=3,type="char",string='Employee PIN',),

    }
hr_pf_deduction()
class hr_advance_salary(osv.osv):
    def on_change_emp_id(self, cursor, uid, ids, emp_id, context=None):

        cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        department_id = row[0]
        cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        job_id = row[0]

        cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        employee_id = row[0]

        return {'value': {'position':job_id,'department':department_id,'employee_id':str(employee_id)}}


    def _get_name(self, cursor, user, ids, name, arg, context):
        print arg
        current_id = ids[0]
        cursor.execute("""SELECT emp_id FROM hr_advance_salary WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]

        if arg==1:
            cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            department_id = row[0]
            print department_id
            return {current_id:department_id}
        if arg==2:
            cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            job_id = row[0]
            print job_id
            return {current_id:job_id}
        if arg==3:
            cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            employee_id = row[0]
            print employee_id
            return {current_id:str(employee_id)}

    _name = "hr.advance.salary"
    _columns = {

        'emp_id':fields.many2one('hr.employee', 'Employee', required=True,),
        'date':fields.date('Date',required=True,),
        'amount':fields.float('Amount',digits=(20,2),required=True,),
        'department': fields.function(_get_name,arg=1,type='many2one',obj='hr.department',string='Department',),
        'position': fields.function(_get_name,arg=2,type='many2one',obj='hr.job',string='Position',),
        'employee_id': fields.function(_get_name,arg=3,type="char",string='Employee PIN',),

    }
hr_advance_salary()
class hr_mobile_bill(osv.osv):
    def on_change_emp_id(self, cursor, uid, ids, emp_id, context=None):

        cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        department_id = row[0]
        cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        job_id = row[0]

        cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        employee_id = row[0]

        return {'value': {'position':job_id,'department':department_id,'employee_id':str(employee_id)}}


    def _get_name(self, cursor, user, ids, name, arg, context):
        print arg
        current_id = ids[0]
        cursor.execute("""SELECT emp_id FROM hr_mobile_bill WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]

        if arg==1:
            cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            department_id = row[0]
            print department_id
            return {current_id:department_id}
        if arg==2:
            cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            job_id = row[0]
            print job_id
            return {current_id:job_id}
        if arg==3:
            cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            employee_id = row[0]
            print employee_id
            return {current_id:str(employee_id)}

    _name = "hr.mobile.bill"
    _columns = {

        'emp_id':fields.many2one('hr.employee', 'Employee', required=True,),
        'date':fields.date('Date',required=True,),
        'amount':fields.float('Amount',digits=(20,2),required=True,),
        'department': fields.function(_get_name,arg=1,type='many2one',obj='hr.department',string='Department',),
        'position': fields.function(_get_name,arg=2,type='many2one',obj='hr.job',string='Position',),
        'employee_id': fields.function(_get_name,arg=3,type="char",string='Employee PIN',),

    }
hr_mobile_bill()
class hr_revenue_stamp(osv.osv):
    def on_change_emp_id(self, cursor, uid, ids, emp_id, context=None):

        cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        department_id = row[0]
        cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        job_id = row[0]

        cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        employee_id = row[0]

        return {'value': {'position':job_id,'department':department_id,'employee_id':str(employee_id)}}


    def _get_name(self, cursor, user, ids, name, arg, context):
        print arg
        current_id = ids[0]
        cursor.execute("""SELECT emp_id FROM hr_revenue_stamp WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]

        if arg==1:
            cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            department_id = row[0]
            print department_id
            return {current_id:department_id}
        if arg==2:
            cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            job_id = row[0]
            print job_id
            return {current_id:job_id}
        if arg==3:
            cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            employee_id = row[0]
            print employee_id
            return {current_id:str(employee_id)}

    _name = "hr.revenue.stamp"
    _columns = {

        'emp_id':fields.many2one('hr.employee', 'Employee', required=True,),
        'date':fields.date('Date',required=True,),
        'amount':fields.float('Amount',digits=(20,2),required=True,),
        'department': fields.function(_get_name,arg=1,type='many2one',obj='hr.department',string='Department',),
        'position': fields.function(_get_name,arg=2,type='many2one',obj='hr.job',string='Position',),
        'employee_id': fields.function(_get_name,arg=3,type="char",string='Employee PIN',),

    }
hr_revenue_stamp()

class hr_other_deduction(osv.osv):
    def on_change_emp_id(self, cursor, uid, ids, emp_id, context=None):

        cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        department_id = row[0]
        cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        job_id = row[0]

        cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        employee_id = row[0]

        return {'value': {'position':job_id,'department':department_id,'employee_id':str(employee_id)}}


    def _get_name(self, cursor, user, ids, name, arg, context):
        print arg
        current_id = ids[0]
        cursor.execute("""SELECT emp_id FROM hr_other_deduction WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]

        if arg==1:
            cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            department_id = row[0]
            print department_id
            return {current_id:department_id}
        if arg==2:
            cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            job_id = row[0]
            print job_id
            return {current_id:job_id}
        if arg==3:
            cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            employee_id = row[0]
            print employee_id
            return {current_id:str(employee_id)}

    _name = "hr.other.deduction"
    _columns = {

        'emp_id':fields.many2one('hr.employee', 'Employee', required=True,),
        'date':fields.date('Date',required=True,),
        'amount':fields.float('Amount',digits=(20,2),required=True,),
        'department': fields.function(_get_name,arg=1,type='many2one',obj='hr.department',string='Department',),
        'position': fields.function(_get_name,arg=2,type='many2one',obj='hr.job',string='Position',),
        'employee_id': fields.function(_get_name,arg=3,type="char",string='Employee PIN',),

    }
hr_other_deduction()



class hr_daily_allowance(osv.osv):
    def on_change_emp_id(self, cursor, uid, ids, emp_id, context=None):

        cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        department_id = row[0]
        cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        job_id = row[0]

        cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        employee_id = row[0]

        return {'value': {'position':job_id,'department':department_id,'employee_id':str(employee_id)}}


    def _get_name(self, cursor, user, ids, name, arg, context):
        print arg
        current_id = ids[0]
        cursor.execute("""SELECT emp_id FROM hr_daily_allowance WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]

        if arg==1:
            cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            department_id = row[0]
            print department_id
            return {current_id:department_id}
        if arg==2:
            cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            job_id = row[0]
            print job_id
            return {current_id:job_id}
        if arg==3:
            cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            employee_id = row[0]
            print employee_id
            return {current_id:str(employee_id)}

    def myonchange(self,cr,uid,on_basic, on_gross,context=None):
        vals={}
        if on_gross or on_basic:
           vals['value']={'amount':0.00}
        else:
            vals['value']={'percent_amount':False}
        return vals

    _name = "hr.daily.allowance"
    _columns = {

        'emp_id':fields.many2one('hr.employee', 'Employee', required=True,),
        'date':fields.date('Date',required=True,),
        'amount':fields.float('Amount',digits=(20,2),required=True,),
        'department': fields.function(_get_name,arg=1,type='many2one',obj='hr.department',string='Department',),
        'position': fields.function(_get_name,arg=2,type='many2one',obj='hr.job',string='Position',),
        'employee_id': fields.function(_get_name,arg=3,type="char",string='Employee PIN',),
        'on_basic': fields.boolean(string='Percentage on Basic'),
        'on_gross': fields.boolean(string='Percentage on Gross'),
        'percent_amount': fields.float(string='Percentage Amount'),


    }
hr_daily_allowance()

#bonus allowance
class hr_bonus_allowance(osv.osv):
    def on_change_emp_id(self, cursor, uid, ids, emp_id, context=None):

        cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        department_id = row[0]
        cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        job_id = row[0]

        cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        employee_id = row[0]

        return {'value': {'position':job_id,'department':department_id,'employee_id':str(employee_id)}}


    def _get_name(self, cursor, user, ids, name, arg, context):
        print arg
        current_id = ids[0]
        cursor.execute("""SELECT emp_id FROM hr_daily_allowance WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]

        if arg==1:
            cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            department_id = row[0]
            print department_id
            return {current_id:department_id}
        if arg==2:
            cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            job_id = row[0]
            print job_id
            return {current_id:job_id}
        if arg==3:
            cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            employee_id = row[0]
            print employee_id
            return {current_id:str(employee_id)}

    def myonchange(self,cr,uid,on_basic, on_gross,context=None):
        vals={}
        if on_gross or on_basic:
           vals['value']={'amount':0.00}
        else:
            vals['value']={'percent_amount':False}
        return vals

    _name = "hr.bonus.allowance"
    _columns = {

        'emp_id':fields.many2one('hr.employee', 'Employee', required=True,),
        'date':fields.date('Date',required=True,),
        'amount':fields.float('Amount',digits=(20,2),required=True,),
        'department': fields.function(_get_name,arg=1,type='many2one',obj='hr.department',string='Department',),
        'position': fields.function(_get_name,arg=2,type='many2one',obj='hr.job',string='Position',),
        'employee_id': fields.function(_get_name,arg=3,type="char",string='Employee PIN',),
        'on_basic': fields.boolean(string='Percentage on Basic'),
        'on_gross': fields.boolean(string='Percentage on Gross'),
        'percent_amount': fields.float(string='Percentage Amount'),


    }
hr_bonus_allowance()


#holiday allowance
class hr_holiday_allowance(osv.osv):
    def on_change_emp_id(self, cursor, uid, ids, emp_id, context=None):

        cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        department_id = row[0]
        cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        job_id = row[0]

        cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        employee_id = row[0]

        return {'value': {'position':job_id,'department':department_id,'employee_id':str(employee_id)}}


    def _get_name(self, cursor, user, ids, name, arg, context):
        #print arg
        current_id = ids[0]
        cursor.execute("""SELECT emp_id FROM hr_holiday_allowance WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]

        if arg==1:
            cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            department_id = row[0]
            print department_id
            return {current_id:department_id}
        if arg==2:
            cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            job_id = row[0]
            print job_id
            return {current_id:job_id}
        if arg==3:
            cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            employee_id = row[0]
            print employee_id
            return {current_id:str(employee_id)}

    def myholidayonchange(self,cr,uid,on_basic, on_gross,context=None):
        vals={}
        if on_gross or on_basic:
           vals['value']={'amount':0.00}
        else:
            vals['value']={'percent_amount':False}
        return vals

    _name = "hr.holiday.allowance"
    _columns = {

        'emp_id':fields.many2one('hr.employee', 'Employee', required=True,),
        'date':fields.date('Date',required=True,),
        'amount':fields.float('Amount',digits=(20,2),required=True,),
        'department': fields.function(_get_name,arg=1,type='many2one',obj='hr.department',string='Department',),
        'position': fields.function(_get_name,arg=2,type='many2one',obj='hr.job',string='Position',),
        'employee_pin': fields.function(_get_name,arg=3,type="char",string='Employee PIN',),
        'on_basic': fields.boolean(string='Percentage on Basic'),
        'on_gross': fields.boolean(string='Percentage on Gross'),
        'percent_amount': fields.float(string='Percentage Amount'),

    }

    _defaults = {
        'amount':0.00,
    }
hr_holiday_allowance()

#provident_decuction
class hr_provident_deduction(osv.osv):
    def on_change_emp_id(self, cursor, uid, ids, emp_id, context=None):

        cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        department_id = row[0]
        cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        job_id = row[0]

        cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        employee_id = row[0]

        return {'value': {'position':job_id,'department':department_id,'employee_id':str(employee_id)}}


    def _get_name(self, cursor, user, ids, name, arg, context):
        #print arg
        current_id = ids[0]
        cursor.execute("""SELECT emp_id FROM hr_provident_decuction WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]

        if arg==1:
            cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            department_id = row[0]
            print department_id
            return {current_id:department_id}
        if arg==2:
            cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            job_id = row[0]
            print job_id
            return {current_id:job_id}
        if arg==3:
            cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            employee_id = row[0]
            print employee_id
            return {current_id:str(employee_id)}

    def myholidayonchange(self,cr,uid,on_basic, on_gross,context=None):
        vals={}
        if on_gross or on_basic:
           vals['value']={'amount':0.00}
        else:
            vals['value']={'percent_amount':False}
        return vals

    _name = "hr.provident.deduction"
    _columns = {

        'emp_id':fields.many2one('hr.employee', 'Employee', required=True,),
        'date':fields.date('Date',required=True,),
        'amount':fields.float('Amount',digits=(20,2),required=True,),
        'department': fields.function(_get_name,arg=1,type='many2one',obj='hr.department',string='Department',),
        'position': fields.function(_get_name,arg=2,type='many2one',obj='hr.job',string='Position',),
        'employee_pin': fields.function(_get_name,arg=3,type="char",string='Employee PIN',),
        'on_basic': fields.boolean(string='Off for Current Month'),
        'on_gross': fields.boolean(string='Percentage on Gross'),
        'percent_amount': fields.float(string='Percentage Amount'),

    }

    _defaults = {
        'amount':0.00,
    }
hr_provident_deduction()

#canteen_decuction
class hr_canteen_deduction(osv.osv):
    def on_change_emp_id(self, cursor, uid, ids, emp_id, context=None):

        cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        department_id = row[0]
        cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        job_id = row[0]

        cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                       ,[emp_id])
        row = cursor.fetchone()
        #print row
        employee_id = row[0]

        return {'value': {'position':job_id,'department':department_id,'employee_id':str(employee_id)}}


    def _get_name(self, cursor, user, ids, name, arg, context):
        #print arg
        current_id = ids[0]
        cursor.execute("""SELECT emp_id FROM hr_canteen_deduction WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]

        if arg==1:
            cursor.execute("""SELECT department_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            department_id = row[0]
            print department_id
            return {current_id:department_id}
        if arg==2:
            cursor.execute("""SELECT job_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            job_id = row[0]
            print job_id
            return {current_id:job_id}
        if arg==3:
            cursor.execute("""SELECT employee_id FROM hr_employee WHERE id=%s """
                           ,[emp_id])
            row = cursor.fetchone()
            #print row
            employee_id = row[0]
            print employee_id
            return {current_id:str(employee_id)}

    def mealCalculationonchange(self,cr,uid,ids,no_meal, meal_rate,context=None):
        vals={}
        if no_meal>0 and meal_rate>0:
            dd = no_meal * meal_rate
            vals['value']={'amount': dd}
            return vals
        else:
            vals['value']={'amount': 0.00}
            return vals

    def nomealCalculationonchange(self,cr,uid,ids,no_meal, meal_rate,context=None):
        vals={}
        if no_meal>0 and meal_rate>0:
            dd = no_meal * meal_rate
            vals['value']={'amount': dd}
            return vals
        else:
            vals['value']={'amount': 0.00}
            return vals

    _name = "hr.canteen.deduction"
    _columns = {

        'emp_id':fields.many2one('hr.employee', 'Employee', required=True,),
        'date':fields.date('Date',required=True,),
        'amount':fields.float('Amount',digits=(20,2),required=True,),
        'department': fields.function(_get_name,arg=1,type='many2one',obj='hr.department',string='Department',),
        'position': fields.function(_get_name,arg=2,type='many2one',obj='hr.job',string='Position',),
        'employee_pin': fields.function(_get_name,arg=3,type="char",string='Employee PIN',),
        'no_meal': fields.integer(string='Number of Meal'),
        'meal_rate': fields.float(string='Meal Rate'),
        'percent_amount': fields.float(string='Percentage Amount'),

    }

    _defaults = {
        'amount':0.00,
    }
hr_canteen_deduction()

class hr_payroll_dev(osv.osv):


    def _get_bonus(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT SUM(amount) AS totDaiAlw FROM hr_bonus WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalDailyAllowance = cursor.fetchone()[0]
        #print totalDailyAllowance
        return {ids[0]:totalDailyAllowance}

    def _get_special_allowance(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT SUM(amount) AS totDaiAlw FROM hr_special_allowance WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalDailyAllowance = cursor.fetchone()[0]
        #print totalDailyAllowance
        return {ids[0]:totalDailyAllowance}

    def _get_arrear_salary(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT SUM(amount) AS totDaiAlw FROM hr_arrear_salary WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalDailyAllowance = cursor.fetchone()[0]
        #print totalDailyAllowance
        return {ids[0]:totalDailyAllowance}

    def _get_other_earnings(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT SUM(amount) AS totDaiAlw FROM hr_other_earnings WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalDailyAllowance = cursor.fetchone()[0]
        #print totalDailyAllowance
        return {ids[0]:totalDailyAllowance}

    def _get_absent_deduction(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT SUM(amount) AS totDaiAlw FROM hr_absent_deduction WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalDailyAllowance = cursor.fetchone()[0]
        #print totalDailyAllowance
        return {ids[0]:totalDailyAllowance}

    def _get_pf_deduction(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT SUM(amount) AS totDaiAlw FROM hr_pf_deduction WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalDailyAllowance = cursor.fetchone()[0]
        #print totalDailyAllowance
        return {ids[0]:totalDailyAllowance}

    def _get_advance_salary(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT SUM(amount) AS totDaiAlw FROM hr_advance_salary WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalDailyAllowance = cursor.fetchone()[0]
        #print totalDailyAllowance
        return {ids[0]:totalDailyAllowance}

    def _get_mobile_bill(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT SUM(amount) AS totDaiAlw FROM hr_mobile_bill WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalDailyAllowance = cursor.fetchone()[0]
        #print totalDailyAllowance
        return {ids[0]:totalDailyAllowance}

    def _get_revenue_stamp(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT SUM(amount) AS totDaiAlw FROM hr_revenue_stamp WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalDailyAllowance = cursor.fetchone()[0]
        #print totalDailyAllowance
        return {ids[0]:totalDailyAllowance}

    def _get_other_deduction(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT SUM(amount) AS totDaiAlw FROM hr_other_deduction WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalDailyAllowance = cursor.fetchone()[0]
        #print totalDailyAllowance
        return {ids[0]:totalDailyAllowance}



    def _get_daily_allowance(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT SUM(amount) AS totDaiAlw FROM hr_daily_allowance WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalDailyAllowance = cursor.fetchone()[0]
        #print totalDailyAllowance
        return {ids[0]:totalDailyAllowance}

    def _get_daily_allowance_percent(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT SUM(percent_amount) AS totDaiAlw FROM hr_daily_allowance WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totaldutyAllowanceperc = cursor.fetchone()[0]
        #print totalDailyAllowance
        return {ids[0]:totaldutyAllowanceperc}

    def _get_daily_allowance_basic_gross(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT on_basic, on_gross FROM hr_daily_allowance WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalDutyAllowance = cursor.fetchall()
        #print totalDailyAllowance
        if totalDutyAllowance:
            if totalDutyAllowance[0][0]:
                return {ids[0]:'basic'}
            elif totalDutyAllowance[0][1]:
                return {ids[0]:'gross'}
            else:
                return {ids[0]:'ghora'}
        else:
            return {ids[0]:'ghora'}


    def _get_holiday_allowance_basic_gross(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT on_basic, on_gross FROM hr_daily_allowance WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalHolidayAllowance = cursor.fetchall()
        #print totalDailyAllowance
        if totalHolidayAllowance:
            if totalHolidayAllowance[0][0]:
                return {ids[0]:'basic'}
            elif totalHolidayAllowance[0][1]:
                return {ids[0]:'gross'}
            else:
                return {ids[0]:'ghora'}
        else:
            return {ids[0]:'ghora'}

    def _get_bonus_allowance(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT SUM(amount) AS totDaiAlw FROM hr_daily_allowance WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalDailyAllowance = cursor.fetchone()[0]
        #print totalDailyAllowance
        return {ids[0]:totalDailyAllowance}

    def _get_bonus_allowance_percent(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT SUM(percent_amount) AS totDaiAlw FROM hr_daily_allowance WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totaldutyAllowanceperc = cursor.fetchone()[0]
        #print totalDailyAllowance
        return {ids[0]:totaldutyAllowanceperc}

    def _get_bonus_allowance_basic_gross(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT on_basic, on_gross FROM hr_daily_allowance WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalBonusAllowance = cursor.fetchall()
        #print totalDailyAllowance
        if totalBonusAllowance:
            if totalBonusAllowance[0][0]:
                return {ids[0]:'basic'}
            elif totalBonusAllowance[0][1]:
                return {ids[0]:'gross'}
            else:
                return {ids[0]:'ghora'}
        else:
            return {ids[0]:'ghora'}

    def _get_provident_deduction_off(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT on_basic, on_gross FROM hr_provident_deduction WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalPFDeduction = cursor.fetchall()
        #print totalDailyAllowance
        if totalPFDeduction:
            if totalPFDeduction[0][0]:
                return {ids[0]:'off'}
            elif totalPFDeduction[0][1]:
                return {ids[0]:'offf'}
            else:
                return {ids[0]:'ghora'}
        else:
            return {ids[0]:'ghora'}

    def _get_canteen_deduction(self, cursor, user, ids, name, arg, context):
        #print 'Computing Daily Allowance'
        current_id = ids[0]
        cursor.execute("""SELECT employee_id,date_from,date_to FROM hr_payslip WHERE id=%s """
                       ,[current_id])
        row = cursor.fetchone()
        #print row
        emp_id = row[0]
        date_from =row[1]
        date_to=row[2]
        #print date_from,' ',date_to
        cursor.execute("""SELECT SUM(amount) AS totDaiAlw FROM hr_canteen_deduction WHERE emp_id=%s AND date>=%s AND date<=%s """
                       ,[emp_id,date_from,date_to])
        totalDailyAllowance = cursor.fetchone()[0]
        #print totalDailyAllowance
        return {ids[0]:totalDailyAllowance}

    _inherit = 'hr.payslip'
    _columns = {

        'daily_allowance': fields.function(_get_daily_allowance,type='float',string='Duty Allowance',store=True),
        'daily_allowance_percent': fields.function(_get_daily_allowance_percent,type='float',string='Duty Allowance',store=True),
        'basic_or_gross': fields.function(_get_daily_allowance_basic_gross,type='char',string='Basic or Gross',store=True),

        'special_allowance': fields.function(_get_special_allowance,type='float',string='Special Allowance',store=True),
        'arrear_salary': fields.function(_get_arrear_salary,type='float',string='Arrear Salary',store=True),
        'other_earnings': fields.function(_get_other_earnings,type='float',string='Other Earnings',store=True),
        'wpl': fields.function(_get_absent_deduction,type='float',string='Absent Deduction',store=True),
        'pf_deduction': fields.function(_get_pf_deduction,type='float',string='PF Deduction',store=True),
        'adv_salary': fields.function(_get_advance_salary,type='float',string='Advance Salary',store=True),
        'mob_bill': fields.function(_get_mobile_bill,type='float',string='Mobile Bill',store=True),
        'rev_stamp': fields.function(_get_revenue_stamp,type='float',string='Reveneue Stamp',store=True),
        'other_deduction': fields.function(_get_other_deduction,type='float',string='Other Deduction',store=True),
        'bonus': fields.function(_get_bonus,type='float',string='Bonus',store=True),
        'holiday_allowance':fields.function(_get_holiday_allowance_basic_gross,type='char',string='Holiday Allowance',store=True),

        'bonus_allowance': fields.function(_get_bonus_allowance,type='float',string='Bonus Allowance',store=True),
        'bonus_allowance_percent': fields.function(_get_bonus_allowance_percent,type='float',string='Bonus Allowance',store=True),
        'bonus_basic_or_gross': fields.function(_get_bonus_allowance_basic_gross,type='char',string='Basic or Gross',store=True),

        # 'provident_decution': fields.function(_get_provident_deduction_off,type='char',string='Off for this month',store=True),
        'provident_deduction': fields.function(_get_provident_deduction_off,type='char',string='Off for this month',store=True),
        'canteen_deduction': fields.function(_get_canteen_deduction,type='float',string='Canteen Deduction',store=True),
    }
    _defaults = {
        'daily_allowance':0.00,
        'special_allowance': 0.00,
        'arrear_salary': 0.00,
        'other_earnings': 0.00,

        'wpl': 0.00,
        'pf_deduction': 0.00,
        'adv_salary': 0.00,

        'mob_bill': 0.00,
        'rev_stamp': 0.00,
        'other_deduction': 0.00,
        'bonus':0.00,
        'provident_deduction' : 0.00
    }
hr_payroll_dev()

class contract_addition(osv.osv):
    _name = 'hr.contract'
    _inherit = 'hr.contract'
    _columns = {
        'welfare_fund': fields.boolean('Welfare Fund'),

        'mobile_bill_limit': fields.float('Mobile Bill Limit'),
        'mobile_bill_limit_exec': fields.boolean('Mobile Bill Extra'),
        'mobile_bill_extra': fields.float('MB Extra Amount'),
        'mobile_bill_remarks': fields.char('Remarks'),

        'driver_allowance': fields.float('Driver Allowance'),
        'driver_all_limit_exec': fields.boolean('Driver Allowance Extra'),
        'driver_all_extra': fields.float('Driver Allowance Extra Amount'),
        'driver_all_remarks': fields.char('Remarks'),

        'fuel_benefit': fields.float('Fuel Benefit'),
        'fuel_benefit_limit_exec': fields.boolean('Fuel Benefit Extra'),
        'fuel_benefit_extra': fields.float('Fuel Benefit Extra Amount'),
        'fuel_benefit_remarks': fields.char('Remarks'),

        'provident_fund': fields.boolean('Provident Fund'),
        'emp_insurance': fields.float('Employee Insurance'),
        'home_allowance': fields.float('Home Allowance'),
        'home_allowance_percent': fields.float('Home Allowance %'),
    }

    _defaults = {
        'mobile_bill_limit':0.00,
        'driver_allowance': 0.00,
        'fuel_benefit':0.00,
        'emp_insurance': 0.00,
    }

class structure_in_grade(osv.Model):
    _inherit = 'hr.grade'
    _columns = {

    }

class addition_nd_deduction(osv.Model):
    _name = 'addition.deduction'
    _columns = {
        'sal_rule': fields.many2one('hr.salary.rule', 'Salary Rule'),
        't_date': fields.date('Date'),
        'f_amount': fields.float('Fixed Amount'),
        'employee_sel': fields.many2many('hr.employee', 'em_addnded', 'emp_id','add_ded_id', 'Employee'),

    }

class hr_salary_rule_range(osv.Model):
    _inherit = 'hr.salary.rule'
    _columns = {
        'amount_range': fields.one2many('amount.range.line', 'name','Amount Range'),
        'income_tax':fields.boolean('Income Tax'),
        'home_allowance':fields.boolean('Home Allowance'),

    }

class amount_range_line(osv.Model):
    _name = 'amount.range.line'
    _columns = {
        'name' : fields.many2one('hr.salary.rule', 'Amount Range'),
        'range_from': fields.float('Range From'),
        'range_to': fields.float('Range To'),
        'range_amount': fields.float('Amount')
    }

# class work_location_allowance(osv.Model):
#     _name = 'work.location.allowance'
#     _columns = {
#                 'name': fields.char('Work Location Allowance'),
#                 'work_location_line': fields.one2many('work.location.line','location_name','Work Location'),
#     }


class work_location_line(osv.Model):
    _name = 'work.location.line'
    _columns = {
        'name': fields.many2one('hr.district', 'Name'),
        'allowance_amount': fields.float('Amount'),
    }