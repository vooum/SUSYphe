# SUSYphe

SUSY phenomenology on LHC

这个项目的目的是重写 prospino-smodels-madgraph-checkmate 的自动化程序。

当前任务：控制 prospino2 的类

**推送代码发起 Pull request 时一定要推送到自己对应的那个分支上，不要推送到 main 分支，否则会影响代码审核和合并的工作量。**

## 2023/10/20

根据实际的推进情况，现在定为以下流程

```mermaid
graph TB
    A[读取数据] --> |从第一个参数点开始|B[判断 Siglino 类型];
    B -->|计算相应情况的 ElectroWeakino 截面| C[计算截面];
    C -->|某些 Siglino 类型个别截面不计算, 指定为 0| D{收集结果};
    D -->|如果参数点的截面没有全部计算完, 继续计算| C;
    D -->|如果参数点的截面全部计算完毕| E{导出结果到 CSV};
    E --> |计算下一个参数点的截面|B;
    E --> F[将所有截面信息写入 SModelS 输入文件];
    F --> G[多核运行 SModelS];
    G --> H[收集全部 SModelS py 结果];
    style A fill:#90EE90;
    style B fill:#90EE90;
    style C fill:#90EE90;
    style D fill:#90EE90;
    style E fill:#90EE90;
    style F fill:#f9f,stroke:#333,stroke-width:4px;
    style G fill:#f9f,stroke:#333,stroke-width:4px;
    style H fill:#f9f,stroke:#333,stroke-width:4px;
```

## 2023/10/04

更新流程图和文件结构。

下面的总流程图只是一个示意，**收集结果**后的内容需要讨论，是将所有截面计算完毕后再写入 `SModelS` 输入，还是当计算完一个参数点后立刻写入 `SModelS` 输入。

```mermaid
graph LR
    A{收集结果} --> B[将截面信息写入 SModelS 输入文件];
    B --> C[导出结果到 CSV];
    style A fill:#90EE90;
    style B fill:#f9f,stroke:#333,stroke-width:4px;
    style C fill:#90EE90;
```

```mermaid
graph LR
    A{收集结果} --> B[导出结果到 CSV];
    B --> C[将截面信息写入 SModelS 输入文件];
    style A fill:#90EE90;
    style B fill:#90EE90;
    style C fill:#f9f,stroke:#333,stroke-width:4px;
```

```mermaid
graph TB
    A[读取数据] --> B[判断 Siglino 类型];
    B -->|计算相应情况的 ElectroWeakino 截面| C[计算截面];
    C -->|某些 Siglino 类型个别截面不计算, 指定为 0| D{收集结果};
    D -->|如果参数点的截面没有全部计算完, 继续计算| C;
    D -->|如果参数点的截面全部计算完毕| E[导出结果到 CSV];
    D --> F[将截面信息写入 SModelS 输入文件];
    style A fill:#90EE90;
    style B fill:#90EE90;
    style C fill:#90EE90;
    style D fill:#90EE90;
    style E fill:#90EE90;
    style F fill:#f9f,stroke:#333,stroke-width:4px;
```

下面的文件结构仅供参考

- 这里把 `Program_CrossSection.py` 暂时改名为 `Program.py`
- 文件结构中添加了 `SModelS_Input` 文件夹，用于存放 `SModelS` 输入文件
- 文件结构中添加了 `SModelS_Output` 文件夹，用于存放 `SModelS` 输出文件

```text
Our_Program/
├── Program.py
├── Prospino_Input/
│   └── ProspinoIn_1.txt
├── Cross_Section/
│   └── Prospino2_*/
│      └── prospino_2.run
├── Prospino_Run/
│   ├── Pro2_subroutines/
│   ├── prospino.in.les_houches
│   └── prospino.dat
├── Results/
│   └── CrossSection.csv
├── SModelS_Input/
│   └── SModelS_1.slha
├── SModelS_Output/
│   └── SModelS_1.smodels
└── slhaReaderOutput.csv
```

## 2023/09/23

更新流程图和文件结构，**浅绿色方框**中的内容为新的目标

总的来说就是，分类讨论 Siglino 为不同 neutralino 时的情况，计算相关截面并处理某些情况下跳过某些截面的情况

```mermaid
graph TB
    A[读取数据] --> B[判断 Siglino 类型];
    B -->|计算相应情况的 ElectroWeakino 截面| C[计算截面];
    C -->|某些 Siglino 类型个别截面不计算, 指定为 0| D[收集结果];
    D -->|循环足够的次数把相应截面全都计算完| B;
    style A fill:#f9f,stroke:#333,stroke-width:4px;
    style B fill:#90EE90;
    style C fill:#f9f,stroke:#333,stroke-width:4px;
    style D fill:#f9f,stroke:#333,stroke-width:4px;
```

