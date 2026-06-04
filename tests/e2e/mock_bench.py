"""A lightweight mock 'bench-ready' frappe module for local E2E runs.

Enable by setting environment variable `E2E_FORCE_MOCK=1` before running pytest.

This shim implements the minimal subset of the frappe API used by the E2E tests
so tests won't be skipped. It is not a full replacement for a real bench.
"""
from types import ModuleType
import threading


class _InMemoryDB:
    def __init__(self):
        self._lock = threading.Lock()
        self._data = {}  # {(doctype, name): doc}

    def exists(self, doctype, name):
        with self._lock:
            return (doctype, name) in self._data

    def get_value(self, doctype, name, fieldname=None):
        with self._lock:
            doc = self._data.get((doctype, name))
            if not doc:
                return None
            if fieldname:
                return getattr(doc, fieldname, None)
            return doc

    def insert(self, doctype, name, doc):
        with self._lock:
            self._data[(doctype, name)] = doc


class _LocalContext:
    def __init__(self):
        self.site = "mock-site"


class _Doc:
    def __init__(self, doctype=None):
        self.doctype = doctype
        self.name = None
        self._saved = False

    def save(self, ignore_permissions=False):
        if not self.name:
            # assign a mock name
            self.name = f"MOCK-{id(self)}"
        self._saved = True


def get_mock_frappe():
    m = ModuleType("frappe")

    # minimal attributes
    m.local = _LocalContext()
    m.db = _InMemoryDB()
    m.session = type("S", (), {"user": "Administrator"})()

    def connect():
        # no-op for mock
        m.local = _LocalContext()
        return True

    def clear_cache():
        # no-op
        return True

    def set_user(user):
        m.session.user = user

    def new_doc(doctype):
        d = _Doc(doctype=doctype)
        return d

    def get_doc(arg):
        # if arg is dict-like create a _Doc wrapper
        if isinstance(arg, dict):
            d = _Doc(doctype=arg.get("doctype"))
            for k, v in arg.items():
                setattr(d, k, v)
            return d
        return _Doc()

    # defaults helper used in some tests
    class defaults:
        @staticmethod
        def get_user_default(key):
            return None

    # attach functions
    m.connect = connect
    m.clear_cache = clear_cache
    m.set_user = set_user
    m.new_doc = new_doc
    m.get_doc = get_doc
    m.defaults = defaults

    # Exceptions placeholder
    class ValidationError(Exception):
        pass

    m.ValidationError = ValidationError

    return m


if __name__ == "__main__":
    # quick local smoke test
    f = get_mock_frappe()
    assert hasattr(f, "connect")
    print("mock frappe ready")
