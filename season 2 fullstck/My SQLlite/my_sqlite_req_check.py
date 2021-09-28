'''
    I provided some test commands for MySqliteRequest
    Uncomment the commands you need before you run the program
'''

from my_sqlite_request import MySqliteRequest
# 1. Select and where commands
req = MySqliteRequest()

req = req.from_table('nba_player_data.csv').select('name')
print(req.run())

req = req.new()
req = req.from_table('nba_player_data.csv').select('name').where('college', 'University of California')
print(req.run())

req = req.new()
req = req.from_table('nba_player_data.csv').select('name').where('college', 'University of California').\
    where('year_start', '1997')
print(req.run())

# 2. Insert
# req = req.new()
# req = req.insert('nba_player_data.csv').values('Alaa Abdelnaby','1991','1995', 'F-C', 
#  '6-10', '240', "June 24, 1968", 'Duke University').run()

# req = req.new()
# req = req.from_table('nba_player_data.csv').select('*').where('name', 'Alaa Abdelnaby')
# print(req.run())

# 3. Update 

# req = req.new()
# req = req.update('nba_player_data.csv').update_set('name', 'Alaa Renamed').where('name', 'Alaa Abdelnaby')\
#     .run()

# req = req.new()
# req = req.from_table('nba_player_data.csv').select('*').where('name', 'Alaa Renamed')
# print(req.run())

# 4. Delete
# req = req.new()
# req = req.delete().from_table('nba_player_data.csv').where('name', 'Alaa Renamed').run()

# req = req.new()
# req = req.from_table('nba_player_data.csv').select('*').where('name', 'Alaa Renamed')
# print(req.run())

# 5. Join

# req = req.new()
# req = req.from_table('nba_player_data.csv').select("name", "college", "birth_state").join('name', 'nba_players.csv', 'Player').\
#     where('college', 'Indiana University')
# print(req.run())

# 6. Order

# req = req.new()
# req = req.from_table('nba_player_data.csv').select('*').where('college', 'University of California').\
#     order('year_start')
# print(req.run())

# req = req.new()
# req = req.from_table('nba_player_data.csv').select('*').where('college', 'University of California').\
#     order('year_start', desc = True)
# print(req.run())




