import unittest
import random
import string
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from database.connection import get_db_connection

class TestModels(unittest.TestCase):
    def setUp(self):
        """Set up the database connection before each test."""
        self.connection = get_db_connection()  # Use a valid database connection
        # Optionally, create tables if they don't exist
        self.create_tables()

    def tearDown(self):
        """Clean up after each test."""
        self.connection.close()

    def create_tables(self):
        """Create tables for testing."""
        cursor = self.connection.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author_id INTEGER,
                magazine_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES authors (id),
                FOREIGN KEY (magazine_id) REFERENCES magazines (id)
            )
        ''')

        self.connection.commit()

    def generate_random_string(self, length=10):
        """Generate a random string of a given length."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def test_author_creation(self):
        """Test author creation with a valid name."""
        author_name = self.generate_random_string(10)  # Generate a random name
        author = Author(name=author_name, connection=self.connection)
        
        self.assertEqual(author.name, author_name)
        self.assertIsInstance(author.id, int)  # Check that an ID was assigned

    def test_article_creation(self):
        """Test article creation with valid inputs."""
        author_name = self.generate_random_string(10)
        magazine_name = self.generate_random_string(10)
        magazine_category = self.generate_random_string(5)
        article_title = self.generate_random_string(15)
        article_content = self.generate_random_string(30)
        
        # Create author and magazine (do not pass 'id')
        author = Author(name=author_name, connection=self.connection)
        magazine = Magazine(name=magazine_name, category=magazine_category, connection=self.connection)

        # Create article with dynamic inputs and allow the 'id' to be auto-generated
        article = Article(title=article_title, content=article_content, author_id=author.id, magazine_id=magazine.id, connection=self.connection)
        
        self.assertEqual(article.title, article_title)
        self.assertEqual(article.content, article_content)
        self.assertEqual(article.author_id, author.id)
        self.assertEqual(article.magazine_id, magazine.id)

    def test_magazine_creation(self):
        """Test magazine creation with valid inputs."""
        magazine_name = self.generate_random_string(10)
        magazine_category = self.generate_random_string(5)
        
        # Create magazine (do not pass 'id')
        magazine = Magazine(name=magazine_name, category=magazine_category, connection=self.connection)
        
        self.assertEqual(magazine.name, magazine_name)
        self.assertEqual(magazine.category, magazine_category)

if __name__ == "__main__":
    unittest.main()
