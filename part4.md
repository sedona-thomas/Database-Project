
# Names and UNIs:
Jessica Kuleshov - jjk2235
Sedona Thomas - snt2127

# PostgreSQL account:
jjk2235


# Add-Ons:
    
    
Our first addition is that of a Composite "note_page" type. This type contains a page of notes that a User has written, as well as when it was written. That way, Users can keep notes about snippets of code, methods, constants, packages, etc. that they find interesting for future use. 

The second addition is a full-text search over the note_pages. This allows Users to see if they have written any notes about a particular subject - say they wish to see what notes they have about "hexdigits" - the full-text search looks in the body of each note_page and returns the title and body so the User can read what the note says.

The final addition is a trigger that, when user code is added into the user_code table, it automatically adds the user as an author and assigns them the next author-id in the author-id table, as well as adding them as a contributor, if they have not already contributed something.



Composite Type: note_page type
  
    CREATE TYPE note_page AS (title VARCHAR(100), timestamp date NOT NULL DEFAULT CURRENT_DATE, body TEXT);
    

    
Text attribute: notes page using note_page data type
  
    make search query for text attribute

Trigger:

    *find new one (deleteing userid from things happens automatically since it is a primary key)
  
    upon insert into user_code add user to author and contributor if it doesnt exist
    
    any time something is connected to a keyword, it is added to the keywords table
    
      any time a keyword is connected to another keyword, the trigger makes pairs with all keywords connected to both of them
    
    share notes with another user
  




# Create statements:

CREATE TYPE note_page AS (title VARCHAR(100), time_stamp date, keywords CHAR(500)[], body TEXT);

CREATE TABLE notes (note_id int, note note_page, PRIMARY KEY (note_id));

CREATE TABLE user_notes (user_id int, note_id int, PRIMARY KEY (user_id, note_id), FOREIGN KEY(user_id) REFERENCES users, FOREIGN KEY(not_id) REFERENCES notes);



# Queries:

INSERT INTO user_notes VALUES (1, 2);
  
INSERT INTO notes VALUES (0, ROW('Note Title', 'This is the note body.'));

SELECT n.title || ' ' || n.body AS document FROM notes AS n WHERE note_id = 0;
  
SELECT n.title || ' ' || n.body AS document FROM notes AS n WHERE note_id = 0 AND SELECT document @@ to_tsquery('str || char');
  
SELECT n.title FROM notes AS n WHERE note_id = 0 AND 'str' = ANY(n.keywords);

CREATE FUNCTION contributor_trigger() RETURNS TRIGGER AS $BODY$ BEGIN INSERT INTO contributor(user_id, author_id) VALUES (NEW.user_id, (SELECT max(a.author_id)+1 FROM author AS a)) ON CONFLICT DO NOTHING; INSERT INTO author(author_id, name) VALUES ((SELECT a.author_id FROM contributor AS c WHERE c.user_id = NEW.user_id), (SELECT u.name FROM contributor AS c, users AS u WHERE c.user_id = NEW.user_id AND u.user_id = NEW.user_id)) ON CONFLICT DO NOTHING; RETURN NEW; END; $BODY$ language plpgsql;

CREATE TRIGGER add_contributor AFTER INSERT ON user_code FOR EACH ROW EXECUTE PROCEDURE contributor_trigger();


INSERT INTO code VALUES ('johnBuffer/AntSimulator', 'AntSimulator', 'github.com/johnBuffer/AntSimulator');
INSERT INTO user_code VALUES ('johnBuffer/AntSimulator', 1);



