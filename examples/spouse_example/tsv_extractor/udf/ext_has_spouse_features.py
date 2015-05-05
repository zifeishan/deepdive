#! /usr/bin/env python

import sys
import ddlib     # DeepDive python utility

ARR_DELIM = '~^~'

# For each input tuple
for row in sys.stdin:
  parts = row.strip().split('\t')
  if len(parts) != 6: 
    print >>sys.stderr, 'Failed to parse row:', row
    continue
  
  # Get all fields from a row
  words = parts[0].split(ARR_DELIM)
  relation_id = parts[1]
  p1_start, p1_length, p2_start, p2_length = [int(x) for x in parts[2:]]

  # Unpack input into tuples.
  span1 = ddlib.Span(begin_word_id=p1_start, length=p1_length)
  span2 = ddlib.Span(begin_word_id=p2_start, length=p2_length)

  # Features for this pair come in here
  features = set()
  
  # Feature 1: Bag of words between the two phrases
  words_between = ddlib.tokens_between_spans(words, span1, span2)
  for word in words_between.elements:
    features.add("word_between=" + word)

  # Feature 2: Number of words between the two phrases
  features.add("num_words_between=%s" % len(words_between.elements))

  # Feature 3: Does the last word (last name) match?
  last_word_left = ddlib.materialize_span(words, span1)[-1]
  last_word_right = ddlib.materialize_span(words, span2)[-1]
  if (last_word_left == last_word_right):
    features.add("potential_last_name_match")

  ######################## 
  # Improved Feature Set #
  ########################

  # # Feature 1: Find out if a lemma of marry occurs.
  # # A better feature would ensure this is on the dependency path between the two.
  # words_between = ddlib.tokens_between_spans(words, span1, span2)
  # lemma_between = ddlib.tokens_between_spans(obj["lemma"], span1, span2)
  # married_words = ['marry', 'widow', 'wife', 'fiancee', 'spouse']
  # non_married_words = ['father', 'mother', 'brother', 'sister', 'son']
  # # Make sure the distance between mention pairs is not too long
  # if len(words_between.elements) <= 10:
  #   for mw in married_words + non_married_words:
  #     if mw in lemma_between.elements: 
  #       features.add("important_word=%s" % mw)

  # # Feature 2: Number of words between the two phrases
  # # Intuition: if they are close by, the link may be stronger.
  # l = len(words_between.elements)
  # if l < 5: features.add("few_words_between")
  # else: features.add("many_words_between")

  # # Feature 3: Does the last word (last name) match?
  # last_word_left = ddlib.materialize_span(words, span1)[-1]
  # last_word_right = ddlib.materialize_span(words, span2)[-1]
  # if (last_word_left == last_word_right):
  #   features.add("potential_last_name_match")

  #######################

  # # Use this line if you want to print out all features extracted:
  # ddlib.log(features)

  for feature in features:  
    print str(relation_id) + '\t' + feature
