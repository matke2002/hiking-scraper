class DestinationData:
    def __init__(self):
        self.klub = ''
        self.title = ''
        self.url = ''
        self.country = ''
        self.location = ''
        self.price = ''
        self.desc = ''
        self.date_start = ''
        self.date_end = ''
        self.date_str = ''
    def __str__(self):
        return self.klub + ": " +  self.title + ": " + str(self.date_start) + "-" +  str(self.date_end) + " " + self.url + " " + self.location + " " + self.desc

    def __iter__(self):
        return iter([self.klub, self.title, self.date_start.strftime('%Y-%m-%d'), self.date_end.strftime('%Y-%m-%d'), self.url, self.desc])
