# Project 1 Part 3

PostgreSQL account: jk2235
Database Name: project1

URL: 34.74.183.38:8111

Description: 

We implemented a database with ​Packages​, ​Modules​, ​Methods​, ​Constants​, ​Users​, ​Authors​, ​User Code​, ​Source Code​,Keywords​ and ​History​

The database will seek to solve the problem of searching up methods (and theirdocumentation) for programming languages, specifically focusing on implementing agood way of searching up Python packages, modules, and methods while also leavingroom for implementation of other programming languages. The entities involved wouldbe . The ​Package​ entity contains a package name and filepath, andare the folders for ​Modules​. ​Modules​ have a module name, list of ​Constants​, and list ofMethods​, and a list of ​Dependencies​. ​Constants​ have a constant name, ​Module itbelongs to​, constant type, a list of ​Keywords​, and a constant description and arecontained within ​Modules​. ​Methods​ have a method name, ​Module​ it belongs to,parameters, a return value, return value type, a list of keywords, a method description,and a list of similar methods and are also contained within ​Modules​. ​Modules​ alsocontain the ​Source Code​ and/or ​User Code​, which have text and a file size. The ​UserCode​ (ID’ed by ​Filepath​) contains the text and file size in bytes and must be written by aUser​ who contributes as an ​Author​. ​Source Code​ and​ User Code​ must be written by anAuthor​ with an ID, an author name, and the list of files worked on. The ​Users​ have aunique ID, a ​Username​, list of ​Favorite Packages​, list of ​Favorite Modules​, list ofFavorite Methods​, and a ​History​ associated with them. ​Keywords​ have a list of relatedKeywords​, and ​History​ has the date searched, time searched, and ​Filepath​ of the thingsearched. We will be pursuing the Web Front-End Option.

The ​Package​ entity contains a package name and filepath, andare the folders for ​Modules​. ​Modules​ have a module name, list of ​Constants​, and list ofMethods​, and a list of ​Dependencies​. ​Constants​ have a constant name, ​Module itbelongs to​, constant type, a list of ​Keywords​, and a constant description and arecontained within ​Modules​. ​Methods​ have a method name, ​Module​ it belongs to,parameters, a return value, return value type, a list of keywords, a method description,and a list of similar methods and are also contained within ​Modules​. ​Modules​ alsocontain the ​Source Code​ and/or ​User Code​, which have text and a file size. The ​UserCode​ (ID’ed by ​Filepath​) contains the text and file size in bytes and must be written by aUser​ who contributes as an ​Author​. ​Source Code​ and​ User Code​ must be written by anAuthor​ with an ID, an author name, and the list of files worked on. The ​Users​ have aunique ID, a ​Username​, list of ​Favorite Packages​, list of ​Favorite Modules​, list ofFavorite Methods​, and a ​History​ associated with them. ​Keywords​ have a list of relatedKeywords​, and ​History​ has the date searched, time searched, and ​Filepath​ of the thingsearched. We will be pursuing the Web Front-End Option.


of the parts of your original proposal in Part 1 that you implemented, the parts you did not (which hopefully is nothing or something very small), and possibly new features that were not included in the proposal and that you implemented anyway. If you did not implement some part of the proposal in Part 1, explain why.


Two of the web pages that require the most interesting database operations:


in terms of what the pages are used for, how the page is related to the database operations (e.g., inputs on the page are used in such and such way to produce database operations that do such and such), and why you think they are interesting.
