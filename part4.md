

# Add-Ons:

Text attribute: notes page using note_page data type
  
    make search query for text attribute

Composite Type: note_page type
  
    CREATE TYPE note_page AS (title VARCHAR(100), timestamp DATE NOT NULL DEFAULT CURRENT_DATE, body TEXT);

Trigger:

    *find new one (deleteing userid from things happens automatically since it is a primary key)
  
    upon insert into user_code add user to author and contributor if it doesnt exist
    
    any time something is connected to a keyword, it is added to the keywords table
    
      any time a keyword is connected to another keyword, the trigger makes pairs with all keywords connected to both of them
    
    share notes with another user
  
Array:

    keyword array in note page
  




# Create statements:

CREATE TYPE note_page AS (title VARCHAR(100), timestamp DATE NOT NULL DEFAULT CURRENT_DATE, keywords CHAR(500)[], body TEXT);

CREATE TABLE user_notes (user_id int, note_id int PRIMARY KEY (user_id, note_id), FOREIGN KEY(user_id) REFERENCES users, FOREIGN KEY(not_id) REFERENCES notes);

CREATE TABLE notes (note_id int, note note_page, PRIMARY KEY (note_id));




# Queries:

INSERT INTO user_notes VALUES (1, 2);
  
INSERT INTO notes VALUES (0, ROW('Note Title', 'This is the note body.'));

SELECT n.title || ' ' || n.body AS document FROM notes AS n WHERE note_id = 0;
  
SELECT n.title || ' ' || n.body AS document FROM notes AS n WHERE note_id = 0 AND SELECT document @@ to_tsquery('str || char');
  
SELECT n.title FROM notes AS n WHERE note_id = 0 AND 'str' = ANY(n.keywords);

CREATE FUNCTION contributor_trigger() RETURNS TRIGGER AS $BODY$ BEGIN INSERT INTO contibutor(user_id, author_id) VALUES (user_id, SELECT max(a.author_id)+1 FROM author AS a); INSERT INTO author(author_id, name) VALUES (SELECT a.author_id FROM author AS a WHERE a.user_id = NEW.user_id, SELECT u.name FROM contributor AS c, users AS u WHERE c.user_id = NEW.user_id AND u.user_id = NEW.user_id); RETURN NEW; END; $BODY$ language plpgsql;

CREATE TRIGGER add_contributor AFTER INSERT ON user_code FOR EACH ROW EXECUTE PROCEDURE contributor_trigger()
