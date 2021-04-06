
1. Names and UNIs:
  Jessica Kuleshov - jjk2235
  Sedona Thomas - snt2127

2. PostgreSQL account:
  jjk2235

3. Add-Ons:    

  Our first addition is that of a Composite "note_page" type. This type contains a title, a timestamp,
  an array of keywords, and a text attribute containing the note. That way, Users can keep notes about 
  snippets of code, methods, constants, packages, etc. that they find interesting for future use.
  This fits in with our general database schema because our database has a large focus on 
  personalized data per User, and having notes on various methods also allows for more customization
  on a User's part, along with already-existing features such as Favorites.

  The second addition is a full-text search over the note_pages. This allows Users to see if they 
  have written any notes about a particular subject - say they wish to see what notes they have 
  about "hexdigits" - the full-text search looks in the body of each note_page and returns the 
  title and body so the User can read what the note says. This is important because Users sometimes
  do not remember exactly what they titled their notes, so it can often be more useful to search
  the body and title for phrases they expect to find. 

  The final addition is a trigger that, when user code is added into the user_code table, it 
  automatically adds the user as an author and assigns them the next author-id in the author-id 
  table, as well as adding them as a contributor, if they have not already contributed something.
  This fits with our general design because it helps ensure that author_id's are properly assigned
  to users in a correct order without having to make a function for it, and properly updates the
  contributor table as well without manually doing so as well.


4. Trigger:

  INSERT INTO user_code VALUES ('johnBuffer/AntSimulator', 6);

    This is the event that causes the trigger to fire. When ('johnBuffer/AntSimulator',5) is added, 
    it indicates the filepath 'johnBuffer/AntSimulator', where it checks that the filepath is in the 
    code table, and indicates the user_id 5. It then looks to see if this user_id is already an author 
    (i.e. has an author_id associated with it - in this case there isn't) else it adds the next highest 
    author_id and the name associated with the user_id (from the users table) to the author table. It 
    then checks to see if the author_id and user_id are already associated in the contributor table.
    In this case it is not associated, so the trigger adds the author_id and user_id as a row there as well.

5. Queries:

  SELECT (note).title || ': ' || (note).body FROM notes WHERE note_id = 1;

    This query returns an entire note with the title and body given the note_id.

  SELECT note_id FROM notes WHERE 'numpy' = ANY((note).keywords);

    This query searches the array of keywords in all notes for 'numpy' and returns all the note_id for 
    all notes that have the keyword numpy. This allows a user to search notes by keyword rather than just 
    a full text search.

  SELECT note_id FROM notes WHERE (to_tsvector((SELECT (note).title || ' ' || (note).body)) @@ to_tsquery('numpy | tuple'));

    This query searches the body and title of all notes for 'numpy' or 'tuple'. This allows users to search 
    the full note for any number of strings and access the note_id for the notes containing the query.

  SELECT note_id FROM (SELECT * FROM notes AS n NATURAL JOIN user_notes AS u WHERE u.user_id=4) AS your_notes 
  WHERE (to_tsvector((SELECT (note).title || ' ' || (note).body)) @@ to_tsquery('numpy | tuple'));

    This query searches the body and title of all notes associated with a specific user for 'numpy' or 
    'tuple'. This allows users to search within their personal notes for any number of strings and access 
    the note_id for the notes containing the query.
