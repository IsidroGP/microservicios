CREATE TABLE "original_content" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL,
	"type"	TEXT NOT NULL,
	"genre"	TEXT NOT NULL,
	"imdb_rating"	REAL
);