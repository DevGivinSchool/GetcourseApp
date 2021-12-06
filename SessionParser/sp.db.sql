BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "last_date" (
	"value"	TEXT
);
CREATE TABLE IF NOT EXISTS "sessions" (
	"name"	,
	"value"	
);
INSERT INTO "last_date" VALUES ('18.05.2019');
COMMIT;
