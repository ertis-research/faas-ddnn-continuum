from pulsar import Function

class EchoFunction(Function):
  def __init__(self):
    pass

  def process(self, input, context):
    return str(input)
