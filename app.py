from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()

    # Create a cursor and interact with the database
    cursor = conn.cursor()

    '''
        The following is just for testing purposes, 
        you can modify it to meet the requirements of your implementation.
    '''

    # Create an author
    cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
    author_id = cursor.lastrowid # Use this to fetch the id of the newly created author

    # Create a magazine
    cursor.execute('INSERT INTO magazines (name, category) VALUES (?,?)', (magazine_name, magazine_category))
    magazine_id = cursor.lastrowid # Use this to fetch the id of the newly created magazine

    # Create an article
    cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                   (article_title, article_content, author_id, magazine_id))

    conn.commit()

    # Query the database for inserted records. 
    # The following fetch functionality should probably be in their respective models

    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()

    # Do not close the connection yet
    # conn.close()   # <-- Remove this line

    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        # Pass the connection `conn` to the Magazine class
        print(Magazine(id=magazine[0], name=magazine[1], category=magazine[2], connection=conn))

    print("\nAuthors:")
    for author in authors:
        print(Author(id=author[0], name=author[1], connection=conn))

    print("\nArticles:")
    for article in articles:
        print(Article(id=article[0], title=article[1], content=article[2], author_id=article[3], magazine_id=article[4]))

    # Close the connection after all the operations
    conn.close()

if __name__ == "__main__":
    main()
