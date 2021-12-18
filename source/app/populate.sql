
drop table if exists Movies;

create table Movies (
    name    text,
    price   int,
    primary key (name)
);

-- Test data
INSERT INTO Movies VALUES
    ("The Shining", 4.80),
    ("E.T. the Extra-Terrestrial", 5.97),
    ("Back to the Future", 3.45),
    ("Beetlejuice", 5.25),
    ("Stand by Me", 4.20),
    ("The Breakfast Club", 5.50),
    ("Top Gun", 5.60),
    ("The Princess Bride", 1.50),
    ("Ferris Bueller's Day Off", 4.10),
    ("Ghostbusters", 6.75),
    ("Dune", 4.60),
    ("The Goonies", 5.70),
    ("Airplane!", 3.80),
    ("Spaceballs", 7.30),
    ("INSEC{w1sh_w3_b@ck_on_t1me}", 1337)
