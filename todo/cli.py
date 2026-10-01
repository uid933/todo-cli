"""Command line entry point."""

import argparse
import sys

from . import core, storage


def build_parser():
    parser = argparse.ArgumentParser(prog="todo", description="简单的命令行待办清单")
    parser.add_argument(
        "--file", default=str(storage.DEFAULT_PATH), help="数据文件路径 (默认 todos.json)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add", help="添加待办")
    p.add_argument("text")
    sub.add_parser("list", help="列出所有待办")
    p = sub.add_parser("done", help="标记为已完成")
    p.add_argument("id", type=int)
    p = sub.add_parser("remove", help="删除待办")
    p.add_argument("id", type=int)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        todos = storage.load(args.file)
        if args.command == "add":
            todos, item = core.add(todos, args.text)
            storage.save(todos, args.file)
            print(f"已添加 #{item['id']}: {item['text']}")
        elif args.command == "list":
            print(core.format_list(todos))
        elif args.command == "done":
            storage.save(core.mark_done(todos, args.id), args.file)
            print(f"已完成 #{args.id}")
        elif args.command == "remove":
            storage.save(core.remove(todos, args.id), args.file)
            print(f"已删除 #{args.id}")
    except (KeyError, ValueError) as e:
        # KeyError's str() adds quotes; use the message itself.
        print(f"错误: {e.args[0]}", file=sys.stderr)
        return 1
    return 0
