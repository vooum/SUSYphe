# Smodels2 说明文档

**作者：** 贾兴隆

`SmodelS` 是一个使用 LHC 数据限制粒子物理简化模型的 `Python` 自动化工具，目前最新版本的 `SmodelS` 对 `Python` 版本的要求为 **3.6** 及以上。它的运行流程整体上分为两个步骤。第一步是将 BSM 模型拆解为简化模型的拓扑情形。第二步是根据 LHC 数据对这些拓扑情形做出限制。鉴于 `SmodelS` 是一个规模庞大的程序包，所以本文档暂时只讨论最必要的内容，至于剩余的内容欢迎大家共同添加。

## Smodels 官方网站

- 官网：<https://smodels.github.io/>
- 用户手册：<https://smodels.readthedocs.io/en/stable/>
- GitHub：<https://github.com/SModelS/smodels>
- 数据库 GitHub：<https://github.com/SModelS/smodels-database-release>

## 安装方法

### Smodels 的依赖

`SmodelS` 是一个使用 `Python` 语言编写的程序包，同时也用到了许多 `Python` 的扩展模块。因此在安装和使用 `SmodelS` 之前首先，要确保 `Python` 以及这些依赖项的版本要求得到了满足，可以使用 `pip install` 或者 `conda install` 命令安装这些依赖，也可以通过使用 `setuptools` 的方式安装 `SmodelS` 以避免逐一安装这些依赖项。

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

除此以外 `SmodelS` 还提供了一些可选功能，这些可选功能对环境有一些额外的依赖：

- 如果要使用 `SmodelS` 的截面计算器，则系统需要安装 `C++` 以及 `fortran` 编译器，`SmodelS` 会使用它们安装 `Pythia 8.3` 以及 `NLL-fast`。
- 数据库浏览功能需要安装 `IPython`。
- 交互式绘图功能需要安装 `plotly` 以及 `Pandas`。

### Smodels 的安装

在安装完所有必要的依赖后就可以开始安装 `SmodelS` 了，一共有三种方法可以安装。

#### 源代码安装（推荐）

从 GitHub 上可以下载到 `SmodelS` 源代码文件 `smodels-X.X.X.tar.gz`，解压后可得到 `smodels-X.X.X` 文件，进入到 `smodels-X.X.X` 文件中即可执行安装命令。

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

`SmodelS` 也可以使用 `pip` 直接安装，命令是：

```bash
pip install smodels
```

这种方式同样不需要提前处理依赖问题，`pip` 会自动下载所需的依赖项。

在这种情况下 `SmodelS` 以及示例文件和参数文件会直接安装到特定的 `Python` 包目录中，具体依赖于所使用的 `Python` 环境。此时可能需要调整某些环境变量，如 `$PATH, $PYTHONPATH, $LD_LIBRARY_PATH`。数据库文件例外，可以不安装到该目录中。

如果遇到权限问题的话，则需要使用 `sudo` 命令获得权限，或者可以使用以下命令进行安装：

```bash
pip install --user smodels 
```

这种方式只推荐比较有经验的 `Python` 使用者使用。

### Smodels Database

`SmodelS` 数据库包含 LHC 相关的数据，`SmodelS` 正是通过对比简化模型的拓扑结构以及数据库信息从而得出对特定模型的 LHC 限制。

#### 数据库的类型

`SmodelS` 数据库一共有两种类型的数据，分别是 `UL` 类型和 `EM` 类型。

- `UL` 类型是 `SmodelS` 中大多数数据的数据类型，指的是以产生截面的上限来作为限制的来源。
- `EM` 类型是以产生效率来作为限制的来源。

这部分可以详见：<https://smodels.readthedocs.io/en/stable/DatabaseDefinitions.html#emtype>

#### Smodels Database 的安装方法

新下载安装的 `SmodelS` 不自带数据库，需要进行安装。

以下载源代码安装为例，解压后的文件夹中存在一个名为 `parameters.ini` 的文件，这是 `SmodelS` 的配置文件。其中有一项配置是 `[database]`，该项配置负责设定数据库文件所在的位置。具体的安装方法有两种。

#### 使用内置的官方链接

最简单的方式是使用官方内置的链接作为数据库路径，这种方式需要确保网络连接通畅，能够连接到 `Smodels Database` 的网络地址。设置配置文件中的 `[database]` 项为以下内容即可：

```ini
path = official
```

在这种情况下，运行 `SmodelS` 会自动下载相应版本的数据库二进制文件。默认情况下，数据库会被下载到用户的 `.cache/smodels/` 目录下。如果想把数据库缓存至其他位置，则需要设置环境变量 `SMODELS_CACHEDIR`，数据库会缓存至该环境变量所指向的目录。

从 v2.2.0 版本开始，部分 `EM` 类型的数据在官方数据库中被进行了整合和汇总，这能加快运行速度。如果不想使用整合后的数据，可以使用以下命令安装数据库

```ini
path = official+nonaggregated
```

#### 手动下载数据库

另一种方式是自行前往数据库的 GitHub 地址下载数据库

数据库的 GitHub 地址是：<https://github.com/SModelS/smodels-database-release>

下载后可解压至任意位置，只需要在 `[database]` 项中指定与参数文件的相对路径或绝对路径即可，例如，若数据库文件放置于与参数文件同一级目录的话：

```ini
path = ./smodels-database/
```

同样的，如果不想使用被整合的 `EM` 类型数据，则解压   `smodels-database` 中的 `nonaggregated220.tar.gz` 文件即可。

如果选择这种方式安装数据库，那么安装完成后首次运行 `SmodelS` 时，`SmodelS` 会自动使用数据库中的文本文件生成二进制文件。

### 使用 Smodels

`SmodelS` 可以接收 SLHA 以及 LHE 格式的文件作为输入，并提供了包括命令行工具，以及自定义脚本在内的两种运行方式。如果输入模型为非 `MSSM` 模型，用户可能需要自行在 `model.py` 中定义 BSM 粒子。

#### `SmodelS` 的输入文件

此处暂时只介绍 SLHA 格式文件作为输入文件的情形。

`SmodelS` 可以读取标准的 SLHA 格式文件，从而获取相应的所有信息。但 SLHA 格式文件并不包含对撞机产生 BSM 粒子的产生截面信息，因此这一部分信息需要自行添加。

下面是一个标准的截面信息描述格式的示例

```SLHA
XSECTION SQRTS PDG_CODE1 PDG_CODE2 NF PDG_CODE3 PDG_CODE4
SCALE_SCHEME QCD_ORDER EW_ORDER KAPPA_F KAPPA_R  PDF_ID VALUE CODE VERSION
```

第一行的含义分别是：

- XSECTION: Block 标记。当 `SmodelS` 读取 SLHA 文件时，读取到该标记就能知道这部分为截面信息
- SQRTS: 一个浮点数，对撞机质心能，单位为 GeV
- PDG_CODE1 PDG_CODE2: 均为整数，对撞粒子的 PDG 编号，质子为 2212
- NF: 一个整数，末态粒子的数量
- PDG_CODE3 PDG_CODE4 ... : 均为整数，末态粒子的 PDG 编号

第二行的含义分别是：

- SCALE_SCHEME: 一个整数，选择指定的中心标度，目前可选项有
    0: 中心标度为产生粒子的平均质量。
    1: 固定标度
    2: 标度设定为质心能
    3: 标度为末态粒子的横向质量
- QCD_ORDER: QCD 修正阶数

下面是一个来自 `SmodelS` 官网的具体例子

![xsecBlock](./xsecBlock.jpg)
