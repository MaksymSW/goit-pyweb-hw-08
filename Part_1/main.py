import json
from models import Author,Quote
from termcolor import colored

def load_authors(authors_file):
    with open(authors_file, 'r', encoding='utf-8') as file:
        authors = json.load(file)
        for author in authors:
            new_author = Author(name=author['fullname'])
            new_author.save()


def load_quotes(quotes_file):
    with open(quotes_file, 'r', encoding='utf-8') as file:
        quotes = json.load(file)
        for quote in quotes:
            author_name = quote['author']
            author = Author.objects(name=author_name).first()
            if author:
                new_quote = Quote(content=quote['quote'], author=author, tags=quote['tags'])
                new_quote.save()


load_authors('authors.json')
load_quotes('quotes.json')

def find_quotes_by_author(author_name):
    author = Author.objects(name=author_name).first()
    if author:
        quotes = Quote.objects(author=author)
        return [quote.content for quote in quotes]
    return []

def find_quotes_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    return [quote.content for quote in quotes]

def find_quotes_by_tags(tags):
    tags_list = tags.split(',')
    quotes = Quote.objects(tags__in=tags_list)
    return [quote.content for quote in quotes]

def main():
    while True:
        command = input("""\nEnter a command, for example:\n\tname: Steve Martin\n\ttag:life\n\ttags:life,live\n\texit\nplease:\t""")
        if command.startswith("name:"):
            author_name = command.split("name:")[1].strip()
            quotes = find_quotes_by_author(author_name)
            print('\n'.join(quotes))
        elif command.startswith("tag:"):
            tag = command.split("tag:")[1].strip()
            quotes = find_quotes_by_tag(tag)
            print('\n'.join(quotes))
        elif command.startswith("tags:"):
            tags = command.split("tags:")[1].strip()
            quotes = find_quotes_by_tags(tags)
            print('\n'.join(quotes))
        elif command == "exit":
            break
        else:
            print(colored("! ", 'red', 'on_black', ['bold', 'blink']) + colored("The command is bad", "red") + colored(" !", 'red', 'on_black', ['bold', 'blink']))

if __name__ == "__main__":
    main()