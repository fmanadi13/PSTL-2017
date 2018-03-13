class Stream():

    def __init__(self, sequence):
        self.sequences = sequence.splitlines()
        self.totalLines = len(self.sequences)
        self.lineNumber = 0

    def peekNextLine(self):
        return self.hasNext() and self.sequences[self.lineNumber] or None

    def getNextLine(self):
        if self.hasNext():
            self.lineNumber += 1
            return self.sequences[self.lineNumber - 1]
        else:
            return None

    def hasNext(self):
        return self.lineNumber < self.totalLines