下面的文件结构仅供参考

```text
Our_Program/
├── Program_CrossSection.py
├── Prospino_Input/
│   └── ProspinoIn_1.txt
├── Cross_Section/
│   └── Prospino2_*/
│      └── prospino_2.run
├── Prospino_Run/
│   ├── Pro2_subroutines/
│   ├── prospino.in.les_houches
│   └── prospino.dat
├── Results/
│   └── CrossSection.csv
└── slhaReaderOutput.csv
```

## 2023/09/18

更新流程图，设定新的目标，**浅绿色方框** 中的内容为新的目标

```mermaid
graph TB
    A[读取数据, 计算截面] --> B[从 prospino.dat 中读取结果];
    B --> C[将数据写入一个 pd.DataFrame 表格中];
    C --> D[将表格导出成 CrossSection.csv];
    style A fill:#f9f,stroke:#333,stroke-width:4px;
    style B fill:#90EE90;
    style C fill:#90EE90;
    style D fill:#90EE90;
```

**现在的文件结构是：**

```text
Our_Program/
├── Program_CrossSection.py
├── Prospino_Input/
│   ├── ProspinoIn_1.txt
├── Prospino2/
│   ├── prospino_main.f90
│   ├── prospino.in.les_houches
│   ├── prospino.dat
│   └── prospino_2.run
├── Prospino2.tar.gz
├── CrossSection.csv
└── slhaReaderOutput.csv
```

## 2023/09/15

更新流程图，以函数功能作为其基本组成单元，使其表达的更清晰。

现在目标就是先让 Prospino 正确地运行某一个参数点的某一个截面，得出结果，但是目前先不涉及收集结果的操作。下面的每一个方框代表一个函数的功能，如果有必要也可以适当把复数功能整合进一个函数。

```mermaid
graph TB
    A[读取 slhaReaderOutput.csv] --> B[根据 Index 找到对应输入文件 ProspinoIn_Index.txt];
    B-->C[以 Index=1 为例, 把 ProspinoIn_1.txt 转换为 prospino.in.les_houches];
    C-->D[运行 prospino_2.run 适当打印结果];
```

同时更新的还有一个名字暂定为 `Our_Program` 的文件夹，相关的文件结构都已经配置好，Prospino2 也已经安装好，并编译为计算 $\tilde{\chi}_1^- \bar{\tilde{\chi}}_1^+$ 截面，因此只需要完成流程图内程序的编写，完成测试即可。

流程图中提到的功能可以参考 `Test_Point/Reference/cs_smodels_nmssm_staustau.py` 文件中第 13 行，第 31 或 39 行，以及第 47 行的函数中的某些写法。

**现在的文件结构是：**

```text
Our_Program/
├── Program_CrossSection.py
├── Prospino_Input/
│   ├── ProspinoIn_1.txt
├── Prospino2/
│   ├── prospino_main.f90
│   ├── prospino.in.les_houches
│   ├── prospino.dat
│   └── prospino_2.run
├── Prospino2.tar.gz
└── slhaReaderOutput.csv
```

## 2023/09/08

目前要实现使用 `Prospino` 执行单进程计算单个样本单个截面的功能

现在假定：

- 包含所有样本数据的 `slhareaderOutput.csv` 文件已经存在。
- 所有要计算截面的参数点的标准输入谱 `ProspinoIn_*.txt` 已经存在，并且存放在 `Prospino_Input` 文件夹里，暂时先只考虑一个参数点 `ProspinoIn_1.txt` 的情况。
- `Prospino2` 程序安装完毕。

`Prospino` 程序中有四个比较重要的文件要用到：

- 配置文件 prospino_main.f90
- 输入文件 prospino.in.les_houches
- 执行文件 prospino_2.run
- 结果文件 prospino.dat

`prospino_main.f90` 修改后需要重新编译，现在先设定好任一截面，提前编译好。

### 文件结构

```text
Our_Program/
├── Program_CrossSection.py
├── Prospino_Input/
│   ├── ProspinoIn_1.txt
├── Prospino2/
│   ├── prospino_main.f90
│   ├── prospino.in.les_houches
│   ├── prospino.dat
│   └── prospino_2.run
└── slhaReaderOutput.csv
```

### Program_CrossSection.py 流程图

```mermaid
graph TB
    A[读取 slhaReaderOutput.csv] -->|根据 Index 找到对应输入文件 ProspinoIn_1.txt| B[把 ProspinoIn_1.txt 转换为 prospino.in.les_houches];
    B-->C[运行 prospino_2.run 适当打印结果];
    C-->D[读取 prospino.dat 里的数值结果];
    D-->E[把数值结果存入表格 cross_section 里];
    E-->F[把 cross_section 输出为一个 csv 文件];
```
