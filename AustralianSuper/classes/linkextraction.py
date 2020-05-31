class Extraction:
    def __init__(self):
        self.filename = 'source/agmnts.txt'

        self.agmnts = self.get_ag_list()
        self.links = self.agmnt_to_link()


    def agmnt_to_link(self):
        lstart = 'https://www.fwc.gov.au/documents/documents/agreements/fwa/'
        lend = '.pdf'
        link_list = list()
        for i in self.agmnts:
            link_list.append(lstart + i + lend)
        return link_list


    def get_ag_list(self):
        f = open(self.filename, "r")
        contents = f.read()
        aglist = contents.split("\n")
        for a in aglist:
            if len(a) < 3:
                aglist.remove(a)
        return aglist

    def get_agmnts(self):
        return self.agmnts

    def get_links(self):
        return self.links

