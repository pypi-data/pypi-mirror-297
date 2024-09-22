import numbers
import pickle
import sqlite3
from typing import Any, Text, Union

from pyassorted.asyncio.executor import run_func

PrimitiveType = Union[str, numbers.Number]


class SqliteDict(object):
    """The SqliteDict class is a dictionary-like object that stores its data in a SQLite database.

    Examples
    --------
    >>> import asyncio
    >>> from pyassorted.collections.sqlitedict import SqliteDict
    >>>
    >>> sql_dict = SqliteDict(":memory:")
    >>> sql_dict["key"] = "value"
    >>> assert sql_dict["key"] == "value"
    >>>
    >>> # Asynchronous usage
    >>> async def main():
    ...     await sql_dict.async_set("key", "value")
    ...     assert (await sql_dict.async_get("key")) == "value"
    >>>
    >>> asyncio.run(main())
    """

    def __init__(
        self,
        sqlite_filepath: Text = ":memory:",
        tablename: Text = "cache",
        auto_commit: bool = True,
        **kwargs,
    ):
        self._sqlite_filepath = sqlite_filepath
        self._tablename = tablename
        self.auto_commit = auto_commit

        self._conn = sqlite3.connect(self._sqlite_filepath, check_same_thread=False)
        self._cursor = self._conn.cursor()
        self._cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self._tablename} (key TEXT PRIMARY KEY, value TEXT)"
        )
        self._conn.commit()

    def __len__(self) -> int:
        self._cursor.execute(f"SELECT COUNT(*) FROM {self._tablename}")
        return self._cursor.fetchone()[0]

    def __getitem__(self, key: PrimitiveType) -> Any:
        self.validate_key(key=key)
        self._cursor.execute(f"SELECT value FROM {self._tablename} WHERE key=?", (key,))
        fetch_result = self._cursor.fetchone()
        if fetch_result is None:
            raise KeyError(f"Key {key} not found")
        value_bytes = fetch_result[0]
        return pickle.loads(value_bytes)

    def __setitem__(self, key: PrimitiveType, value: Any):
        self.validate_key(key=key)
        value_bytes = pickle.dumps(value)
        self._cursor.execute(
            f"INSERT OR REPLACE INTO {self._tablename} (key, value) VALUES (?, ?)",
            (key, value_bytes),
        )
        if self.auto_commit:
            self.commit()

    def __iter__(self):
        self._cursor.execute(f"SELECT key, value FROM {self._tablename}")
        for row in self._cursor:
            yield (row[0], pickle.loads(row[1]))

    def __contains__(self, key: PrimitiveType) -> bool:
        self.validate_key(key=key)
        self._cursor.execute(
            f"SELECT COUNT(*) FROM {self._tablename} WHERE key=?", (key,)
        )
        return self._cursor.fetchone()[0] > 0

    def __delitem__(self, key: PrimitiveType):
        self.validate_key(key=key)
        self._cursor.execute(f"DELETE FROM {self._tablename} WHERE key=?", (key,))
        if self.auto_commit:
            self.commit()

    def set(self, key: PrimitiveType, value: Any):
        self[key] = value

    def get(self, key: PrimitiveType, default: Any = None) -> Any:
        self.validate_key(key=key)
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: PrimitiveType, default: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            return default

    def commit(self):
        self._conn.commit()

    def items(self):
        return self.__iter__()

    async def async_set(self, key: PrimitiveType, value: Any):
        await run_func(self.set, key=key, value=value)
        if self.auto_commit:
            await run_func(self.commit)

    async def async_get(self, key: PrimitiveType):
        return await run_func(self.get, key=key)

    def validate_key(self, key: Any, raise_error: bool = True) -> bool:
        if isinstance(key, (str, numbers.Number, None)):
            return True
        if raise_error:
            raise TypeError(f"Key must be a primitive type, got {type(key)}")
        return False
