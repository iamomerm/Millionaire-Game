from prettytable import PrettyTable
import random
from questions import Questions

def valid_input(excluded_options=[]):
    while True:
        options = ['1', '2', '3', '4', 'FRIEND', '50:50', 'EXIT']
        for excluded_option in excluded_options:
            options.remove(excluded_option)
        value = input("[Gamebot] Answer (%s): " % options).upper()
        if value not in options:
            print('[Gamebot] Invalid Answer: %s (Accepted Answers: %s)' % (value, options))
        else:
            return value

def check_answer(user_input, correct_answer_idx):
    try:
        if int(user_input) == correct_answer_idx:
            return True
        return False
    except ValueError:
        return False

def create_table(question):
    table = PrettyTable([question['question'] + ' ?'])
    for i in range(4):
        table.add_row([str(i + 1) + '. ' + question['answers'][i]])
    table.align = 'l'
    return table

def choose_random_question(questions):
    return random.choice(questions)

def friend_help(correct_answer):
    weights = []
    answers = list(range(1, 5))
    for answer in answers:
        if answer == correct_answer:
            weights.append(75)
        else:
            weights.append(25 / 3)
    print("[Gamebot] I'm Pretty Sure the Answer is: %d" % random.choices(answers, weights)[0])

def fifty_fifty(correct_answer):
    answers = list(range(1, 5))
    answers.remove(correct_answer)
    random_incorrect_answer = random.choice(answers)
    answers.remove(random_incorrect_answer)
    result = [random_incorrect_answer, correct_answer]
    result.sort()
    print('[Gamebot]', result)
    return [str(answer) for answer in answers]

# Game
balance = 0

while True:
    random_question = choose_random_question(Questions)
    Questions.remove(random_question)
    print(create_table(random_question))
    value = valid_input()
    # Friend
    if value == 'FRIEND':
        friend_help(random_question['correct_answer'])
        value = valid_input(['FRIEND', '50:50'])
    # 50:50
    elif value == '50:50':
        result = fifty_fifty(random_question['correct_answer'])
        value = valid_input(['FRIEND', '50:50', result[0], result[1]])
    if check_answer(value, random_question['correct_answer']):
        balance += 100000
        if balance == 1000000:
            print('\nYou Won!')
            break
        print('\n[Gamebot] You are Correct! (Balance: %d$)' % balance)
    else:
        print('[Gamebot] Game Over! (Balance: %d$)' % balance)
        break
