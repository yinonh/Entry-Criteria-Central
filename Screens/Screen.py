
class Screen:
    name = ''
    icon = ''

    def __init__(self, data, *args, **kwargs):
        super(Screen, self).__init__(*args, **kwargs)
        self.data = data

    def build(self):
        pass