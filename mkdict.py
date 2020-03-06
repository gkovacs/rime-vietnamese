from collections import Counter
import bogo
weights = Counter()
rules = bogo.get_telex_definition()

outfile = open('vietnamese.dict.yaml', 'wt')
is_started = False
for line in open('hannom.dict.yaml'):
  line = line.strip()
  if not is_started:
    if line == '...':
      is_started = True
    continue
  if '#' in line:
    line = line[:line.index('#')].strip()
  parts = line.split('\t')
  weight = 1
  if len(parts) == 3:
    weight = int(parts[2])
  elif len(parts) != 2:
    continue
  telex = parts[1].strip()
  weights[telex] += weight
  if 'uwow' in telex:
    telex = telex.replace('uwow', 'uow')
    weights[telex] += weight

print('''# Rime dictionary
# encoding: utf-8
---
name: vietnamese
version: "2013.07.10"
sort: original
use_preset_vocabulary: false
max_phrase_length: 7
min_phrase_weight: 100
...
''', file=outfile)

for telex,weight in weights.items():
  vietnamese = bogo.process_sequence(telex.replace('z', ''), rules=rules).strip()
  print('\t'.join(map(str, [vietnamese + ' ', telex, weight])), file=outfile)
