from openerp.osv import fields, osv
from openerp import tools


class hr_req_job_application_filter(osv.osv):
     _name = 'hr.cv.filter'



     def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image)
        return result

     def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

     def primary_select_button(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'selected_application': 'initially_selected'})
        return True


     _columns = {
         'applicant_title':fields.selection([('a','Mr'),('b', 'Ms'),],'Title',required='True'),
         'partner_name': fields.char("Applicant's Name", size=64,required='True'),
         'father_name':fields.char('Father Name',size=50,required='True'),
         'mother_name':fields.char('Mother Name',size=50,required='True'),
         'partner_phone': fields.char('Phone', size=32),
         'partner_mobile': fields.char('Mobile', size=32),
         'applicant_gender':fields.selection([('a','Male'),('b', 'Female'),],'Gender'),
         'nationality':fields.char('Nationality',size=50,required='True'),
         'nid':fields.char('National Id',required='True'),
         'email_from': fields.char('Email', size=128, help="These people will receive email."),
         'date_of_birth':fields.date('Date of Birth',size=50),
         'present_address':fields.char('Present Address',size=50),
         'permanent_address':fields.char('Permanent Address',size=50),
         'type_id': fields.many2one('hr.recruitment.degree', 'Degree'),
         'institution':fields.char('Institution',size=50),
         'latest_designation':fields.char('Latest Designation',size=50),
         'company':fields.char('Company',size=50),
         'resume':fields.many2many('ir.attachment', 'hr_recruitment_attachment', 'employee_id', 'attachment_id', 'Attachments'),
         'job_id': fields.many2one('hr.job', 'Applied Job'),
         'recruitment_no':fields.many2one('manpower.requisition','Recruitment Number'),
         'selected_application':fields.char(),

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

     }

