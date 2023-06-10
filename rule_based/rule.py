
class Rule(object):
  def __init__(self, premise, consequence, weight=1.0):
    self._premise = premise
    self._consequence = consequence
    self._weight = weight
  
  def __str__(self) -> str:
    return f"(Premise: '{self._premise}' => Consequence: '{self._consequence}' [weight: {self._weight}])"