import sqlite3
import argparse

parser = argparse.ArgumentParser(
    description="Outputs the word, the word stem, and the context from a Kindle vocabulary builder database"
)
parser.add_argument("databasefile", type=str, help="The filename of the database file")
parser.add_argument("book_name", type=str, help="The (partial) name of the book")
args = parser.parse_args()


def get_data(book_name):
    con = sqlite3.connect(args.databasefile)
    cur = con.cursor()
    sql = """
    SELECT
        word,
        stem,
        USAGE
    FROM
        WORDS
        INNER JOIN lookups ON words.id = lookups.word_key
        INNER JOIN book_info ON book_info.id = lookups.book_key
    WHERE
        --words.lang = ?
        title LIKE '%' || ? || '%';"""
    return cur.execute(sql, (book_name,))


def print_data(data):
    for row in data:
        print(row[0], row[1])
        print(row[2] + "\n")


if __name__ == "__main__":
    print_data(get_data(args.book_name))
