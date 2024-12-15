class Author:
    def __init__(self, id: int = None, name: str = None, connection=None):
        # Ensure that a valid database connection is provided
        if connection is None:
            raise ValueError("A database connection must be provided.")
        
        self.connection = connection

        if id is not None and name is None:
            # Fetch author by id
            cursor = self.connection.cursor()
            try:
                cursor.execute("SELECT id, name FROM authors WHERE id = ?", (id,))
                result = cursor.fetchone()
                if result is None:
                    raise ValueError(f"No author found with the given id: {id}.")
                self._id, self._name = result
            finally:
                cursor.close()
        elif name is not None and id is None:
            # Validate name and insert new author
            if not isinstance(name, str):
                raise TypeError("Name must be of type str.")
            if len(name.strip()) == 0:
                raise ValueError("Name must not be empty.")

            cursor = self.connection.cursor()
            try:
                cursor.execute("INSERT INTO authors (name) VALUES (?)", (name.strip(),))
                self.connection.commit()
                self._id = cursor.lastrowid
                self._name = name.strip()
            finally:
                cursor.close()
        else:
            raise ValueError("You must provide either an id or a name, but not both.")

    def __repr__(self):
        return f"<Author {self.name}>"

    # Getter for id
    @property
    def id(self) -> int:
        return self._id

    # Setter for id - The 'id' property cannot be changed once set
    @id.setter
    def id(self, value: int):
        raise AttributeError("The 'id' property cannot be changed once set.")

    # Getter for name
    @property
    def name(self) -> str:
        return self._name

    # Prevent changing the name after initialization
    @name.setter
    def name(self, value: str):
        raise AttributeError("The 'name' property cannot be changed after initialization.")

    
    def articles(self):
        if self.connection is None:
            raise ValueError("Database connection is not set.")
        
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                SELECT articles.id, articles.title, articles.content, articles.magazine_id
                FROM articles
                JOIN authors_articles ON authors_articles.article_id = articles.id
                WHERE authors_articles.author_id = ?
            """, (self.id,))
            articles = cursor.fetchall()
        finally:
            cursor.close()
        
        return articles if articles else []

    
    def magazines(self):
        if self.connection is None:
            raise ValueError("Database connection is not set.")
        
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                SELECT DISTINCT magazines.id, magazines.name, magazines.category
                FROM magazines
                JOIN articles ON articles.magazine_id = magazines.id
                JOIN authors_articles ON authors_articles.article_id = articles.id
                WHERE authors_articles.author_id = ?
            """, (self.id,))
            magazines = cursor.fetchall()
        finally:
            cursor.close()
        
        return magazines if magazines else []
