from datetime import datetime, timedelta

class Spread:
    def __init__(self):
        self.all = list()
        self.opportunity = "N/A"
        self.amwu = None                      # big union
        self.awu = None                       # big union
        self.uv = None                        # big union
        self.fsu = None                       # big union
        self.rtbu = None                      # big union
        self.tcfu = None                      # big union
        self.meau = None                      # big union
        self.asu = None                       # big union
        self.other = None                     # not one of the big unions
        self.no_union = None                  # no union in document
        self.name_union = None                # name of smaller union
        self.negotiator = "N/A"               # secret
        self.education_manager = "N/A"        # secret
        self.bmp_am = "N/A"                   # secret
        self.employer_an = "N/A"              # secret
        self.employer = None                  # ???
        self.abn = None                       # companies abn
        self.agreement_name = None            # name of the agreement
        self.ag_id = None                     # agreement Id Number
        self.p_id = None                      # print id number
        self.odn = "N/A"                      # ???
        self.prev_ag = "N/A"                  # Previous agreement name
        self.prev_ag_id = "N/A"               # Previous agreement ID
        self.industry = None                  # Related Industry name
        self.o_date = None                    # Opperative Date
        self.e_date = None                    # Expiry Date
        self.nine_prior = None                # 9 months before Expiry
        self.approval = None                  # First Listed City of the document
        self.coverage = None                  # ??
        self.region = None                    # area agreement made in ??
        self.d_status = None                  # Default status, probably if employee has a choice for there super
        self.fund_type = None                 # Type of fund for selected super company
        self.d_fund = "N/A"                   # Name of default fund
        self.c_fund = "N/A"                   # Name of choice fund
        self.other_funds = None               # Other funds that appear in the agreement
        self.link = None                      # link to the agreement


    def set_unions(self):
        pass

    def set_nine_prior(self):
        f_date = datetime.strptime(self.e_date, '%d %B %Y')
        self.nine_prior = f_date - timedelta(274)
        self.nine_prior = self.nine_prior.strftime('%d %B %Y')

    def set_agreement_values(self, link, ag_id, agreement_name, p_id, industry, o_date, e_date):
        self.link = link
        self.ag_id = ag_id
        self.agreement_name = agreement_name
        self.p_id = p_id
        self.industry = industry
        self.o_date = o_date
        self.e_date = e_date

    # adds the approval city field
    def set_approval(self, approval):
        self.approval = approval

    def make_list(self):
        # append all fields to a list
        self.all = list()
        self.all.append(self.opportunity)
        self.all.append(self.amwu)
        self.all.append(self.awu)
        self.all.append(self.uv)
        self.all.append(self.fsu)
        self.all.append(self.rtbu)
        self.all.append(self.tcfu)
        self.all.append(self.meau)
        self.all.append(self.asu)
        self.all.append(self.other)
        self.all.append(self.no_union)
        self.all.append(self.name_union)
        self.all.append(self.negotiator)
        self.all.append(self.education_manager)
        self.all.append(self.bmp_am)
        self.all.append(self.employer_an)
        self.all.append(self.employer)
        self.all.append(self.abn)
        self.all.append(self.agreement_name)
        self.all.append(self.ag_id)
        self.all.append(self.p_id)
        self.all.append(self.odn)
        self.all.append(self.prev_ag)
        self.all.append(self.prev_ag_id)
        self.all.append(self.industry)
        self.all.append(self.o_date)
        self.all.append(self.e_date)
        self.all.append(self.nine_prior)
        self.all.append(self.approval)
        self.all.append(self.coverage)
        self.all.append(self.region)
        self.all.append(self.d_status)
        self.all.append(self.fund_type)
        self.all.append(self.d_fund)
        self.all.append(self.c_fund)
        self.all.append(self.other_funds)
        self.all.append(self.link)
        return self.all

    def format_spread(self):
        self.all = list()
        self.all.append(self.opportunity)
        self.all.append(self.amwu)
        self.all.append(self.awu)
        self.all.append(self.uv)
        self.all.append(self.fsu)
        self.all.append(self.rtbu)
        self.all.append(self.tcfu)
        self.all.append(self.meau)
        self.all.append(self.asu)
        self.all.append(self.other)
        self.all.append(self.no_union)
        self.all.append(self.name_union)
        self.all.append(self.negotiator)
        self.all.append(self.education_manager)
        self.all.append(self.bmp_am)
        self.all.append(self.employer_an)
        self.all.append(self.employer)
        self.all.append(self.abn)
        self.all.append(self.agreement_name)
        self.all.append(self.ag_id)
        self.all.append(self.p_id)
        self.all.append(self.odn)
        self.all.append(self.prev_ag)
        self.all.append(self.prev_ag_id)
        self.all.append(self.industry)
        self.all.append(self.o_date)
        self.all.append(self.e_date)
        self.all.append(self.nine_prior)
        self.all.append(self.approval)
        self.all.append(self.coverage)
        self.all.append(self.region)
        self.all.append(self.d_status)
        self.all.append(self.fund_type)
        self.all.append(self.d_fund)
        self.all.append(self.c_fund)
        self.all.append(self.other_funds)
        self.all.append(self.link)
        outstring = ""
        for s in self.all:
            outstring += str(s) + "\t"
        outstring += "\n"
        return outstring
