from models.author import Author

class Magazine:
    def __init__(self, id=None, name=None, category=None, connection=None):
        # Ensure only one of id or name is provided
        if connection is None:
            raise ValueError("A database connection must be provided.")
        self.connection = connection
        
        if id is None and (name is None or category is None):
            raise ValueError("If id is not provided, both name and category must be provided.")
        
        if id is not None and name is not None:
            raise ValueError("You must provide either an id or a name, but not both.")

        if id is not None:
            # If ID is provided, fetch the magazine from the database
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, name, category FROM magazines WHERE id = ?", (id,))
            result = cursor.fetchone()
            if result is None:
                raise ValueError(f"No magazine found with id {id}.")
            self._id, self._name, self._category = result
        elif name is not None and category is not None:
            # If id is not provided, insert a new magazine into the database
            if not isinstance(name, str) or len(name) < 2 or len(name) > 16:
                raise ValueError("Name must be a string between 2 and 16 characters.")
            if not isinstance(category, str) or not category.strip():
                raise ValueError("Category must be a non-empty string.")
            
            self._name = name.strip()
            self._category = category.strip()

            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self._name, self._category))
            self.connection.commit()
            self._id = cursor.lastrowid
        else:
            raise ValueError("Either id or name and category must be provided.")

    def __repr__(self):
        return f"<Magazine {self.name} - {self.category}>"

    


    # Getter for id
    @property
    def id(self) -> int:
        return self._id

    # Setter for id
    @id.setter
    def id(self, value: int):
        if not isinstance(value, int):
            raise TypeError("ID must be of type int.")
        self._id = value

    # Getter for name
    @property
    def name(self) -> str:
        return self._name

    # Setter for name
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Name must be of type str.")
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be between 2 and 16 characters, inclusive.")
        self._name = value.strip()

    # Getter for category
    @property
    def category(self) -> str:
        return self._category

    # Setter for category
    @category.setter
    def category(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Category must be of type str.")
        if len(value.strip()) == 0:
            raise ValueError("Category must not be empty.")
        self._category = value.strip()

    
    def articles(self):
        if self.connection is None:
            raise ValueError("Database connection is not set.")

        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT articles.*
                FROM articles
                WHERE articles.magazine_id = ?
            """, (self.id,))
            articles = cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Error fetching articles: {e}")
        finally:
            cursor.close()

        return articles or []

   
    def contributors(self):
        if self.connection is None:
            raise ValueError("Database connection is not set.")

        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT authors.*
                FROM authors
                JOIN authors_articles ON authors_articles.author_id = authors.id
                JOIN articles ON articles.id = authors_articles.article_id
                WHERE articles.magazine_id = ?
            """, (self.id,))
            contributors = cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Error fetching contributors: {e}")
        finally:
            cursor.close()

        return contributors or []

    # Method to get titles of all articles for the magazine
    def article_titles(self):
        if self.connection is None:
            raise ValueError("Database connection is not set.")

        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT articles.title
                FROM articles
                WHERE articles.magazine_id = ?
            """, (self.id,))
            articles = cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Error fetching article titles: {e}")
        finally:
            cursor.close()

        # Return titles or an empty list
        return [article[0] for article in articles] if articles else []

    # Method to get authors who have written more than 2 articles for the magazine
    def contributing_authors(self):
        if self.connection is None:
            raise ValueError("Database connection is not set.")

        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT authors.id, authors.name
                FROM authors
                JOIN authors_articles ON authors_articles.author_id = authors.id
                JOIN articles ON articles.id = authors_articles.article_id
                WHERE articles.magazine_id = ?
                GROUP BY authors.id, authors.name
                HAVING COUNT(articles.id) > 2
            """, (self.id,))
            authors = cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Error fetching contributing authors: {e}")
        finally:
            cursor.close()

        # Convert to Author objects or return an empty list
        return [Author(id=author[0], name=author[1], connection=self.connection) for author in authors] if authors else []
