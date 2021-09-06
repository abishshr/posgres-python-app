
from sqlalchemy import create_engine
import pandas as pd
import time
# all the constants
db_name = 'database'
db_user = 'username'
db_pass = 'secret'
db_host = 'db'
db_port = '5432'
PRSN_TBL = "persons"
PRSN_TEAM_ASSOC_TBL = "person_team_association"
TEAMS_TBL = "teams"
MODELED_TBL = "persons_no_team"

DIR = "/code/data/"
EXTENSION = ".csv"
PRSN_FILE_LOC = DIR + PRSN_TBL + EXTENSION
PRSN_TEAM_ASSOC_FILE_LOC = DIR + PRSN_TEAM_ASSOC_TBL + EXTENSION
TEAMS_TBL_FILE_LOC = DIR + TEAMS_TBL + EXTENSION

db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
print(f"Connecting to: \n{db_string}")
db = create_engine(db_string)

create_table_persons_sql = "CREATE TABLE IF NOT EXISTS persons\
                            (\
                            pid VARCHAR NOT NULL PRIMARY KEY,\
                            person_created_ts TIMESTAMP ,\
                            last_login_ts TIMESTAMP,\
                            subscription_start_ts TIMESTAMP,\
                            subscription_end_ts TIMESTAMP\
                            )"
create_table_person_team_association_sql = "CREATE TABLE IF NOT EXISTS person_team_association\
                                            (\
                                            pid VARCHAR NOT NULL ,\
                                            qid VARCHAR NOT NULL \
                                            )"

create_table_teams_sql = "CREATE TABLE IF NOT EXISTS teams \
                            (\
                            tid VARCHAR NOT NULL PRIMARY KEY,\
                            age_group VARCHAR,\
                            competition_level VARCHAR ,\
                            n_games_scored INTEGER ,\
                            last_game_scored_ts TIMESTAMP\
                            )"

modeled_table_persons_sql = "CREATE TABLE IF NOT EXISTS persons_no_team \
                            as (select\
                            distinct(a.pid) as pid \
                            from public.persons a \
                            left join \
                            public.person_team_association b\
                            on a.pid = b.pid where b.tid is null )\
                            "
modeled_table_persons_count_sql = "SELECT COUNT(*) FROM persons_no_team"

def create_table(query, table_name):
    try:
        db.execute(query)
    except:
        print("Table " + table_name + " didnt load , some error has occurred!")
    else:
        print("Table  " + table_name + " Successfully created")


def load_table(table_name, file_location, engine):
    df = pd.read_csv(file_location)

    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
    except:
        print("Table " + table_name + " didnt load , some error has occurred!")
    else:
        print("Table " + table_name + " Successfully Loaded with count :  "+ str(len(df.index)))

def count_rows(querry) :
    try:
        count = str(db.execute(querry).scalar())
        return count
    except:
        print("Table not present")

if __name__ == '__main__':
    time.sleep(5)
    create_table(create_table_persons_sql, PRSN_TBL)
    create_table(create_table_person_team_association_sql, PRSN_TEAM_ASSOC_TBL)
    create_table(create_table_teams_sql, TEAMS_TBL)
    load_table(PRSN_TBL, PRSN_FILE_LOC, db)
    load_table(PRSN_TEAM_ASSOC_TBL, PRSN_TEAM_ASSOC_FILE_LOC, db)
    load_table(TEAMS_TBL, TEAMS_TBL_FILE_LOC, db)
    create_table(modeled_table_persons_sql ,MODELED_TBL)
    print ("Count of unique persons who dont follow any teams is : " + count_rows(modeled_table_persons_count_sql))
    db.dispose()