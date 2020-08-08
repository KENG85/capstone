DROP TABLE load_score;
CREATE TABLE load_score ( 	
	"timestamp" varchar(20) NOT NULL ,
	"org" varchar(30),
	"sport" varchar(30),
	"pos" varchar(30),
	"player" varchar(12),
	--"jump_score" numeric , 
	"sleep" integer,
	"nutrition" integer, 
	"fatigue" integer,
	"motivation" integer,
	"stress" integer,
	"RPE" integer,
	--"plus" integer,
	--"value" integer,
	"tweet" varchar(150)
);

select * from load_score; 