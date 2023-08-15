import re
from rule import Rule


class RuleParser(object):
  """
  fact - variable-free tuples
  pattern - tuples with some variables
  rule - has a list of patterns in its premise
  Rules will follow this grammar:
  <premise>\n  => <consequence>
  <premise> := (pattern, [pattern, ...])
  <consequence> := fact
  fact = (\w+)\s+
  pattern = fact | \w+ <\w+> \w+ variable is enclosed in angle brackets
  """
  rule_regex = r"^(?P<premise>.+)\n\s*=>\s*(?P<consequence>.+)$"
  pattern_regex = r"<([^>]+)>"
  
  def parse(self, rule):
    match = re.match(self.rule_regex, rule)
    if match:
      premise = match.group('premise').strip()
      consequence = match.group('consequence').strip()
      return Rule(premise, consequence)
    else:
      raise ValueError("Invalid rule format")


if __name__ == "__main__":
  rule_parser = RuleParser()
  
  fact_fact_input = """apple is ripe
  => eat it"""
  rule = rule_parser.parse(input)
  print(rule)
  
  patterns_fact_input = """<apple> is ripe, <banana> is ripe
  => eat it"""
  rule = rule_parser.parse(input)
  print(rule)