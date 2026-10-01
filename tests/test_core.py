import tempfile
import unittest
from pathlib import Path

from todo import cli, core, storage


class CoreTests(unittest.TestCase):
    def test_add_assigns_incrementing_ids(self):
        todos, a = core.add([], "买牛奶")
        todos, b = core.add(todos, "写代码")
        self.assertEqual((a["id"], b["id"]), (1, 2))
        self.assertFalse(a["done"])

    def test_add_rejects_empty_text(self):
        with self.assertRaises(ValueError):
            core.add([], "   ")

    def test_remove_does_not_shift_other_ids(self):
        todos, _ = core.add([], "a")
        todos, _ = core.add(todos, "b")
        todos, _ = core.add(todos, "c")
        todos = core.remove(todos, 1)
        self.assertEqual([t["id"] for t in todos], [2, 3])
        _, d = core.add(todos, "d")
        self.assertEqual(d["id"], 4)

    def test_mark_done_does_not_mutate_input(self):
        todos, _ = core.add([], "a")
        new = core.mark_done(todos, 1)
        self.assertTrue(new[0]["done"])
        self.assertFalse(todos[0]["done"])

    def test_missing_id_raises(self):
        with self.assertRaises(KeyError):
            core.mark_done([], 1)
        with self.assertRaises(KeyError):
            core.remove([], 1)

    def test_format_list(self):
        self.assertEqual(core.format_list([]), "没有待办事项。")
        todos, _ = core.add([], "a")
        todos = core.mark_done(todos, 1)
        self.assertEqual(core.format_list(todos), "1. [x] a")


class StorageAndCliTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.path = str(Path(self.dir.name) / "todos.json")

    def run_cli(self, *args):
        return cli.main(["--file", self.path, *args])

    def test_load_missing_file_is_empty(self):
        self.assertEqual(storage.load(self.path), [])

    def test_save_and_load_roundtrip_with_unicode(self):
        data = [{"id": 1, "text": "买牛奶", "done": False}]
        storage.save(data, self.path)
        self.assertEqual(storage.load(self.path), data)

    def test_corrupt_file_gives_error_exit_code(self):
        Path(self.path).write_text("{oops", encoding="utf-8")
        self.assertEqual(self.run_cli("list"), 1)

    def test_full_flow(self):
        self.assertEqual(self.run_cli("add", "买牛奶"), 0)
        self.assertEqual(self.run_cli("done", "1"), 0)
        self.assertTrue(storage.load(self.path)[0]["done"])
        self.assertEqual(self.run_cli("remove", "1"), 0)
        self.assertEqual(storage.load(self.path), [])

    def test_unknown_id_exit_code(self):
        self.assertEqual(self.run_cli("done", "99"), 1)


if __name__ == "__main__":
    unittest.main()
