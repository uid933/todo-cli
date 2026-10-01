# todo-cli

一个只用 Python 标准库写的命令行待办清单。数据保存在当前目录的 `todos.json`。

## 使用

需要 Python 3.8+,无需安装任何依赖:

```bash
python -m todo add "买牛奶"
python -m todo list
python -m todo done 1
python -m todo remove 1
```

示例输出:

```
$ python -m todo list
1. [x] 买牛奶
2. [ ] 写 README
```

可选:`pip install .` 后可直接用 `todo add "..."`。
用 `--file 路径` 可指定别的数据文件。

## 测试

```bash
python -m unittest discover -s tests -v
```

## 结构

- `todo/core.py` — 纯逻辑(增、完成、删、格式化),不做 I/O
- `todo/storage.py` — JSON 读写
- `todo/cli.py` — argparse 命令行入口

## 许可证

MIT
