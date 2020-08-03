from selenium import webdriver
import pyinputplus, time, csv

def log_in():
    print('Logging in...')
    emailInputElem = browser.find_element_by_name('username')
    pwInputElem = browser.find_element_by_name('password')

    emailInputElem.send_keys(my_email)
    pwInputElem.send_keys(my_password)
    pwInputElem.submit()

def enter_ADD_page():
    print('Entering ADD page...')
    addElem = browser.find_element_by_link_text('Add')
    addElem.click()

def get_data(filename):
    print(filename)
    with open(filename) as file:
        print('Getting data...')
        reader = csv.reader(file)
        next(reader) # skip the header row

        # num_of_words = len(list(reader))
        # It's not len() which is causing the generator to reach the end,
        # but it's the list() which turns the generator into a list by taking
        # an item one by one from the iterator, resulting in the generator being
        # exhausted (i.e finished).

        eng_words, thai_words, pronunciations, comments = [], [], [], []

        for row in reader:
            eng_words.append(row[1])
            thai_words.append(row[2])
            pronunciations.append(row[3])
            comments.append(row[4])

        num_of_words = len(eng_words)
        return num_of_words, eng_words, thai_words, pronunciations, comments

def enter_data(eng_word, thai_word, pronunciation, comment):
    deckElem = browser.find_element_by_id('deck')
    frontElem = browser.find_element_by_id('f0')
    backElem = browser.find_element_by_id('f1')
    saveElems = browser.find_elements_by_tag_name('button')

    deckElem.clear()
    deckElem.send_keys(my_deck)
    frontElem.send_keys(eng_word)
    backElem.send_keys(f"{thai_word}\n{pronunciation}\n{comment}")

    time.sleep(1)
    saveElems[1].click()

def create_flashcards():
    print('Creating flashcards...')
    num_of_words, eng_words, thai_words, pronunciations, comments = get_data(my_word_list)

    for i in range(0, num_of_words):
        print(f"Creating card {i+1}/{num_of_words}...")
        enter_data(eng_words[i], thai_words[i], pronunciations[i], comments[i])
        time.sleep(2)

my_email = input('Enter email: ')
my_password = pyinputplus.inputPassword(prompt='Enter password: ')
my_deck = 'Testing'
my_word_list = 'data/testing.csv'

print('Opening the website...')
browser = webdriver.Firefox()
browser.get('https://ankiweb.net/account/login')
time.sleep(1)
log_in()
time.sleep(3)
enter_ADD_page()
time.sleep(3)
create_flashcards()
print('Done')
