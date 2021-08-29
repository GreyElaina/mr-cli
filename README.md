# mr-cli - a simple monorepo solution for python and poetry

`mr-cli` 是一个为 python 和 poetry 实现的简单的 Monorepo 解决方案, 通过替换 pyproject.toml 实现.
~~所以我还是不明白为什么我要写这样一个糟糕的东西.~~

## Installation / 安装

```bash
pip install mr-cli

# poetry, as a dev dependency
poetry add mr-cli --dev
```

## How to use / 使用方式

通过 `mr new` 指令新建一个子包:

```bash
mr new pkg_name
```

通过 `mr use` 将分包的配置载入当前工作区.  
需要手动切 vscode/pycharm 的 venv 配置:

```bash
mr use pkg_name
```

删除一个分包:

```bash
mr remove pkg_name
```

列出能找到的所有分包:

```bash
mr ls
```

从指定分包切出:

```bash
mr reset
```

将当前目录下的 `pyproject.toml` 保存为指定分包:

```bash
mr save pkg_name

# 如果想直接确认
mr save pkg_name --confirmed
```

# License / 许可

本项目使用 MIT License.