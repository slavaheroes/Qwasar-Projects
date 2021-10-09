1. Run the my_sqlite_req_check.py file to check functions of my_sqlite_request.py
    my_sqlite_req_check.py contains some basic test cases, feel free to modify it for different scenarios.


2. Run the my_sqlite_cli.py by python my_sqlite_cli.py

These commands can be used as test cases for testing my_sqlite_cli.py: (please follow the order)
    SELECT * FROM 'nba_player_data.csv' WHERE name = 'John Abramovic';
    INSERT INTO 'nba_player_data.csv' VALUES (Cristiano Ronaldo, 2003, 2020, F, 6-3, 195.0, Feb 4 2020, Manchester University) ;
    SELECT * FROM 'nba_player_data.csv' WHERE name = 'Cristiano Ronaldo';
    UPDATE 'nba_player_data.csv' SET year_end = 2021, college = 'Columbia University' WHERE name = Cristiano Ronaldo';
    SELECT * FROM 'nba_player_data.csv' WHERE name = 'Cristiano Ronaldo';
    DELETE FROM 'nba_player_data.csv' WHERE name = 'Cristiano Ronaldo';
    SELECT * FROM 'nba_player_data.csv' WHERE name = 'Cristiano Ronaldo';
    quit