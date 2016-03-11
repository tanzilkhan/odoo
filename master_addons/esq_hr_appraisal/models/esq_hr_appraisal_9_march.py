from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _


class hr_appraisal_form(osv.osv):
    _name = "hr.appraisal.form"
    _description = "Appraisal Form"


    _columns = {
        'name': fields.char('Appraisal Form Title', required=True),
        'type': fields.many2one('hr.appraisal.type', 'Type'),
        'purpose': fields.many2one('hr.appraisal.purpose', 'Purpose'),
        'additional_details': fields.one2many('hr.appraisal.details', 'name', 'Additional Details', required=True),
        'appraisal_description': fields.text('Description'),
        'month_first': fields.integer('First Appraisal (months)'),
        'month_next': fields.integer('Periodicity of Appraisal (months)'),
        'appraisal_for': fields.selection([('department', 'Department'), ('employee', 'Employee')],'Appraisal For'),
        'selected_department': fields.many2one('hr.department', 'Department'),
        'selected_employees': fields.many2many('hr.employee', 'hr_emp_appr_rel_n', 'cal_id', 'employee_id', 'Select Employee(s)'),
        'reason': fields.many2one('hr.appraisal.reasons','Reason', required=True),
        'due_date_appraisal': fields.boolean('Due Date Appraisal'),
        'deadline': fields.date('Deadline'),

        'next_appraisal': fields.selection([('periodic', 'Periodic'),('specific', 'Specific Date')], 'Next Appraisal'),
        'month_next_date': fields.date('Next Appraisal Date'),
    }

    def create(self, cr, uid, values, context=None):
        appraisal_detail = []
        for each_line in values['additional_details']:
            appraisal_detail.append([0, False, each_line[2]])


        if values['appraisal_for']=='employee':
            employee_list = values['selected_employees'][0][2]
        else:
            employee_obj = self.pool.get('hr.employee')
            # employee_list = employee_obj.search(cr, uid, [('department_id', '=', values['selected_department'])])
            employee_list = employee_obj.search(cr, uid, [('department_id', '=', values['selected_department']),('active','=',True),('name_related','not in',('Administrator','Mahbubur Rahman HOHR'))])

        weight_list = []
        for each in values['additional_details']:
            weight_list.append(each[2]['weight'])

        if len(weight_list)>0:
            total_weight = sum(weight_list)
        else:
            total_weight = 0

        if total_weight == 25:

            form_id = super(hr_appraisal_form, self).create(cr, uid, values, context=context)

            plan_values = {
                'name': values['name'],
                'active': True,
                'appraisal_form_ids': form_id,
            }

            plan_obj = self.pool.get('hr.appraisal.plan')
            plan_id = super(hr_appraisal_plan, plan_obj).create(cr, uid, plan_values, context=context)

            for each_employee_id in employee_list:
                employee_obj = self.pool.get('hr.employee')
                employee_info = employee_obj.browse(cr, uid, each_employee_id, context)
                print employee_info.name_related
                print employee_info.parent_id.name

                appraisal_values = {
                    'employee_pin': employee_info.employee_pin,
                    'deadline': values['deadline'],
                    'responsible_person': employee_info.parent_id.name,
                    'appraisal_plan': plan_id,
                    'employee_id': each_employee_id,
                    'due_date_appraisal': values['due_date_appraisal'],
                    'reason': values['reason'],
                    'dept_id': employee_info.department_id.name,
                    'employee_name': employee_info.name_related,

                    'training_suggestion': False,
                    'remainder_criterion': False,
                    'improvements': False,
                    'appraisal_venue': False,
                    'comments': False,
                    'trainings_needed': False,
                    'initiation_date': False,
                    'performance_feedback': False,
                    'problems_faced': False,
                    'appreciation': False,
                    'description_appraisal': False,
                    'appraisal_datetime': False,
                    'period_accomplishments': False,
                    'next_appraisal': False,
                    'instruction': False,
                    # 'appraisal_goal': [],
                    'action_plan': False,
                    'extra_ordinary_activities': False,
                    'could_be_done': False,

                    'appraisal_questions': appraisal_detail,
                    'appraisal_goal': appraisal_detail,
                    'initiation_date': datetime.now().date(),
                }

                appraisal_obj = self.pool.get('hr.appraisal')
                # appraisal_id = super(hr_appraisal, appraisal_obj).create(cr, uid, appraisal_values, context=context)
                appraisal_id = appraisal_obj.create(cr, uid, appraisal_values, context=context)

            return form_id

        else:
            raise osv.except_osv(_('Error!!'),_('Summation of the weights of the criterion in the form is not equal to 25.'))


