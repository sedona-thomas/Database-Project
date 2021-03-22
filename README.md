# Project 1 Part 3

PostgreSQL account: jk2235
Database Name: project1

URL: 34.74.183.38:8111

Description: 

Our homepage allows users to log in and the server saves the current user. Users can also add themselves to the database so they can save their favorite modules, methods, and constants and they can add their personal code. Users can also search for the github link to packages and modules. Users can also search for modules, packages, constants, and methods with either a specific keyword or for modules, packages, constants, and methods with keywords directly related to the given keyword. Users can also search within their favorites by keyword. Users can also add favorite modules, methods, and constants and can add their personal code.

There are tabs that display all packages, modules, methods, and constants in the database. The packages and modules pages allow users to search for the modules contained in a given package and allow users to search for the methods and constants in a given module. Users also have an "About You" page where they can view all of their favorites and personal code.

We had intended to store the source code for all author and user code, but we modified it to store the github link instead so the user can see updated source code. We also decided to remove the history feature since it added an extra operation every time something is searched and you can already see your search history when you click on the text box which automatically displays previous searches from the browser. Important searches are also able to be stored in favorites and this is more selective since the user chooses and avoids saving searches that include spelling mistakes and unimportant searches.

 jjk2235 | author                      | table | jjk2235
 jjk2235 | code                        | table | jjk2235
 jjk2235 | contributor                 | table | jjk2235
 jjk2235 | module_constant_containment | table | jjk2235
 jjk2235 | module_dependencies         | table | jjk2235
 jjk2235 | module_method_containment   | table | jjk2235
 jjk2235 | package_module_containment  | table | jjk2235


of the parts of your original proposal in Part 1 that you implemented, the parts you did not (which hopefully is nothing or something very small), and possibly new features that were not included in the proposal and that you implemented anyway. If you did not implement some part of the proposal in Part 1, explain why.


Two of the web pages that require the most interesting database operations:


in terms of what the pages are used for, how the page is related to the database operations (e.g., inputs on the page are used in such and such way to produce database operations that do such and such), and why you think they are interesting.
