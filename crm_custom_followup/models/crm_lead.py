from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    follow_up_level = fields.Integer(string="Follow Up Level", default=0)
    
    # Set lead to Interested stage when call is connected and customer shows interest
    def action_call_connected_interested(self):
        for lead in self:
            lead.stage_id = self.env.ref('crm_custom_followup.stage_interested').id
            
    # Set lead to Not Interested stage when call is connected and customer shows interest
    def action_call_connected_not_interested(self):
        for lead in self:
            lead.stage_id = self.env.ref('crm_custom_followup.stage_not_interested').id


    def action_call_not_connected(self):
        for lead in self:
            # Prevent follow-up if already in a final state
            if lead.stage_id.id in [
                self.env.ref('crm_custom_followup.stage_sale').id,
                self.env.ref('crm_custom_followup.stage_disqualified').id,
                self.env.ref('crm_custom_followup.stage_not_interested').id,
            ]:
                continue  # Skip this lead
    
            if lead.follow_up_level < 7:
                lead.follow_up_level += 1
                next_stage = self.env.ref(f'crm_custom_followup.stage_follow_up_{lead.follow_up_level}')
                lead.stage_id = next_stage.id
            else:
                #Mark as disqualified after 7 attempts
                lead.stage_id = self.env.ref('crm_custom_followup.stage_disqualified').id

    
    # Manually move the lead to the May Buy Later stage
    def action_may_buy_later(self):
        for lead in self:
            lead.stage_id = self.env.ref('crm_custom_followup.stage_may_buy_later').id
    
    # Manually disqualify the lead and move it to the Disqualified stage
    def action_disqualify(self):
        for lead in self:
            lead.stage_id = self.env.ref('crm_custom_followup.stage_disqualified').id
            
   
    # Scheduler for automatically convert leads in the Interested stage to the SALE stage.
    def auto_convert_interested_to_sale(self):
        interested_stage = self.env.ref('crm_custom_followup.stage_interested')
        sale_stage = self.env.ref('crm_custom_followup.stage_sale')
        leads = self.search([('stage_id', '=', interested_stage.id)])
        for lead in leads:
            lead.stage_id = sale_stage.id


    