class hr_appraisal_type(osv.osv):
    _name = "hr.appraisal.type"
    _columns = {
        'name': fields.char('Type'),
    }

class hr_appraisal_purpose(osv.osv):
    _name = "hr.appraisal.purpose"
    _columns = {
        'name': fields.char('Purpose'),
    }

class hr_appraisal_details(osv.osv):
    _name = "hr.appraisal.details"
    _columns = {
        'name': fields.many2one('hr.appraisal.form'),
        'sequence': fields.integer('Seq'),
        'page_title': fields.char('Page Title'),
        'criteria': fields.char('Criteria', required=True),
        'standard': fields.char('Standard', required=True),
        'weight': fields.float('Weight', required=True),
    }

class hr_appraisal_plan(osv.osv):
    _name = "hr.appraisal.plan"
    _columns = {
        'name': fields.char('Appraisal Plan', required=True),
        'active': fields.boolean('Active'),
        'month_first': fields.integer('First Appraisal (months)'),
        'month_next': fields.integer('Periodicity of Appraisal (months)'),
        # 'phase_ids': fields.one2many('hr.appraisal.plan.phase', 'name', 'Appraisal Phases'),
        'action': fields.char('Action'),
        'appraisal_form_ids': fields.many2one('hr.appraisal.form', 'Appraisal Form'),
    }
    _defaults = {
        'active': True,
        'action': 'Top-Down Appraisal',
    }

    # def create(self, cr, uid, values, context=None):
    #     total_weight = 0
    #     for each_line_item in values['appraisal_form_ids']:
    #         form_id = each_line_item[2]['appraisal_form']
    #         sql = "SELECT * FROM hr_appraisal_details WHERE name = " + str(form_id)
    #         cr.execute(sql)
    #         result = cr.dictfetchall()
    #         for each in result:
    #             print each['weight']
    #             total_weight = total_weight + each['weight']
    #
    #     if total_weight == 25:
    #         return super(hr_appraisal_plan, self).create(cr, uid, values, context=context)
    #     else:
    #         raise osv.except_osv(_('Error!!'),_('Summation of the weights of the criterion in the form(s) is not equal to 25.'))


class hr_appraisal_plan_phase(osv.osv):
    _name = "hr.appraisal.plan.phase"
    _columns = {
        'name': fields.many2one('hr.appraisal.plan'),
        'appraisal_form': fields.many2one('hr.appraisal.form', 'Appraisal Form'),
    }
#     _defaults = {
#         'action': 'Top-Down Appraisal',
#     }

