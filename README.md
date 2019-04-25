Sometimes you just need a lightweight DB client outside a traditional MVC.

Requires a .env file in the format:
```
DB_USER=
DB_PASS=
DB_HOST=
DB_PORT=
DB_NAME=
DB_TUNNEL=
```
Keeping this consistent makes connecting easier.

Example usage:

```python
query = (
    EasySQL(".env", tunnel=True)
    .SELECT(["users","user_ids"])
    .FROM("user_table", alias="ut")
    .JOIN("clients", alias="c").LEFT().USING("ID")
    .WHERE("c.status = 1")
    .WHERE("ut.name = 'John'")
    .ORDERBY("ut.date_created", by="desc")
    .LIMIT(250)
)

data: pd.DataFrame = query.execute 
```

You can also pull out a new SQL client like so:

```python
client = EasySQL(".env").new()
```

This just a wrap for the mysql-connector class, so it can be used similarly by pulling out the client:

```python
# This returns a mysql.connector object
EasySQL(".env").new().client
```

or by using the EasySQL methods for DataFrame responses:

```python
data: pd.DataFrame = EasySQL(".env").new().data_frame_query(query_string)
```