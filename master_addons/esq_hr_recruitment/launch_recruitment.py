from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _

class hr_req_launch_recruitment(osv.osv):
     _name = 'launch.recruitment'

     def apply_button(self, cr, uid, ids, context=None):
        for i in self.browse(cr,uid,ids,context=context):
            job_id=i.job_title.id
            wf_requisition=i.wf_requisition.id
        test_design_brs=self.pool.get('test.design')
        test_design_list=test_design_brs.search(cr,uid,[('recruitment_no','=',wf_requisition)])
        if test_design_list:
            last_test_design=test_design_list[-1]
            exam_types=test_design_brs.browse(cr,uid,last_test_design,context=context).exam_type
            exam_list=[]
        else:
            raise osv.except_osv(_('Warning!'),_('There is no Test Design created for this Job Title'))


        for exams in exam_types:
            exam_list.append((0, 0, {'test_name':exams.name.id}))

        new_id=ids[0]

        context.update({'default_job_id':job_id,'default_recruitment_no':new_id,'default_test_design':exam_list})

        return{
              'view_type': 'form',
              'view_mode': 'form',
              'view_id':False,
              'res_model': 'hr.applicant',
              'context': context,
              'type': 'ir.actions.act_window',
              'nodestroy':True,
              'target': 'current',
              }



     def job_done(self, cr, uid, ids, *args):
            self.write(cr, uid, ids, {'state': 'done'})
            return True

     # def _get_test(self, cr, uid, context=None):
     #    print "\n\nget function call Default"
     #    res = 'Satellite TV'
     #    return res

     _columns = {
         'department_id': fields.many2one('hr.department','Department',readonly='1'),
         'company_industry_type':fields.char('Type of Industry',size=50,required=True),
         'job_title':fields.many2one('hr.job','Job Title',readonly='1'),
         # 'no_of_vacancies':fields.integer('Number of Vacancies'),
         'receive_cv':fields.char('Receive CVs',readonly=True),
         'enclose_photo_cv':fields.char('Enclose Photo with CV',readonly=True),
         'application_deadline_date':fields.date('Last date of Application',required=True),
         'applicant_gender':fields.selection([('a','Male'),('b', 'Female'),],'Gender'),
         'job_level':fields.many2one('hr.job.level','Job Level'),
         'educational_qualification':fields.char('Education Qualification'),
         'job_responsibility':fields.text('Job Responsibility'),
         'additional_responsibility':fields.text('Additional Responsibility'),
         'job_location':fields.char('Job Location'),

         'age_min':fields.integer('Minimum Age'),
         'age_max':fields.integer('Maximum Age'),
         'year_min':fields.integer('Minimum Experience'),
         'year_max':fields.integer('Maximum Experience'),

         'company_name':fields.char('Company name'),
         'company_address':fields.char('Company Address'),
         'compensation_benefits':fields.char('Benefits'),
         'wf_requisition':fields.many2one('manpower.requisition','Workforce Requisition Number'),


        'state': fields.selection([('draft', 'Recruitment On Going'),('done', 'Recruitment done')], 'Status', readonly=True, required=True,),

    }
     # def get_no_of_vacancies(self, cr, uid,wf_requisition,context=None ):
     #     vacancies_obj = self.pool.get('manpower.requisition')
     #     current_vacancies = vacancies_obj.search(cr, uid,[('name','=',wf_requisition)])
     #     vacancies_info=current_vacancies.browse(cr, uid, current_vacancies, context)
     #     vacancies=vacancies_info['shortage_emp']

         # print vacancies

     def onchange_job_title(self, cr, uid,ids,job_id,context=None ):
         result={}
         job_obj=self.pool.get('hr.job')
         job_responsibility=job_obj.search(cr, uid,[('id','=',job_id)])
         job_info=job_obj.browse(cr, uid, job_responsibility[0], context)
         result['value']={'job_responsibility':job_info.job_responsibility}
         return result


     _defaults = {
        'state':'draft',
        'company_industry_type': 'Esquire',
        'receive_cv':'Online CV',
        'enclose_photo_cv':'Yes',
        # 'no_of_vacancies':get_no_of_vacancies,
        # 'job_responsibility':get_job_responsibility,
     }



class hr_req_job_level(osv.osv):

    _name="hr.job.level"

    _columns={
        'name':fields.char('Job Level')
    }