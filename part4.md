

# Add-Ons:

Text attribute: notes page using note_page data type
  
    make search query for text attribute

Composite Type: note_page type
  
    CREATE TYPE note_page AS (title VARCHAR(100), timestamp DATE NOT NULL DEFAULT CURRENT_DATE, body TEXT);

Trigger:

    *find new one (deleteing userid from things happens automatically since it is a primary key)
  
    upon insert into user_code add user to author and contributor if it doesnt exist
  
Array:

    keyword array in note page
  




# Create statements:

CREATE TYPE note_page AS (title VARCHAR(100), timestamp DATE NOT NULL DEFAULT CURRENT_DATE, keywords CHAR(500)[], body TEXT);

CREATE TABLE user_notes (user_id int, note_id int PRIMARY KEY (user_id, note_id), FOREIGN KEY(user_id) REFERENCES users, FOREIGN KEY(not_id) REFERENCES notes);

CREATE TABLE notes (note_id int, note note_page, PRIMARY KEY (note_id));




# Queries:

  share notes with another user
  
  add note page
  
  search note page

  SELECT n.title || ' ' || n.body AS document FROM notes AS n WHERE note_id = 0;
  
  SELECT n.title || ' ' || n.body AS document FROM notes AS n WHERE note_id = 0 AND SELECT document @@ to_tsquery('str || char');
  
  SELECT n.title FROM notes AS n WHERE note_id = 0 AND 'str' = ANY(n.keywords);