class hr_appraisal(osv.osv):
    _name = "hr.appraisal"

    def _populate_employee_pin(self,cr,uid,context=None):
        sql = "SELECT employee_pin, employee_pin FROM hr_employee WHERE employee_pin IS NOT NULL ORDER BY employee_pin"
        cr.execute(sql)
        res = cr.fetchall()
        return res

    _rec_name = 'employee_id'

    _columns = {
        'state': fields.selection([
            ('draft', 'New'),
            ('pre_appraisal', 'Pre-Appraisal'),
            ('pre_appraisal_2', 'Pre-Appraisal2'),
            ('pre_appraisal_3', 'Pre-Appraisal Session'),
            ('feedback', 'Employee Feedback'),
            ('appraisal', 'Appraisal'),
            ('post_appraisal', 'Post-Appraisal'),
            ('hod_comment','HoD Comment'),
            ('hr_comment','HR Comment'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')], 'Status', required=True, readonly=True),
        'employee_pin': fields.selection(_populate_employee_pin, method="True", type="char", string="Employee PIN",required=True),
        'employee_id': fields.many2one('hr.employee', 'Employee', required=True),
        'dept_id': fields.char('Department', readonly=True),
        'appraisal_plan': fields.many2one('hr.appraisal.plan','Appraisal Form', required=True),
        'reason': fields.many2one('hr.appraisal.reasons','Reason', required=True),
        'due_date_appraisal': fields.boolean('Due Date Appraisal'),
        'responsible_person': fields.char('Responsible In-charge/ Supervisor'),
        'deadline': fields.date('Deadline Date'),
        'instruction': fields.text(''),
        'internal_notes': fields.text(''),
        'comments': fields.text(''),
        'appraisal_datetime': fields.datetime('Appraisal Date & Time'),
        'appraisal_venue': fields.many2one('hr.appraisal.venue','Appraisal Venue'),
        'description_appraisal': fields.boolean('Describe purpose and description of upcoming appraisal', required=True),
        'remainder_criterion': fields.boolean('Remainder of criterion, standard of Appraisal form', required=True),
        'performance_feedback': fields.boolean('Employee feedback on performance for last evaluation period', required=True),
        'period_accomplishments': fields.text(''),
        'improvements': fields.text(''),
        'extra_ordinary_activities': fields.text(''),
        'could_be_done': fields.text(''),
        'trainings_needed': fields.text(''),
        'problems_faced': fields.text(''),
        'appraisal_goal': fields.one2many('hr.appraisal.goal', 'name', ''),
        'next_appraisal': fields.selection([('1','Monthly'),('3', 'Quarterly'), ('6', 'Half Yearly'), ('12', 'Yearly')], 'Next Appraisal'),
        'action_plan': fields.text(''),
        # 'training_suggestion': fields.text(''),
        'training_suggestion': fields.many2many('appraisal.suggested.trainings', 'suggestion_training_rel', 'training_name', 'training_id', string=''),
        'supervisor_remarks': fields.text(''),
        'hod_comments': fields.text(''),
        'hr_comments': fields.text(''),
        'appraisal_result': fields.one2many('hr.appraisal.result', 'name', 'Summary'),
        'appraisal_questions': fields.one2many('hr.appraisal.questions', 'name', 'Appraisal Questions'),
        'appraisal_answer_total': fields.float('CPI Marks'),
        'kpi_questions': fields.one2many('hr.kpi.questions', 'name', 'Key Performance Indicator'),
        'kpi_answer_total': fields.float('KPI Marks'),
        'negative_questions': fields.one2many('hr.negative.questions', 'name', ''),
        'negative_answer_total': fields.float('Negative Marks'),
        'total_marks_scored': fields.float('Total Marks Obtained'),
        'employee_name': fields.char('Name'),

        'strength': fields.char('Strength'),
        'weakness': fields.char('Weakness'),
        'areas_of_opportunities': fields.char('Areas of Opportunities'),
        'tna': fields.char('TNR'),
        'recommendations': fields.char('Recommendations'),

        'appreciation': fields.selection([('excellent', 'Excellent'), ('very_good', 'Very Good'), ('good', 'Good'), ('average', 'Average'), ('unacceptable', 'Unacceptable')], 'Appreciation'),

        'initiation_date': fields.date('Appraisal Initiation Date', readonly=True),
    }

    _defaults = {
        'state': lambda *a: 'pre_appraisal',
        'employee_name': False,
    }

    _rec_name = 'employee_name'

    def create(self, cr, uid, value, context=None):
        # if 'negative_questions' not in value:
        #     cr.execute("SELECT criteria FROM hr_appraisal_negative_questions")
        #     r = cr.fetchall()
        #     negative_dict = []
        #     for each_item in r:
        #         negative_dict.append((0, 0, {'criteria': each_item[0]}))
        #
        #     value.update({'negative_questions': negative_dict})

        employee_id =  value['employee_id']
        appraisal_obj = self.pool.get('hr.appraisal')
        appraisal_list = appraisal_obj.search(cr, uid, [('employee_id', '=', employee_id),('state','=','done')])

        if len(appraisal_list)>0:
            last_appraisal_id = max(appraisal_list)
            appraisal_info = appraisal_obj.browse(cr, uid, last_appraisal_id, context)
            goals = appraisal_info.appraisal_goal
            previous_goals_list = []
            for each in goals:
                previous_goals_list.append([0, False, {'standard': each['standard'], 'weight': each['weight'], 'criteria': each['criteria']}])

            value.update({'appraisal_questions': previous_goals_list})

        else:
            pass

        return super(hr_appraisal, self).create(cr, uid, value, context=context)


    def on_change_pin(self, cr, uid, ids, employee_pin, context=None):
        results = {}
        temp_dict = {}

        sql = "SELECT id, name_related FROM hr_employee WHERE employee_pin = '"+str(employee_pin)+"'"
        cr.execute(sql)
        res = cr.fetchone()

        #--------------dynamic plan creation-------------------------------------

        cr.execute("SELECT id FROM hr_appraisal WHERE employee_id = "+ str(res[0]) + " AND state = 'done'")
        rows = cr.fetchall()
        if len(rows)>0:
            last_appraisal_id = max(rows)[0]
            cr.execute("SELECT criteria, standard, weight FROM hr_appraisal_goal WHERE name = "+ str(last_appraisal_id))
            res_1 = cr.fetchall()
            cr.execute("SELECT id FROM hr_appraisal_plan WHERE name = 'No Plan Needed'")
            plan_id = cr.fetchone()
            temp_dict['appraisal_plan'] = plan_id[0]
        else:
            temp_dict['appraisal_plan'] = False
        #------------------------------------------------------------------------------

        temp_dict['employee_id'] = res[0]
        temp_dict['employee_name'] = res[1]
        results['value'] = temp_dict
        return results

    def on_change_name(self, cr, uid, ids, employee_id, context=None):
        results = {}
        if employee_id is not False:
            sql = "SELECT employee_pin, parent_id, department_id FROM hr_employee WHERE id = "+str(employee_id)
            cr.execute(sql)
            res = cr.fetchone()

            if res[0] is not None:
                pin = str(res[0])
            else:
                pin = False

            if res[1] is not None:
                reporting_to_sql = "SELECT name_related FROM hr_employee WHERE id = "+str(res[1])
                cr.execute(reporting_to_sql)
                result = cr.fetchone()
                if result is not None:
                    manager = result[0]
                else:
                    manager = False
            else:
                manager = False

            if res[2] is not None:
                dept_sql = "SELECT name FROM hr_department WHERE id = "+str(res[2])
                cr.execute(dept_sql)
                result = cr.fetchone()
                if result is not None:
                    department = result[0]
                else:
                    department = False
            else:
                department = False

            results['value'] = {
                'employee_pin': pin,
                'responsible_person': manager,
                'dept_id': department,
            }
        return results


    def write(self, cr, uid, ids, value, context=None):
        appraisal_data = self.browse(cr, uid, ids, context)
        current_goal_list = []
        for each in appraisal_data:
            for each_goal in each['appraisal_goal']:
                data = {
                    'id': each_goal['id'],
                    'weight': each_goal['weight']
                }
                current_goal_list.append(data)

        obj = self.browse(cr, uid, ids, context=context)
        cpi_marks = {}
        kpi_marks = {}
        neg_marks = {}
        for each in obj:
            for each_record in each.appraisal_questions:
                cpi_marks[str(each_record.id)] = each_record.total_marks

            for each_record in each.kpi_questions:
                kpi_marks[str(each_record.id)] = each_record.total_marks

            for each_record in each.negative_questions:
                neg_marks[str(each_record.id)] = each_record.marks

        appraisal_ans_marks = 0
        if 'appraisal_questions' in value:
            for each in value['appraisal_questions']:
                if each[2] is not False:
                    if 'total_marks' in each[2].keys():
                        cpi_marks[str(each[1])] = each[2]['total_marks']

        appraisal_ans_marks = sum(cpi_marks.values())
        # print appraisal_ans_marks

        kpi_ans_marks = 0
        if 'kpi_questions' in value:
            for each in value['kpi_questions']:
                if each[2] is not False:
                    if 'total_marks' in each[2].keys():
                        kpi_marks[str(each[1])] = each[2]['total_marks']

        kpi_ans_marks = sum(kpi_marks.values())
            # print kpi_ans_marks

        neg_ans_marks = 0
        if 'negative_questions' in value:
            for each in value['negative_questions']:
                if each[2] is not False:
                    if 'marks' in each[2].keys():
                        neg_marks[str(each[1])] = each[2]['marks']

        neg_ans_marks = sum(neg_marks.values())
        # print neg_ans_marks

        value['appraisal_answer_total'] = appraisal_ans_marks
        value['kpi_answer_total'] = kpi_ans_marks
        value['negative_answer_total'] = neg_ans_marks
        value['total_marks_scored'] = appraisal_ans_marks+kpi_ans_marks+neg_ans_marks

        if 'appraisal_goal' in value:
            # print value['appraisal_goal']
            total_weight = 0
            for each_item in value['appraisal_goal']:
                if each_item[0]==0:
                    total_weight = total_weight + each_item[2]['weight']
                elif each_item[0]==1:
                    if 'weight' in each_item[2]:
                        total_weight = total_weight + each_item[2]['weight']
                    else:
                        for each in current_goal_list:
                            if each_item[1]==each['id']:
                                total_weight = total_weight + each['weight']

                elif each_item[0]==2:
                    pass
                elif each_item[0]==4:
                    cr.execute("SELECT weight FROM hr_appraisal_goal WHERE id = " + str(each_item[1]))
                    r = cr.fetchone()
                    total_weight = total_weight + r[0]
                else:
                    pass

            if total_weight != 25:
                raise osv.except_osv(_('Attention!'),_('Total weight must be equal to 25.'))



        return super(hr_appraisal, self).write(cr, uid, ids, value, context=context)


    def waiting_answer(self, cr, uid, ids, context=None):
        """Method is used to show form view in new windows"""
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'hr_evaluation_custom', 'view_hr_appraisal_form_form')
        view_id = view_ref and view_ref[1] or False,
        this = self.browse(cr, uid, ids, context=context)[0]
        return {
           'type': 'ir.actions.act_window',
           'name': 'Appraisal Form',
           'view_mode': 'form',
           'view_type': 'form',
           'view_id': view_id,
           'res_model': 'hr.appraisal.form',
           'nodestroy': True,
           # 'res_id': this.id, # assuming the many2one
           'target':'new',
           'context': context,
        }

    def review_answer(self, cr, uid, ids, context=None):
        print "review_answer called"
        return True

    def appraisal_start(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'pre_appraisal', 'initiation_date': datetime.now().date()}, context=context)
        return True

    def appraisal_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'cancel'}, context=context)
        return True

    def reset_to_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'draft'}, context=context)
        return True

    def answer_appraisal(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'feedback'}, context=context)
        return True

    def pre_appraisal_2_done(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'pre_appraisal_3'}, context=context)
        return True

    def pre_appraisal_3_done(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'feedback'}, context=context)
        return True

    def feedback_done(self, cr, uid, ids, context=None):
        value = {}
        appraisal_id = ids[0]
        data = self.browse(cr, uid, ids, context)
        for each in data:
            negative_ques_size = len(each.negative_questions)

        if negative_ques_size == 0:
            cr.execute("SELECT criteria FROM hr_appraisal_negative_questions")
            r = cr.fetchall()
            negative_dict = []
            for each_item in r:
                # negative_obj=self.pool.get('hr.negative.questions')
                negative_dict.append((0, 0, {'criteria': each_item[0]}))

                value.update({'negative_questions': negative_dict})
            # print negative_dict

            self.write(cr, uid, ids, {'state': 'appraisal', 'negative_questions': negative_dict}, context=context)
            return True
        else:
            self.write(cr, uid, ids, {'state': 'appraisal'}, context=context)
            return True

    def appraisal_done(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'post_appraisal'}, context=context)
        return True

    def post_appraisal_done(self, cr, uid, ids, context=None):
        # print self.search(cr, uid, [('id', '=', ids)])
        self.write(cr, uid, ids, {'state': 'hod_comment'}, context=context)
        return True

    def hod_comment_done(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'hr_comment'}, context=context)
        return True

    def hr_comment_done(self, cr, uid, ids, context=None):
        # strength, weakness calculation starts from here
        strength = []
        weakness = []
        areas_of_opportunities = []

        obj = self.browse(cr, uid, ids, context)
        for each in obj:
            tna = each['training_suggestion']
            recommendations = each['supervisor_remarks']

            for each_question in each['appraisal_questions']:
                print each_question['marks']
                if each_question['marks'] == '2':
                    weakness.append(each_question['criteria'])
                elif each_question['marks'] == '3':
                    areas_of_opportunities.append(each_question['criteria'])
                elif each_question['marks'] == '4':
                    strength.append(each_question['criteria'])

            weakness_str = ''
            for every in weakness:
                weakness_str = every + ', ' + str(weakness_str)
            strength_str = ''
            for every in strength:
                strength_str = every + ', ' + str(strength_str)
            areas_of_opportunities_str = ''
            for every in areas_of_opportunities:
                areas_of_opportunities_str = every + ', ' + str(areas_of_opportunities_str)

            if len(weakness_str) == 0:
                weakness_str = False
            if len(strength_str) == 0:
                strength_str = False
            if len(areas_of_opportunities_str) == 0:
                areas_of_opportunities_str = False

        # strength, weakness calculation ends here
        values = {
            'state': 'done',
            'strength': strength_str,
            'weakness': weakness_str,
            'areas_of_opportunities': areas_of_opportunities_str,
            'tna': tna,
            'recommendations': recommendations,
        }
        self.write(cr, uid, ids, values, context=context)

