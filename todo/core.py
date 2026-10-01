"""Pure todo logic: no file or terminal I/O, so it is easy to test.

A todo is a dict: {"id": int, "text": str, "done": bool}.
A new id is max(existing ids) + 1, so ids of other items never shift when
something is removed (removing the newest item frees its id).
"""


def add(todos, text):
    """Return (new_list, new_item). Raises ValueError for empty text."""
    text = text.strip()
    if not text:
        raise ValueError("待办内容不能为空")
    next_id = max((t["id"] for t in todos), default=0) + 1
    item = {"id": next_id, "text": text, "done": False}
    return todos + [item], item


def _find(todos, todo_id):
    for t in todos:
        if t["id"] == todo_id:
            return t
    raise KeyError(f"找不到编号为 {todo_id} 的待办")


def mark_done(todos, todo_id):
    """Return a new list with the item marked done. Raises KeyError if missing."""
    _find(todos, todo_id)
    return [{**t, "done": True} if t["id"] == todo_id else t for t in todos]


def remove(todos, todo_id):
    """Return a new list without the item. Raises KeyError if missing."""
    _find(todos, todo_id)
    return [t for t in todos if t["id"] != todo_id]


def format_list(todos):
    if not todos:
        return "没有待办事项。"
    return "\n".join(
        f"{t['id']}. [{'x' if t['done'] else ' '}] {t['text']}" for t in todos
    )
