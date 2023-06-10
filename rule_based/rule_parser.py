import re
from rule import Rule


class RuleParser(object):
  """Rules will follow this grammar:
  <premise>\n  => <consequence>
  """
  rule_regex = r"^(?P<premise>.+)\n\s*=>\s*(?P<consequence>.+)$"
  
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
  input = """apple is ripe
  => eat it"""
  rule = rule_parser.parse(input)
  print(rule)