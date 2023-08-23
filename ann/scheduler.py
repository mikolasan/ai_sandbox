
class Scheduler:
  def __init__(self) -> None:
    self.propagating = False
    self.time = 0
    self.scheduled = {}

  def start(self, starting_objects):
    for obj in starting_objects:
      obj.activate(self.time)
    
    self.propagating = True
    
    while self.propagating:
      self.run_scheduled(self.time)
      self.time += 1

  def add(self, time, run_fn):
    if time not in self.scheduled:
      self.scheduled[time] = [run_fn]
    else:
      self.scheduled[time].append(run_fn)

  def run_scheduled(self, time):
    if time not in self.scheduled:
      print(f'nothing scheduled for time {time}. stop.')
      self.propagating = False
      return
    
    for run_fn in self.scheduled[time]:
      run_fn(time)
    


# (t=0) sensor (=axon) -> dendrite -> neuron (+t) -> 
# -> axon -> dendrite -> neuron (+t) -> ...