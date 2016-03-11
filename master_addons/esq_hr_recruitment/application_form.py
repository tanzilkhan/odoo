import base64
from openerp.osv import fields, osv
from openerp import tools
from tempfile import TemporaryFile





# def import_file(self, cr, uid, ids, context=None):
#         fileobj = TemporaryFile('w+')
#         fileobj.write(base64.decodestring(data))
#         return

class hr_req_job_application_form(osv.osv):
     _name = 'hr.applicant'
     _inherit='hr.applicant'

     def confirm(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'pending'})
        return True

     def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image)
        return result

     def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)


     _columns = {
         # 'name':fields.char('Applicant Name',size=50),
         'applicant_title':fields.selection([('a','Mr'),('b', 'Ms'),],'Title',required='True'),
         'creation_date':fields.date('Creation Date',size=50),
         # 'designation_apply_for':fields.many2one('hr.job','Designation applied to',size=50,required=True),
         'title':fields.char('Title',size=50),
         'date_of_birth':fields.date('Date of Birth',size=50),
         'father_name':fields.char('Father Name',size=50,required='True'),
         'mother_name':fields.char('Mother Name',size=50,required='True'),
         'applicant_gender':fields.selection([('a','Male'),('b', 'Female'),],'Gender'),
         'nationality':fields.char('Nationality',size=50,required='True'),
         'nid':fields.char('National Id',required='True'),
         'present_address':fields.char('Present Address',size=50),
         'permanent_address':fields.char('Permanent Address',size=50),
         'institution':fields.char('Institution',size=50),
         'latest_designation':fields.char('Latest Designation',size=50),
         'company':fields.char('Company',size=50),
         # 'resume': fields.boolean('Uplode Resume'),
         'resume':fields.many2many('ir.attachment', 'hr_recruitment_attachment', 'employee_id', 'attachment_id', 'Attachments'),
         'upload_photo':fields.boolean("Upload Photo",
            help="This field holds the image used as photo for the employee, limited to 1024x1024px."),
         'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized photo", type="binary", multi="_get_image",
            store = {
                'job.application.form': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized photo of the employee. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),
         'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized photo", type="binary", multi="_get_image",
            store = {
                'job.application.form': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized photo of the employee. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required."),

         'test_design':fields.one2many('recruitment.applicant.test','rec_rel','Test Summary'),
         'recruitment_no':fields.many2one('manpower.requisition','Recruitment Number'),


          'joining_date':fields.date('Joining Date'),
          #joining report,
          'induction':fields.selection([('a','Yes'),('b', 'No'),],'Induction'),
          # 'induction_note':fields.text(),
          'domain_it_dept':fields.boolean('Email/domain ID to IT Dept'),
          'security_dept':fields.boolean('ID Card to Security Dept'),
          'support_service':fields.boolean('Stationary, Lunch to Support Service'),
          'black_list':fields.boolean('Blacklisted'),

     }

     def create(self, cr, uid, value, context=None ):
         value['name'] = value['partner_name']
         return super(hr_req_job_application_form, self).create(cr, uid, value, context=context)



     def interview_button(self, cr, uid, ids, context=None):

         applied_job=self.browse(cr,uid,ids,context=context)[0].job_id.id

         question_set_id=self.pool.get('hr.job').browse(cr,uid,applied_job,context=context).question_set.id
         question_name=self.pool.get('interview.question.set').browse(cr,uid,question_set_id,context=context).question

         for i in self.browse(cr,uid,ids,context=context):
            job_ids=i.job_id.id

            ap_name=i.id

         question_weight_set=[]

         for j in question_name:
             question_weight_set.append((0,0,{'question':j.name.id,'weight':j.weight}))


         context.update({'default_applicant_question_set':question_weight_set})

         context.update({'default_applicant_question_set':question_weight_set, 'default_name_of_candidate':ap_name,'default_post_applied_for':job_ids})

         return{
            'type': 'ir.actions.act_window',
            'res_model': 'interview.test',
            'view_type': 'form',
            'context':context,
            'view_mode': 'form',
            'view_id': False,
            'target':'new'
            }


class hr_req_applicant_tests(osv.Model):
    _name = 'recruitment.applicant.test'

    _columns = {
        'rec_rel':fields.many2one('hr.applicant'),
        'test_name':fields.many2one('test.design.exam.type','Test Name',readonly='True'),
        'total_marks':fields.float('Total Marks')

    }

class hr_req_interview_test(osv.Model):
    _name = 'interview.test'


    _columns = {
        'name_of_candidate':fields.many2one('hr.applicant','Name of Candidate'),
        'pin':fields.char('Roll or Pin'),
        'date':fields.date('Date'),
        'post_applied_for':fields.many2one('hr.job','Post Applied For'),
        'present_salary':fields.float('Present Salary'),
        'expected_salary':fields.float('Expected Salary'),
        'ref_source':fields.char('Source/Ref'),
        'other_remarks':fields.char('Other Remarks'),
        'applicant_question_set':fields.one2many('applicant.question.set','applicant_qus_set_rel','Applicant Question Set'),
    }

    def create(self, cr, uid, value, context=None ):
         return super(hr_req_interview_test, self).create(cr, uid, value, context=context)

class applicant_question_set(osv.osv):
    _name='applicant.question.set'

    def onchange_total_marks(self,cr,uid,ids,scale,weight,context=None):
        result = {}
        likert_scale_obj=self.pool.get('interview.likert.scale')
        for each_line in likert_scale_obj.browse(cr,uid,[scale,],context=context):
            total = each_line['scale']*weight
        # id=scale_get.search(cr,uid,[('scale','=',scale)],context=context)
        result['value'] = {'total': total,}
        return result

    _columns={
        'rel_question':fields.many2one('interview.test'),
        'question':fields.many2one('interview.question','Question'),
        'weight':fields.integer('Weight'),
        'scale':fields.many2one('interview.likert.scale','Scale'),
        'total':fields.float('Total'),
        'remarks':fields.char('Specific Remarks'),
        'applicant_qus_set_rel':fields.many2one('interview.test')

    }
