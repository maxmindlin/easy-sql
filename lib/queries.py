from __future__ import annotations
from typing import List, Optional


class SQLQueryBuilder:
    """Deconstructs a query string into its different components. Theres are stored
    internally, altered, and then returned in different formats.
    
    Currently uses a dict of strings as storage containers, but something else might
    be more efficient or powerful."""

    def __init__(self) -> SQLQueryBuilder:
        self._query = {
            "select": "",
            "from": "",
            "join": "",
            "where": "",
            "group": "",
            "order": "",
            "limit": ""
        }

    def SELECT(self, selects: List[str]) -> SQLQueryBuilder:
        """General select statement.
        Takes a list of field names - if singluar, still put it in a list of one."""

        self._query["select"] = "SELECT " + ", ".join(selects)

        return self
    
    def FROM(self, table: str, alias: Optional[str] = None) -> SQLQueryBuilder:

        self._query["from"] += "FROM " + table + " "
        if alias:
            self._query["from"] += "AS " + alias + " "
        
        return self

    def JOIN(self, to: str, alias: Optional[str] = None) -> SQLQueryBuilder:
        
        self._query["join"] += "JOIN " + to + " "
        if alias:
            self._query["join"] += "AS " + alias + " "
        
        return self
    
    def SUBQUERY(self, query_obj: SQLQueryBuilder, alias: str, join_left: str, join_right: str) -> SQLQueryBuilder:
        
        sub = query_obj.query
        self._query["join"] += "JOIN (" + sub + ") AS " + alias + " "
        self._query["join"] += "ON " + join_right + " = " + join_right + " "
        return self
    
    def LEFT(self) -> SQLQueryBuilder:
        """Adds a join using the 'LEFT' keyword."""

        self._query["join"] = "LEFT " + self._query["join"]
        return self
    
    def INNER(self) -> SQLQueryBuilder:
        """Adds a join using the 'INNER' keyword."""

        self._query["join"] = "INNER " + self._query["join"]
        return self
    
    def USING(self, field: str) -> SQLQueryBuilder:

        self._query["join"] += "USING (" + field + ") "
        return self

    def ON(self, field_left: str, field_right: str) -> SQLQueryBuilder:
        """Joining method using 'ON' keyword. 
        
        :param field_left: field name in the table being joined to.

        :param field_right: field name in the table joining."""

        self._query["join"] += "ON " + field_left + " = " + field_right + " "
        return self
    
    def WHERE(self, s: str) -> SQLQueryBuilder:

        first_cond = False

        l = self._query["where"].split()

        if "WHERE" not in l:
            # This is the first conditional added
            # Therefore need to add 'WHERE' keyword
            # and no 'AND' is needed
            self._query["where"] += "WHERE "
            first_cond = True

        if not first_cond:
            self._query["where"] += "AND "

        self._query["where"] += s + " "

        return self

    def GROUPBY(self, cond: List[str]) -> SQLQueryBuilder:

        self._query["group"] += "GROUP BY " + ", ".join(cond) + " "

        return self

    def ORDERBY(self, field: str, by: Optional[str] = None) -> SQLQueryBuilder:

        self._query["order"] += "ORDER BY " + field + " "

        if by:
            self._query["order"] += by + " "

        return self

    def LIMIT(self, l: int) -> SQLQueryBuilder:

        self._query["limit"] += "LIMIT " + str(l) + " "
        return self


    @property
    def query(self) -> str:
        """Return query constructed as a string."""

        statements = [s for s in list(self._query.values()) if s != ""]
        return " ".join(statements)
