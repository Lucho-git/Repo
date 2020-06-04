from classes.agreement import Agreement


class Extraction:
    def __init__(self):
        self.filename = 'source/agmnts.txt'
        self.f_agreement = "source/agreements.txt"

        self.agmnts = list()
        self.links = list()
        self.agreements = self.get_agreement_list()

    def agmnt_to_link(self, ag):
        lstart = 'https://www.fwc.gov.au/documents/documents/agreements/fwa/'
        lend = '.pdf'
        return lstart + ag + lend


    def get_ag_list(self):
        f = open(self.filename, "r")
        contents = f.read()
        aglist = contents.split("\n")
        for a in aglist:
            if len(a) < 3:
                aglist.remove(a)
        return aglist

    def get_agreement_list(self):
        f = open(self.f_agreement, "r")
        contents = f.read()
        retlist = list()
        aglist = contents.split("\n")
        for a in aglist:
            linelist = list()
            sublist = a.split("\t")
            for s in sublist:
                if s and s.strip():
                    linelist.append(s)
            if a:
                '''maybe change this to a list, and create the agreements in main'''
                if 8 > len(linelist) > 1:
                    print("Missing Values for arg: " + linelist[1])
                elif len(linelist) > 0:
                    ag = Agreement(linelist[0], linelist[1], linelist[2], linelist[3], linelist[4], linelist[5],
                                   linelist[6], linelist[7], self.agmnt_to_link(linelist[1]))
                    self.agmnts.append(ag.agmnt)
                    self.links.append(ag.link)
                    retlist.append(ag)

        return retlist


    def get_agmnts(self):
        return self.agmnts

    def get_links(self):
        return self.links

    def get_arguments(self):
        return self.agreements