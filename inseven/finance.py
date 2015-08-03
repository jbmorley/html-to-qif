class Record(object):

    def __init__(self):
        self.date = None
        self.value = 0
        self.description = ""
        self.balance = None

    def __str__(self):
        date = self.date.strftime("%d/%m/%Y")
        return "D%s\nT%.02f\nP%s\n^\n" % (date, self.value, self.description)