class hr_appraisal_reasons(osv.osv):
    _name = 'hr.appraisal.reasons'
    _columns = {
        'name': fields.char('Reason'),
    }

class hr_appraisal_venue(osv.osv):
    _name = 'hr.appraisal.venue'
    _columns = {
        'name': fields.char('Appraisal Venue')
    }

class hr_appraisal_goal(osv.osv):
    _name = 'hr.appraisal.goal'
    _columns = {
        'name': fields.many2one('hr.appraisal'),
        'criteria': fields.char('Goal'),
        'weight': fields.float('Weight'),
        'standard': fields.char('Standard'),
    }

class hr_appraisal_result(osv.osv):
    _name = 'hr.appraisal.result'
    _columns = {
        # 'employee_id': fields.many2one('hr.employee', 'Employee'),
        # 'employee_pin': fields.char('Employee PIN'),
        # 'department': fields.many2one('hr.department', 'Department'),
        'name': fields.many2one('hr.appraisal'),
        'employee_name': fields.char('Employee'),
        'department': fields.char('Department'),
        'strength': fields.char('Strength'),
        'weakness': fields.char('Weakness'),
        'areas_of_opportunities': fields.char('Areas of Opportunities'),
        'percentage_of_marks': fields.float('Percentage of Marks'),
        'tna': fields.char('TNR'),
        'recommendations': fields.char('Recommendations'),
    }

