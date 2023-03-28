class Admission:
    def __init__(self, name=None, sum=None, additional=None, psychometric=None, min_final_grade_average=None, without=None, notes=None, date=None, *args, **kwargs):
        super(Admission, self).__init__(*args, **kwargs)
        self.name = name
        self.sum = sum
        self.additional = additional
        self.psychometric = psychometric
        self.min_final_grade_average = min_final_grade_average
        self.without = without
        self.notes = notes
        self.date = date


    def get_mongo(self):
        return dict(vars(self))
