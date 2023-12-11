# 各软件安装说明

## 常用工具和命令

### `tar` 工具

用于压缩和解压缩工作，对于 `tar.gz` 后缀的压缩包，使用以下命令解压：

```bash
tar -zxvf package.tar.gz
```

`-z` 参数表示使用 gzip 来压缩/解压缩文件\
`-x` 参数表示解压\
`-v` 参数表示打印压缩/解压缩的部分细节（可选）\
`-f` 参数表示将在后方指定目标文件名

### `vim` 编辑器

vim 是用于查看和编辑文本文件的软件，常用命令：

- 按 `i` 或 `insert` 键进入编辑模式。
- 输入 `:` 进入命令模式。
- 如果没有进行过修改，可以在命令模式中输入 `q` 直接退出。
- 如果已经进行过修改，可以在命令模式中输入 `q!` 放弃修改并退出。
- 如果已经进行过修改，可以在命令模式中输入 `w` 执行写入，即把修改保存下来。
- 如果已经进行过修改，可以在命令模式中输入 `wq` 执行写入并退出。
- 按 `delete` 键直接删除光标所在字符

## Prospino

## SModelS

## MadGraph

## CERN ROOT

CERN ROOT 有很多安装方法，下面只介绍一下 Ubuntu 系统上的源代码安装方式

### 下载 ROOT 源码压缩包，处理依赖

首先需要到 CERN ROOT 的官网下载源代码安装包 <https://root.cern/install/#ubuntu-and-debian-based-distributions>

注意在 <https://root.cern/install/dependencies/#ubuntu-and-other-debian-based-distributions> 查看所有必要的依赖

> **注意：** 不同版本的 CERN ROOT 之间很可能依赖项不同

以 `root 6.28.06` 版本为例，下载后得到的是一个 `.tar.gz` 后缀的文件，因此需要使用 `tar` 命令解压

```bash
tar -zxf root_v6.28.06.source.tar.gz
```

解压后会获得 `root-6.28.06` 文件夹，进入这个文件夹

```bash
cd root-6.28.06/
```

### 建立 ROOT 的构建目录和安装目录

进入文件夹后，使用 `mkdir` 命令建立两个文件夹

```bash
mkdir builddir installdir
```

- `builddir` 目录为构建目录，在此目录内执行编译和安装操作，编译和安装过程中生成的中间产物会存放在此目录中
- `installdir` 目录为安装目录，软件最终会被安装到此处

建立完这两个目录后，切换到构建目录中

```bash
cd builddir
```

### 生成和配置 ROOT 构建文件

在 `builddir` 目录内，执行以下操作，生成构建文件

```bash
cmake -DCMAKE_INSTALL_PREFIX=../installdir ..
```

这行命令表示，将使用 `cmake` 进行整个软件的编译和安装

- 第一个参数 `-DCMAKE_INSTALL_PREFIX=../installdir` 表明软件将安装到 `../installdir` 下
- 第二个参数 `..` 表明软件源代码在 `..` 目录，即当前目录的上一层目录内

### 打开 ROOT 所有子软件库的开关

`cern root` 软件包括许多子软件库，这些子软件库拥有各不相同的功能，默认情况下，许多子软件库处于 `OFF` 状态，即不进行安装。我们选择安装全部子软件库，使用以下命令进行操作

```bash
sed -i '/minuit2:/s/OFF/ON/g' CMakeCache.txt
```

这个操作会把 `CMakeCache.txt` 文件中所有以 `minuit2:` 开头的行中的 `OFF` 全部替换为 `ON`

### 执行 ROOT 安装命令

完成以上所有操作后就可以进行 `cern root` 的安装了，使用以下命令

```bash
cmake3 --build . -- install -j20
```

即，使用 `cmake3` 在当前目录进行编译和安装操作

`-j` 表示准许同时使用的进程数。准许使用的进程数越多安装速度会越快，此处使用的是 20 个进程即 `-j20`

输入完命令后等待片刻，`cern root` 就会安装完毕

### 第一次打开 `cern root` 以及配置环境变量

此时 `cern root` 已经安装完毕，但输入 `root` 指令仍然无法进入 `cern root`，这是因为 `cern root` 还未被加载。

按照之前示例中一直使用的路径，使用以下命令加载 `cern root`

```bash
source root-6.28.06/installdir/bin/thisroot.sh
```

输入完以上命令后，即可输入 `root` 进入 `cern root` 界面

为了避免每次重新加载终端或重新登录后都必须手动加载一次 `cern root` 的麻烦，可以在环境变量中添加上面的加载命令

打开 `.bashrc`

```bash
vim ~/.bashrc
```

在 `.bashrc` 的末尾添加一行语句

```bashrc
source $PATH/root-6.28.06/installdir/bin/thisroot.sh # ROOT
```

`$PATH` 表示 `cern root` 所在的绝对路径

`#` 后面的 `ROOT` 是该行的一个注释，表示这一语句为加载 `cern root` 的语句，无实质作用。

这样未来每次重新启动终端或重新登陆后都可以直接使用 `root` 指令进入 `cern root`

## Delphes

### 下载 Delphes 安装包

