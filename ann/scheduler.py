
class Scheduler:
  def __init__(self) -> None:
    self.propagating = False
    self.time = 0
    self.scheduled = {}

  def start(self, starting_objects):
    self.propagating = True
    
    while self.propagating:
      # check inputs
      for obj in starting_objects:
        obj.activate(self.time)
      self.run_scheduled(self.time)
      self.time += 1

  def add(self, time, neuron):
    if time not in self.scheduled:
      self.scheduled[time] = [neuron]
    elif neuron not in self.scheduled[time]:
      self.scheduled[time].append(neuron)

  def run_scheduled(self, time):
    if time not in self.scheduled:
      print(f'nothing scheduled for time {time}. stop.')
      self.propagating = False
      return
    
    for neuron in self.scheduled[time]:
      neuron.activate(time)
    


# (t=0) sensor (=axon) -> dendrite -> neuron (+t) -> 
# -> axon -> dendrite -> neuron (+t) -> ...