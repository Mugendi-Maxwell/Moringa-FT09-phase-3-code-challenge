class Article:
    def __init__(self, id: int = None, title: str = None, content: str = None, author_id: int = None, magazine_id: int = None, connection=None):
       
        if connection is None:
            raise ValueError("A database connection must be provided.")
        
        self.connection = connection

        if id is not None:
            # Fetch article by id
            cursor = self.connection.cursor()
            try:
                cursor.execute("SELECT id, title, content, author_id, magazine_id FROM articles WHERE id = ?", (id,))
                result = cursor.fetchone()
                if result is None:
                    raise ValueError(f"No article found with the given id: {id}.")
                self._id, self._title, self._content, self._author_id, self._magazine_id = result
            finally:
                cursor.close()
        elif title is not None and content is not None and author_id is not None and magazine_id is not None:
            # Insert new article
            cursor = self.connection.cursor()
            try:
                cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)", 
                               (title.strip(), content.strip(), author_id, magazine_id))
                self.connection.commit()
                self._id = cursor.lastrowid
                self._title = title.strip()
                self._content = content.strip()
                self._author_id = author_id
                self._magazine_id = magazine_id
            finally:
                cursor.close()
        else:
            raise ValueError("You must provide either an id to fetch an article or title, content, author_id, and magazine_id to create a new article.")

    def __repr__(self):
        return f"<Article {self.title}>"

    # Getter for id
    @property
    def id(self) -> int:
        return self._id

    # Setter for id - The 'id' property cannot be changed once set
    @id.setter
    def id(self, value: int):
        raise AttributeError("The 'id' property cannot be changed once set.")

    # Getter for title
    @property
    def title(self) -> str:
        return self._title

    # Setter for title - The 'title' property cannot be changed after initialization
    @title.setter
    def title(self, value: str):
        raise AttributeError("The 'title' property cannot be changed after initialization.")

    # Getter for content
    @property
    def content(self) -> str:
        return self._content

    # Setter for content - The 'content' property cannot be changed after initialization
    @content.setter
    def content(self, value: str):
        raise AttributeError("The 'content' property cannot be changed after initialization.")

    # Getter for author_id
    @property
    def author_id(self) -> int:
        return self._author_id

    # Setter for author_id - The 'author_id' property cannot be changed after initialization
    @author_id.setter
    def author_id(self, value: int):
        raise AttributeError("The 'author_id' property cannot be changed after initialization.")

    # Getter for magazine_id
    @property
    def magazine_id(self) -> int:
        return self._magazine_id

    # Setter for magazine_id - The 'magazine_id' property cannot be changed after initialization
    @magazine_id.setter
    def magazine_id(self, value: int):
        raise AttributeError("The 'magazine_id' property cannot be changed after initialization.")

    # Method to fetch associated author
    def author(self):
        if self.connection is None:
            raise ValueError("Database connection is not set.")
        
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, name FROM authors WHERE id = ?", (self.author_id,))
            author = cursor.fetchone()
        finally:
            cursor.close()
        
        return author if author else None

    # Method to fetch associated magazine
    def magazine(self):
        if self.connection is None:
            raise ValueError("Database connection is not set.")
        
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, name, category FROM magazines WHERE id = ?", (self.magazine_id,))
            magazine = cursor.fetchone()
        finally:
            cursor.close()
        
        return magazine if magazine else None
