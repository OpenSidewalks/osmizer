class OSMIDGenerator:
    def __init__(self, start_num=-1, step_num=-1):
        if start_num >= 0 or step_num >=0:
            raise ValueError('start_number and step cannot be 0 or positive')
        self.currentNum = start_num
        self.step = step_num

    def get_next(self):
        self.currentNum += self.step
        return self.currentNum