# Smodels2 说明文档

**作者：** 贾兴隆

`Smodels` 是一个使用 LHC 数据限制粒子物理简化模型的 `Python` 自动化工具，目前最新版本的 `Smodels` 对 `Python` 版本的要求为 **3.6** 及以上。它的运行流程整体上分为两个步骤。第一步是将 BSM 模型拆解为简化模型的拓扑情形。第二步是根据 LHC 数据对这些拓扑情形做出限制。

## Smodels 官方网站

- 官网：<https://smodels.github.io/>
- 用户手册：<https://smodels.readthedocs.io/en/stable/>
- GitHub：<https://github.com/SModelS/smodels>
- 数据库 GitHub：<https://github.com/SModelS/smodels-database-release>

## 安装方法

### Smodels 的依赖

`Smodels` 是一个使用 `Python` 语言编写的程序包，同时也用到了许多 `Python` 的扩展模块。因此在安装和使用 `Smodels` 之前首先，要确保 `Python` 以及这些依赖项的版本要求得到了满足，可以使用 `pip install` 或者 `conda install` 命令安装这些依赖，也可以通过使用 `setuptools` 的方式安装 `Smodels` 以避免逐一安装这些依赖项。

**这些依赖项包括：**

```text
- docutils>=0.3
- numpy>=1.18.0,!=1.21.*
- scipy>=1.0.0
- unum>=4.0.0
- requests>=2.0.0
- pyslha>=3.1.0
- pyhf>=0.6.1
- jsonpatch>=1.25
- jsonschema>=3.2.0
```

这里需要特别提一下 `pyslha` 和 `pyhf` 这两个库：

- `pyslha` 库是一个用于读取和解析 SLHA 格式文本文件的库。
- `pyhf` 库是一个用于处理高能物理中统计问题的库。此外，如果有条件的话可以安装 `pytorch>=1.8.0` 作为 `pyhf` 的计算后端，这可以提升运行速度。

除此以外 `Smodels` 还提供了一些可选功能，这些可选功能对环境有一些额外的依赖：

- 如果要使用 `Smodels` 的截面计算器，则系统需要安装 `C++` 以及 `fortran` 编译器，`Smodels` 会使用它们安装 `Pythia 8.3` 以及 `NLL-fast`。
- 数据库浏览功能需要安装 `IPython`。
- 交互式绘图功能需要安装 `plotly` 以及 `Pandas`。

### Smodels 的安装

在安装完所有必要的依赖后就可以开始安装 `Smodels` 了，一共有三种方法可以安装。

#### 源代码安装（推荐）

从 GitHub 上可以下载到 `Smodels` 源代码文件 `smodels-X.X.X.tar.gz`，解压后可得到 `smodels-X.X.X` 文件，进入到 `smodels-X.X.X` 文件中即可执行安装命令。

在运行安装命令之前，可执行以下脚本检查依赖：

```bash
./smodelsTools.py toolbox
```

检查无误后即可运行以下命令进行安装:

```bash
make smodels
```

如果不需要安装 `Pythia` 以及 `NLL-fast` 可以使用以下命令进行安装：

```bash
make smodels_noexternaltools
```

#### 使用 setuptools 安装

该方法同样需要下载源代码文件，如果当前环境安装了 `Python` 的 `setuptools` 库，即可使用以下命令进行安装：

```bash
setup.py install
```

如果使用这种安装方法，则不需要提前安装所有的依赖项，该脚本会自动处理所有依赖问题。

如果因为需要改动系统目录，没有权限而导致执行失败的话，则需要使用 `sudo` 命令获得权限，或者可以使用以下命令安装到用户目录下：

```bash
setup.py install --user
```

#### 使用 pip 安装

`Smodels` 也可以使用 `pip` 直接安装，命令是：

```bash
pip install smodels
```

这种方式同样不需要提前处理依赖问题，`pip` 会自动下载所需的依赖项。

在这种情况下 `Smodels` 以及示例文件和参数文件会直接安装到特定的 `Python` 包目录中，具体依赖于所使用的 `Python` 环境。此时可能需要调整某些环境变量，如 `$PATH, $PYTHONPATH, $LD_LIBRARY_PATH`。数据库文件例外，可以不安装到该目录中。

如果遇到权限问题的话，则需要使用 `sudo` 命令获得权限，或者可以使用以下命令进行安装：

```bash
pip install --user smodels 
```

这种方式只推荐比较有经验的 `Python` 使用者使用。

### Smodels Database 的安装

`Smodels` 数据库包含 LHC 相关的数据，`Smodels` 正是通过对比简化模型的拓扑结构以及数据库信息从而得出对特定模型的 LHC 限制。

以下载源代码安装为例，解压后的文件夹中存在一个名为 `parameters.ini` 的文件，这是 `Smodels` 的配置文件。其中有一项配置是 `[database]`，该项配置负责设定数据库文件所在的位置。

刚刚下载安装的 `Smodels` 不自带数据库，均需要进行安装，一共有两种安装方法。

#### 使用内置的官方链接

最简单的方式是使用官方内置的链接作为数据库路径，这种方式需要确保网络连接通畅，能够连接到 `Smodels Database` 的网络地址。设置配置文件中的 `[database]` 项为：

```ini
path = official
```

在这种情况下，运行 `Smodels` 会自动下载相应版本的数据库文件。默认情况下，数据库会被下载到 `.cache/smodels/` 目录下，
