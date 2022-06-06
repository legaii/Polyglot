import sys
import random
from recordclass import recordclass

def read_file(file_name, delimiter):
  with open(file_name, "r") as f:
    return [tuple(line.split(delimiter)) for line in f.readlines()]

def write_file(file_name, delimiter, data):
  with open(file_name, "w") as f:
    for t in data:
      f.write(delimiter.join(t) + "\n")

MAX_LEVEL = 10
QUIZ_SIZE = 100
DELIMITER = " = "

def sort_by_question(items):
  by_question = {}
  for item in items:
    if item.question not in by_question:
      by_question[item.question] = []
    by_question[item.question].append(item.answer)
  return by_question

def sort_by_level(items):
  by_level = [[] for level in range(MAX_LEVEL + 1)]
  for i, item in enumerate(items):
    by_level[item.level].append(i)
  for lst in by_level:
    random.shuffle(lst)
  return by_level

def main():
  assert len(sys.argv) == 2
  file_name = sys.argv[1]
  Item = recordclass("Item", "question answer level")
  items = [Item(question, answer, int(level)) for question, answer, level in read_file(file_name, DELIMITER)]
  by_question = sort_by_question(items)
  by_level = sort_by_level(items)
  quiz = []
  quiz_ = []
  for i, lst in enumerate(reversed(by_level)):
    for j in lst:
      if len(quiz) < QUIZ_SIZE // (MAX_LEVEL + 1) * (i + 1):
        quiz.append(j)
      else:
        quiz_.append(j)
  random.shuffle(quiz_)
  for j in quiz_:
    if len(quiz) < QUIZ_SIZE:
      quiz.append(j)
  assert len(quiz) == QUIZ_SIZE
  random.shuffle(quiz)
  score = 0
  j = 0
  while j < len(quiz):
    i = quiz[j]
    item = items[i]
    print(f"{j + 1}.", item.question, "{" + str(item.level) + "}")
    answer = input()
    if answer == "/exit":
      break
    if answer == item.answer:
      if j < QUIZ_SIZE:
        if item.level < MAX_LEVEL:
          item.level += 1
        score += 1
      j += 1
      print("OK")
    elif answer in by_question[item.question]:
      print("PE")
    else:
      if j < QUIZ_SIZE:
        item.level = 0
      quiz.append(i)
      j += 1
      print("WA:", item.answer)
  print()
  print("THE END")
  print(score, "/", QUIZ_SIZE)
  print()
  write_file(file_name, DELIMITER, [(item.question, item.answer, str(item.level)) for item in items])

if __name__ == "__main__":
  main()