前往 <https://cp3.irmp.ucl.ac.be/projects/delphes/wiki/Releases> 下载安装包

安装 Delphes 之前需要先安装 CERN ROOT，也需要注意处理其它依赖问题

> **注意：** Delphes 版本需要与 CERN ROOT 的版本进行一定的对应

### 安装 Delphes

使用 `tar` 命令解压，例如：

```bash
tar -zxf Delphes-3.5.0.tar.gz
```

在实际开始安装步骤前，首先需要加载 CERN ROOT 环境

```bash
source $PATH/root-6.xx.xx/installdir/bin/thisroot.sh
```

接下来进入 Delphes 文件夹内执行安装程序，例如：

```bash
cd Delphes-3.5.0/
./configure
make -j20
```

`-j` 表示准许同时使用的进程数。准许使用的进程数越多安装速度会越快，此处使用的是 20 个进程即 `-j20`。

## HepMC

### 下载 HepMC 安装包

前往 <https://gitlab.cern.ch:8443/hepmc/HepMC/-/tags> 下载安装包。

注意处理编译器等依赖项问题

### 安装 HepMC

以下载的压缩包为 `HepMC-2.06.11.tar.gz` 为例，首先进行解压缩操作：

```bash
tar -zxf HepMC-2.06.11.tar.gz
```

解压后进入 `HepMC-2.06.11` 文件夹：

```bash
cd HepMC-2.06.11/
```

建立并进入构建文件：

```bash
mkdir build
cd build
```

使用 cmake 进行编译，将 $PATH 替换为您的实际路径：

```bash
cmake -DCMAKE_INSTALL_PREFIX=$PATH/HepMC-2.06.11 -Dmomentum:STRING=GEV -Dlength:STRING=MM ../
```

最后执行 Makefile 相关命令进行安装：

```bash
make
make test
make install -j
```

## pythia

### 下载 Pythia 压缩包

前往 <https://pythia.org/releases/> 下载 Pythia 安装压缩包，注意关注编译器依赖等问题。

### 安装 Pythia

这里以下载的安装包为 `pythia8245.tgz` 为例，首先进行解压缩并进入文件夹内：

```bash
tar -zxf pythia8245.tgz
cd pythia8245
```

运行 `./configure` 进行安装配置：

```bash
./configure
```

如果需要额外指定一些外部包或者安装路径，则可以使用以下命令：

```bash
./configure --with-hepmc2=$PATH/HepMC-2.xx.xx --prefix=$PATH/pythia8245
```

`$PATH` 代表某个特定路径

`--with-hepmc2` 表示指定 `hepmc2` 软件包的路径

`--prefix` 指定 `pythia` 的安装路径

完成配置后，运行 `gmake` 或 `make` 执行 `Makefile` 进行安装，以执行 `make` 命令为例：

```bash
make -j20
make install
```

`-j20` 表示准许使用至多 20 个核心进行安装作业

## RestFrames

### 下载 RestFrames

首先前往 <http://restframes.com/downloads/> 下载 RestFrames 压缩包

### 安装 RestFrames

下载完成后解压 RestFrames 的压缩包

```bash
tar -zxf RestFrames-1.0.X.tar.gz
```

进入解压的文件夹，依次输入以下命令可以快速安装

```bash
./configure
make
make install
```

默认的 `./configure` 设置会将安装目录设定在 `/usr/local` 文件夹，如果想更换安装目录可以在运行 `./configure` 时指定参数

```bash
./configure --prefix=Install_Path
```

安装完成后还需要运行 RestFrames 配置文件才能使用

```bash
source setup_RestFrames.sh(csh) 
```

将这一命令改为绝对路径添加进环境变量 `~/.bashrc` 中即可在每次开启终端时自动运行 RestFrames 配置文件。

## CheckMATE

### 下载 CheckMATE 安装包

首先前往 CheckMATE 的 github 页面下载 CheckMATE 的源代码文件压缩包 <https://github.com/CheckMATE2/checkmate2>

下面将以截止 2023 年 12 月最新版本的 CheckMATE 为例。

### CheckMATE 依赖项

CheckMATE 对 Python 版本的要求是，如果是 Python2，则版本要大于 2.7.4，如果是 Python3 则版本要大于 3.4。同时需要安装 `future` 库。

CheckMATE 还要求当前环境安装了 `autoreconf` 库。

CheckMATE 依赖的高能物理软件包有：`Cern ROOT`、`Delphes 3.5`、`HEPMC2`，可选依赖有 `Pythia8.2`、`MadGraph5_aMC@NLO`

部分 CheckMATE 分析依赖 RestFrames，因此需要提前安装并加载 RestFrames 软件。

### 安装 CheckMATE

解压压缩包并进入后，首先运行 `autoreconf` 自动构建文件配置

```bash
autoreconf
```

接着运行配置文件，指定依赖项位置，例如：

```bash
./configure --with-delphes=/path/to/delphes --with-hepmc=/path/to/hepmc --with-madgraph=/path/to/madgraph --with-pythia=/path/to/pythia
```

最后运行 `make` 命令进行编译，可以通过 `-j` 参数指定多核编译，例如使用 4 核进行编译

```bash
make -j4
```
