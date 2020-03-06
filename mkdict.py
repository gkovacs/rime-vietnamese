from collections import Counter
import bogo
weights = Counter()
rules = bogo.get_telex_definition()

def capitalize_first_letter_of_word(word):
  return word[0].upper() + word[1:]

def capitalize_first_letter_of_all_words(words):
  return ' '.join([capitalize_first_letter_of_word(word) for word in words.split(' ')])

def get_variants(telex):
  output = [telex]
  if 'uwow' in telex:
    output.extend(get_variants(telex.replace('uwow', 'uow')))
  if telex[0] in 'abcdefghijklmnopqrstuvwxyz':
    output.extend(get_variants(capitalize_first_letter_of_all_words(telex)))
  return output

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
  if telex == '':
    continue
  for telex in get_variants(telex):
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
