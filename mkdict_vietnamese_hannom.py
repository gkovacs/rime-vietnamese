from collections import Counter, defaultdict
import bogo
rules = bogo.get_telex_definition()

def capitalize_first_letter_of_word(word):
  return word[0].upper() + word[1:]

def capitalize_first_letter_of_all_words(words):
  return ' '.join([capitalize_first_letter_of_word(word) for word in words.split(' ')])

def get_variants(telex):
  output = [telex]
  if telex[0] in 'abcdefghijklmnopqrstuvwxyz':
    output.extend(get_variants(capitalize_first_letter_of_all_words(telex)))
  if 'uwow' in telex:
    output.extend(get_variants(telex.replace('uwow', 'uow')))
  return list(set(output))

vietnamese_to_hannom_to_weight = defaultdict(Counter)

outfile = open('vietnamese_hannom.dict.yaml', 'wt')
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
  hannom = parts[0].strip()
  vietnamese_to_hannom_to_weight[telex][hannom] += weight
  #for telex in get_variants(telex):
  #  vietnamese = telex #bogo.process_sequence(telex.replace('z', ''), rules=rules).strip()
  #  vietnamese_to_hannom_to_weight[vietnamese][hannom] += weight

print('''# Rime dictionary
# encoding: utf-8
---
name: vietnamese_hannom
version: "2013.07.10"
sort: original
use_preset_vocabulary: false
...
''', file=outfile)

def sorted_descending_by_weight(d):
  return [y[0] for y in sorted(list(d.items()), key=lambda x: x[1], reverse=True)]

full_width_space = '　'
for vietnamese,hannom_to_weight in vietnamese_to_hannom_to_weight.items():
  hannom_list = sorted_descending_by_weight(hannom_to_weight)
  for telex in get_variants(vietnamese):
    for hannom in hannom_list:
      print('\t'.join(map(str, [hannom, telex, hannom_to_weight[hannom]])), file=outfile)