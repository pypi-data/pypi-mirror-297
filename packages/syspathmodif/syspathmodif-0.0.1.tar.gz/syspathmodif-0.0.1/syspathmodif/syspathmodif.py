from pathlib import Path
import sys


def sp_append(some_path):
	"""
	Appends the given path to the end of list sys.path if it does not already
	contain the path. If the path is of type pathlib.Path, it will be converted
	to a string.

	Args:
		some_path (str or pathlib.Path): the path to append to sys.path.

	Throws:
		TypeError: if argument some_path is not of type str or pathlib.Path.
	"""
	some_path = _ensure_path_is_str(some_path)

	if some_path not in sys.path:
		sys.path.append(some_path)


def sp_contains(some_path):
	"""
	Indicates whether list sys.path contains the given path.

	Args:
		some_path (str or pathlib.Path): the path whose presence is verified.

	Returns:
		bool: True if sys.path contains argument some_path, False otherwise.

	Throws:
		TypeError: if argument some_path is not of type str or pathlib.Path.
	"""
	some_path = _ensure_path_is_str(some_path)
	return some_path in sys.path


def sp_remove(some_path):
	"""
	Removes the given path from list sys.path if it contains the path.

	Args:
		some_path (str or pathlib.Path): the path to remove from sys.path.

	Throws:
		TypeError: if argument some_path is not of type str or pathlib.Path.
	"""
	some_path = _ensure_path_is_str(some_path)

	if some_path in sys.path:
		sys.path.remove(some_path)


def _ensure_path_is_str(some_path):
	if isinstance(some_path, str):
		return some_path
	elif isinstance(some_path, Path):
		return str(some_path)
	else:
		raise TypeError("A path must be of type str or pathlib.Path.")
