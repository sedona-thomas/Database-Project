
# Names and UNIs:
Jessica Kuleshov - jjk2235

Sedona Thomas - snt2127

# PostgreSQL account:
jjk2235


# Add-Ons:
    
    
Our first addition is that of a Composite "note_page" type. This type contains a page of notes that a User has written, as well as when it was written. That way, Users can keep notes about snippets of code, methods, constants, packages, etc. that they find interesting for future use. 

The second addition is a full-text search over the note_pages. This allows Users to see if they have written any notes about a particular subject - say they wish to see what notes they have about "hexdigits" - the full-text search looks in the body of each note_page and returns the title and body so the User can read what the note says.

The final addition is a trigger that, when user code is added into the user_code table, it automatically adds the user as an author and assigns them the next author-id in the author-id table, as well as adding them as a contributor, if they have not already contributed something.


# Create statements:

CREATE TYPE note_page AS (title VARCHAR(100), time_stamp date, keywords CHAR(500)[], body TEXT);

CREATE TABLE notes (note_id int, note note_page, PRIMARY KEY (note_id));

CREATE TABLE user_notes (user_id int, note_id int, PRIMARY KEY (user_id, note_id), FOREIGN KEY(user_id) REFERENCES users, FOREIGN KEY(not_id) REFERENCES notes);

CREATE FUNCTION contributor_trigger() RETURNS TRIGGER AS $BODY$ BEGIN INSERT INTO author(author_id, name) VALUES ((SELECT max(a.author_id)+1 FROM author AS a), (SELECT u.name FROM users AS u WHERE u.user_id = NEW.user_id)) ON CONFLICT DO NOTHING; INSERT INTO contributor(user_id, author_id) VALUES (NEW.user_id, (SELECT a.author_id FROM author AS a WHERE a.name = (SELECT u.name FROM users AS u WHERE u.user_id = NEW.user_id))) ON CONFLICT DO NOTHING; RETURN NEW; END; $BODY$ language plpgsql;

CREATE TRIGGER add_contributor AFTER INSERT ON user_code FOR EACH ROW EXECUTE PROCEDURE contributor_trigger();

INSERT INTO user_code VALUES ('johnBuffer/AntSimulator', 6);

    This is the event that causes the trigger to fire. When ('johnBuffer/AntSimulator',5) is added, it indicates the filepath 'johnBuffer/AntSimulator', where it checks that the filepath is in the code table, and indicates the user_id 5. It then looks to see if this user_id is already an author (i.e. has an author_id associated with it) else it adds the next highest author_id and the name associated with the user_id (from the users table) to the author table. It then checks to see if the author_id and user_id are already associated in the contributor table, and if not adds the author_id and user_id as a row there as well.

# Insert Data:

INSERT INTO user_notes VALUES (1, 2);
  
INSERT INTO notes VALUES (0, ROW('Note Title', '1-1-2021', '{keyword}', 'This is the note body.'));

INSERT INTO code VALUES ('johnBuffer/AntSimulator', 'AntSimulator', 'github.com/johnBuffer/AntSimulator');

INSERT INTO user_code VALUES ('johnBuffer/AntSimulator', 1);

# Queries:

SELECT (note).title || ': ' || (note).body FROM notes WHERE note_id = 1;

    This query returns an entire note with the title and body given the note_id.

SELECT note_id FROM notes WHERE 'numpy' = ANY((note).keywords);

    This query searches the array of keywords in all notes for 'numpy' and returns all the note_id for all notes that have the keyword numpy. This allows a user to search notes by keyword rather than just a full text search.

SELECT note_id FROM notes WHERE (to_tsvector((SELECT (note).title || ' ' || (note).body)) @@ to_tsquery('numpy | tuple'));

    This query searches the body and title of all notes for 'numpy' or 'tuple'. This allows users to search the full note for any number of strings and access the note_id for the notes containing the query.

SELECT note_id FROM (SELECT * FROM notes AS n NATURAL JOIN user_notes AS u WHERE u.user_id=4) AS your_notes WHERE (to_tsvector((SELECT (note).title || ' ' || (note).body)) @@ to_tsquery('numpy | tuple'));

    This query searches the body and title of all notes associated with a specific user for 'numpy' or 'tuple'. This allows users to search within their personal notes for any number of strings and access the note_id for the notes containing the query.
