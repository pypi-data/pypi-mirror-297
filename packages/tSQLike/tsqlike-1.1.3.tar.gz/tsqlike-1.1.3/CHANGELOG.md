# CHANGELOG

* **2024.09.19    tSQLike-1.1.3**
  * `detect_types=False` renamed to `detect_str_types=False`
  * `str_to_type()` `use_none=False` whether to convert empty strings to `None` or not; Boolean conversion fix

* **2024.07.07    tSQLike-1.1.2**
  * `join_lt()` Fast modification

* **2024.07.03    tSQLike-1.1.1**
  * `select_lt()` to accept `<` comparison operator

* **2024.07.02    tSQLike-1.1.0**
  * Import methods use `detect_types` to detect if auto-conversion from `str` to `int`, `float` and `bool` is needed

* **2024.06.28    tSQLike-1.0.4**
  * `select_lt()` respects empty arguments

* **2024.06.24    tSQLike-1.0.3**
  * `write_json()` defaults to `export_f='export_list_dicts()'`
  * `read_json()` implemented as a standalone function
  * `read_csv()` became standalone
  * `Table` auto-import on init of `dict(lists)` fixed
  * `README.md` updated
  * `write_json_lt()` added
  * `README.md` updated

* **2024.06.06    tSQLike-1.0.2**
  * `tSQLike` has been published to PyPI automatically

* **2024.06.06    tSQLike-1.0.1**
  * Package created and uploaded to PyPI manually

* **2024.06.06    tSQLike-1.0.0**
  * The first release
