# Import SQL-Alchemy and Pandas
from sqlalchemy import create_engine
import pandas as pd

# Import file and Test
engine = create_engine("sqlite:///Chinook.sqlite")
table_names = engine.table_names()
print(table_names)

# Connect and undergo SQL query
con = engine.connect()
rs = con.execute("SELECT * FROM Album")
df = pd.DataFrame(rs.fetchall())
df.columns = rs.keys()
print(df.head())
con.close()

# Alternative (Simpler + Easier To Remember)
with engine.connect() as con:
    rs = con.execute("SELECT * FROM Album")
    df = pd.DataFrame(rs.fetchmany(size = 5))
    df.columns = rs.keys()
    print(df.head())
    con.close()

with engine.connect() as con:
    rs = con.execute("SELECT LastName, Title FROM Employee")
    df = pd.DataFrame(rs.fetchmany(size = 3))
    df.columns = rs.keys()
print(df.head())

# Even Simpler Method
df = pd.read_sql("SELECT * FROM Album", engine)
print(df.head())


# Defined SQLITE Query Package
def sql_query(sqlite_file, sql_query, fetch_level = 0, fetch_size = 5):
    # Import packages
    from sqlalchemy import create_engine
    import pandas as pd

    # Create Engine and SQL Query
    engine = create_engine("sqlite:///" + sqlite_file)
    table_names = engine.table_names()
    with engine.connect() as con:
        rs = con.execute(sql_query)
        # Fetch Level must be either 0 or 1
        if fetch_level == 0:
            df = pd.DataFrame(rs.fetchall())
        else:
            df = pd.DataFrame(rs.fetchmany(fetch_size))
        df.columns = rs.keys()
        print(df.head())
        con.close()


# Test
sql_query("Chinook.sqlite", "SELECT * FROM Album", 0)
sql_query("Chinook.sqlite", "SELECT * FROM Employee WHERE EmployeeID >= 6")



# INNER JOIN
with engine.connect() as con:
    rs = con.execute("SELECT Album.Title, Artist.Name FROM Album INNER JOIN Artist ON Album.ArtistID = Artist.ArtistID")
    df = pd.DataFrame(rs.fetchall())
    df.columns = rs.keys()
    print(df.head())
con.close()

# Inner Join with Milliseconds < 250000
df = pd.read_sql_query("SELECT * FROM PlaylistTrack INNER JOIN Track on PlaylistTrack.TrackId = Track.TrackId WHERE Milliseconds < 250000",engine)
print(df.head())