class hr_appraisal_questions(osv.osv):
    _name = 'hr.appraisal.questions'
    _columns = {
        'name': fields.many2one('hr.appraisal'),
        'form_id': fields.integer(),
        'criteria': fields.char('Criteria'),
        'weight': fields.float('Weight'),
        'standard': fields.char('Standard'),
        'marks': fields.selection(
            [('0', 'Unsatisfactory(0)'),
             ('2', 'Improvement Needed(2)'),
             ('3', 'Good(3)'),
             ('4', 'Outstanding(4)')], 'Marks'),
        'total_marks': fields.float('Total Marks'),
        'remarks': fields.char('Remarks'),
    }

    def ques_marks_change(self, cr, uid, ids, weight, marks, context=None):
        res = {}
        marks = float(marks)
        total_marks = marks*weight
        res['value'] = {
            'total_marks': total_marks,
        }
        return res

class hr_kpi_questions(osv.osv):
    _name = 'hr.kpi.questions'
    _columns = {
        'name': fields.many2one('hr.appraisal'),
        'criteria': fields.char('Criteria'),
        'weight': fields.float('Weight'),
        'standard': fields.char('Standard'),
        'marks': fields.selection(
            [('0', 'Unsatisfactory(0)'),
             ('2', 'Improvement Needed(2)'),
             ('3', 'Good(3)'),
             ('4', 'Outstanding(4)')], 'Marks'),
        'total_marks': fields.float('Total Marks'),
        'remarks': fields.char('Remarks'),
    }

    def kpi_marks_change(self, cr, uid, ids, weight, marks, context=None):
        res = {}
        marks = float(marks)
        total_marks = marks*weight
        res['value'] = {
            'total_marks': total_marks,
        }
        return res

class hr_negative_questions(osv.osv):
    _name = 'hr.negative.questions'
    _columns = {
        'name': fields.many2one('hr.appraisal'),
        'criteria': fields.char('Criteria'),
        'answer': fields.selection([
            ('0', 'Yes'),
            ('-5', 'No'),
            ], 'Answer'),
        'marks': fields.float('Marks'),
        'remarks': fields.char('Remarks'),
    }

    def answer_on_change(self, cr, uid, ids, answer, context=None):
        res = {}
        if answer == '-5':
            marks = -5
        else:
            marks = 0
        res['value']={
            'marks': marks
        }
        return res

class hr_appraisal_negative_questions(osv.osv):
    _name = "hr.appraisal.negative.questions"
    _columns = {
        'criteria': fields.char('Criteria'),
    }

class appraisal_suggested_trainings(osv.osv):
    _name = "appraisal.suggested.trainings"
    _columns = {
        'name': fields.char('Training Name'),
        'training': fields.many2many('hr.appraisal', 'suggestion_training_rel', 'training_id', 'training_name', string='Training Name'),
    }