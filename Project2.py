from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """

    with open(filename) as fp:
        soup = BeautifulSoup(fp, "html.parser")
    book_tags = soup.find_all('a', class_ = 'bookTitle')
    book_list = []
    for tag in book_tags:
        book_list.append(tag.text.strip())
    author_tags = soup.find_all('a', class_ = 'authorName')
    author_list = []
    for tag in author_tags:
        author_list.append(tag.text.strip())
    book_and_author = list(zip(book_list, author_list))
    return book_and_author

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """

    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    tags = soup.find('table', class_= "tableList")
    tags2 = tags.find_all('tr')
    book_list = []
    for tag2 in tags2[0:10]:
        book_url = tag2.find('a', class_ = "bookTitle")['href']
        book_url.strip()
        book_url2 = "https://www.goodreads.com" + book_url
        book_list.append(book_url2)
    return book_list
    

    
def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    resp = requests.get(book_url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    tags = soup.find('body')
    tags2 = tags.find('div', class_ = "content")
    tags3 = tags2.find('div', class_ = "mainContentContainer")
    tags4 = tags3.find('div', class_ = "mainContent")
    tags5 = tags4.find('div', class_ = "leftContainer")
    tags6 = tags5.find('div', class_ = 'last col stacked')
    tags7 = tags6.find('div', class_ = 'last col')
    book_title = tags7.find('h1', class_ ='gr-h1 gr-h1--serif').text.strip()
    
    
    tags8 = tags7.find('div')
    tags9 = tags8.find_all('span')[1]
    tags10 = tags9.find('div', class_ = "authorName__container")
    author_name = tags10.find('a', class_ = "authorName").text.strip()
    
    tags11 = tags6.find('div', class_ = "uitext darkGreyText")
    pagenumbers = int(tags11.find('span', itemprop = 'numberOfPages').text.strip()[0:3])
    
    return (book_title, author_name, pagenumbers)


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    with open(filepath) as f:
        soup = BeautifulSoup(f, "html.parser")
    tags = soup.find_all('h4', class_ = 'category__copy')
    categories_list = []
    for tag in tags:
        categories_list.append(tag.text.strip())
    book_titles = []
    book_tags = soup.find_all('div', class_ = 'category__winnerImageContainer')
    for book_tag in book_tags:
        title_tags = book_tag.find_all('img', alt = True)
        for title_tag in title_tags:
            book_titles.append(title_tag['alt'])
    tags2 = soup.find_all('div', class_ = "category clearFix")
    url_list = []
    for tag2 in tags2:
        find_a = tag2.find('a')
        url_list.append(find_a['href'])
    
    return_list = []
    for i in range(len(categories_list)):
        tup = (categories_list[i], book_titles[i], url_list[i])
        return_list.append(tup)
    
    return return_list


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename), "w") as f:
        header = ["Book Title", "Author Name"]
        w = csv.writer(f)
        w.writerow(header)
        for tup in data: 
            w.writerow(tup)


def extra_credit(filepath):
    with open(filepath) as f:
        soup = BeautifulSoup(f, "html.parser")
    tags = soup.find('body')
    tags2 = tags.find('div', class_ = "content")
    tags3 = tags2.find('div', class_ = "mainContentContainer")
    tags4 = tags3.find('div', class_ = 'mainContentFloat')
    tags5 = tags4.find('div', class_ = 'leftContainer')
    tags6 = tags5.find('div', class_ = 'last col stacked')
    tags7 = tags6.find('div', class_ = 'last col')
    tags8 = tags7.find('div', class_ = "readable stacked").text.strip()
    regex = "[A-Z][a-z]+. [A-Z][a-z]+"
    named_entities = []
    x = re.findall(regex, tags8)
    for word in x:
        named_entities.append(word)
    return named_entities

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()



    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        results = get_titles_from_search_results('search_results.htm')    

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(results), 20)

        # check that the variable you saved after calling the function is a list
        self.assertIsInstance(results, list)

        # check that each item in the list is a tuple
        for result in results:
            self.assertIsInstance(result, tuple)

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual((results[0][0]), 'Harry Potter and the Deathly Hallows (Harry Potter, #7)')
        self.assertEqual((results[0][1]), 'J.K. Rowling')

        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual((results[-1][0]), 'Harry Potter: The Prequel (Harry Potter, #0.5)')
        

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertIsInstance(TestCases.search_urls, list)

        # check that the length of TestCases.search_urls is correct (10 URLs)
        count = 0
        for url in TestCases.search_urls:
            count += 1
        self.assertEqual(count, 10)

        # check that each URL in the TestCases.search_urls is a string
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        starts_with_list = []
        for url in TestCases.search_urls:
            self.assertIsInstance(url, str)
            if url.startswith("https://www.goodreads.com/book/show"):
                starts_with_list.append(url)
        
        self.assertEqual(len(starts_with_list), 10)


    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for url in TestCases.search_urls:
            summaries.append(get_book_summary(url))

        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)

            # check that each item in the list is a tuple
        for item in summaries:
            self.assertIsInstance(item, tuple)

            # check that each tuple has 3 elements
            for item in summaries:
                self.assertEqual(len(item), 3)

            # check that the first two elements in the tuple are string
            for item in summaries:
                self.assertIsInstance(item[0], str)
                self.assertIsInstance(item[1], str)

            # check that the third element in the tuple, i.e. pages is an int
            for item in summaries:
                 self.assertIsInstance(item[2], int)

            # check that the first book in the search has 337 pages
            self.assertEqual(summaries[0][2], 337)


    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        summarized = summarize_best_books("best_books_2020.htm")

        # check that we have the right number of best books (20)
        self.assertEqual(len(summarized), 20)

            # assert each item in the list of best books is a tuple
        for item in summarized:
            self.assertIsInstance(item, tuple)

            # check that each tuple has a length of 3
        for item in summarized:
            self.assertEqual(len(item), 3)

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(summarized[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))

        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'A Beautiful Day in the Neighborhood: The Poetry of Mister Rogers', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(summarized[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        search_results = get_titles_from_search_results("search_results.htm")

        # call write csv on the variable you saved and 'test.csv'
        write_csv(search_results, 'test.csv')

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        f = open('test.csv')
        csv_lines = f.readlines()

        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)

        # check that the header row is correct
        self.assertEqual(csv_lines[0], 'Book Title,Author Name\n')

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1], ('"Harry Potter and the Deathly Hallows (Harry Potter, #7)",J.K. Rowling\n'))

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'Julian Harrison (Introduction)'
        self.assertEqual(csv_lines[-1], ('"Harry Potter: The Prequel (Harry Potter, #0.5)",Julian Harrison\n'))


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



