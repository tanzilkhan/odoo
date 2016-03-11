from openerp.osv import fields, osv
import datetime


class hr_req_manpower_requisition(osv.osv):


    def _get_job_position(self, cr, uid, ids, context=None):
        res = []
        for employee in self.pool.get('hr.employee').browse(cr, uid, ids, context=context):
            if employee.job_id:
                res.append(employee.job_id.id)
        return res

    _name = "manpower.requisition"

    _columns = {
        'name':fields.char('Requisition Number', required="1"),
        'dept_name': fields.many2one('hr.department','Department', readonly='True'),
        'date_of_requistion': fields.date('Date of requisition'),
        'job_title':fields.many2one('hr.job','Job Title', required="1"),
        'no_required_workforce': fields.integer('No of required workforce'),
        'job_level':fields.many2one('hr.job.level','Job Level'),
        'job_type':fields.many2one('hr.job.type','Job Type'),
        'requisition_date':fields.date('Date of Requisition'),

        'hr_comments_remarks': fields.text('HR Comment/Remarks'),
        'requirements': fields.text('Requirements'),
        'justification':fields.text('Justification for recruitment'),
        'existing_emp':fields.integer('Existing Employee',readonly='True'),
        'shortage_emp':fields.integer('Shortage Employee'),

        'requisition_by':fields.many2one('res.users','Requisition By',readonly='1'),


        'state': fields.selection([('incharge', 'Draft'),
                                   ('head_dept', 'Head Of Department'),
                                   ('head_hr', 'Head Of HR'),
                                   ('ceo', 'CEO'),
                                   ('recruitment_desk', 'Recruitment Desk'),
                                   ('cancel', 'Rejected')],
                                  'Status', readonly=True, required=True,
            help="By default 'In position', set it to 'In Recruitment' if recruitment process is going on for this job position."),
    }


    def get_department(self, cr, uid, context=None ):
        # current_user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        employee_obj = self.pool.get('hr.employee')
        current_employee = employee_obj.search(cr, uid,[('user_id','=',uid)])
        emp_info = employee_obj.browse(cr, uid, current_employee[0], context)
        dept_id = emp_info['department_id'].id

        current_employee_list = employee_obj.search(cr, uid,[('department_id','=',dept_id)])
        total_employees = len(current_employee_list)

        return dept_id

    def get_employees(self, cr, uid, context=None ):
        # current_user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        employee_obj = self.pool.get('hr.employee')
        current_employee = employee_obj.search(cr, uid,[('user_id','=',uid)])
        emp_info = employee_obj.browse(cr, uid, current_employee[0], context)
        dept_id = emp_info['department_id'].id

        current_employee_list = employee_obj.search(cr, uid,[('department_id','=',dept_id)])
        total_employees = len(current_employee_list)

        return total_employees

    def get_current_date(self , cr, uid, context=None):
        dat = datetime.datetime.today().date()
        return str(dat)

    _defaults ={
        'state':'incharge',
        'dept_name':get_department,
        'existing_emp': get_employees,
        'date_of_requistion':get_current_date,
        'requisition_by':lambda obj, cr, uid, context: uid,
    }




    def create(self, cr, uid, value, context=None ):
        value['state'] = 'head_dept'
        return super(hr_req_manpower_requisition, self).create(cr, uid, value, context=context)

    def write(self, cr, uid, ids, value, context=None):
        obj = self.browse(cr, uid, ids, context)
        state = ''
        for each_line in obj:
            state = each_line['state']
        print state
        if state == 'incharge':
            value['state'] = 'head_dept'

        return super(hr_req_manpower_requisition, self).write(cr, uid, ids, value, context=context)

    def job_incharge(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'head_dept'})
        return True

    def job_head_dept(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'head_hr'})
        return True

    def job_head_hr(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'ceo'})
        return True

    def job_ceo(self, cr, uid, ids, context=None):
        for i in self.browse(cr,uid,ids,context=context):
            job_id=i.job_title.id
            no_of_rec_wf=i.no_required_workforce
            self.pool.get('hr.job').write(cr,uid,job_id,{'no_of_recruitment':no_of_rec_wf})
        self.write(cr, uid, ids, {'state': 'recruitment_desk'})
        return True

    def job_cancel(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'cancel'})
        return True

    def launch_recruitment(self, cr, uid, ids, context=None):
        for i in self.browse(cr,uid,ids,context=None):
            job_id=i.job_title.id
            department_id=i.dept_name.id


        context.update({'default_wf_requisition':ids[0],
                        'default_department_id':department_id,
                        'default_job_title':job_id,
                        # 'default_no_of_vacancies':vacancies,
                        })
        return{
              'view_type': 'form',
              'view_mode': 'form',
              'view_id':False,
              'res_model': 'launch.recruitment',
              'context': context,
              'type': 'ir.actions.act_window',
              'nodestroy':True,
              'target': 'current',
              }

class hr_req_job_level(osv.osv):

    _name="hr.job.level"

    _columns={
        'name':fields.char('Job Level')
    }

class hr_req_job_type(osv.osv):

    _name="hr.job.type"

    _columns={
        'name':fields.char('Job Type')
    }



