# Work Flow

## 2023/11/08

```mermaid
graph TB
    A[为所有进程的 MadEvent 文件夹产生指定的 SL 过程] --> B[读取数据];
    B --> |从第一个参数点开始| C[判断 Siglino 类型];
    C --> D[产生相应的 ElectroWeakino 过程];
    D --> E[为 EW 过程的 MadEvent 替换必要的 Card,<br/>运行 EW 过程的 MadEvent];
    E --> F[替换 EW 过程 CheckMATE 输入文件的 EW 截面,<br/>运行 EW 过程 CheckMATE,<br/>删除 EW 过程的事例结果];
    F --> G[删除 SL 过程的 MadEvent 中的特定文件,<br/>为 SL 过程的 MadEvent 替换必要的 Card,<br/>运行 SL 过程的 MadEvent];
    G --> H[替换 SL 过程 CheckMATE 输入文件的 SL 截面,<br/>运行 SL 过程 CheckMATE,<br/>删除 SL 过程的事例结果];
    H --> I[收集该参数点总的 CheckMATE 结果到 csv];
    I --> J{删除 CheckMATE 结果};
    J --> |模拟下一个参数点|C;
    J --> |所有参数点模拟完毕|K[进行最后的数据整理];
    style A fill:#f9f,stroke:#333,stroke-width:4px;
    style B fill:#f9f,stroke:#333,stroke-width:4px;
    style C fill:#f9f,stroke:#333,stroke-width:4px;
    style D fill:#f9f,stroke:#333,stroke-width:4px;
    style E fill:#f9f,stroke:#333,stroke-width:4px;
    style F fill:#f9f,stroke:#333,stroke-width:4px;
    style G fill:#f9f,stroke:#333,stroke-width:4px;
    style H fill:#f9f,stroke:#333,stroke-width:4px;
    style I fill:#f9f,stroke:#333,stroke-width:4px;
    style J fill:#f9f,stroke:#333,stroke-width:4px;
    style K fill:#f9f,stroke:#333,stroke-width:4px;
```

## 2023/10/29

```mermaid
graph TB
    A[读取数据] --> |从第一个参数点开始|B[判断 Siglino 类型];
    B -->|计算相应情况的 ElectroWeakino 截面| C[计算截面];
    C -->|某些 Siglino 类型个别截面不计算, 指定为 0| D{收集结果};
    D -->|如果参数点的截面没有全部计算完, 继续计算| C;
    D -->|如果参数点的截面全部计算完毕| E{导出结果到 CSV};
    E --> |计算下一个参数点的截面|B;
    E --> |所有参数点截面计算完毕|F[将所有截面信息写入 SModelS 输入文件];
    F --> G[多核运行 SModelS];
    G --> H[收集全部 SModelS py 结果];
    H --> I[筛选 r < 1 的结果生成下一阶段需要的输入数据]
    style A fill:#90EE90;
    style B fill:#90EE90;
    style C fill:#90EE90;
    style D fill:#90EE90;
    style E fill:#90EE90;
    style F fill:#f9f,stroke:#333,stroke-width:4px;
    style G fill:#f9f,stroke:#333,stroke-width:4px;
    style H fill:#f9f,stroke:#333,stroke-width:4px;
    style I fill:#f9f,stroke:#333,stroke-width:4px;
```

## 2023/10/20

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

**流程图**：

```mermaid
graph TB
    A[读取数据] --> B[判断 Siglino 类型];
    B -->|计算相应情况的 ElectroWeakino 截面| C[计算截面];
    C -->|某些 Siglino 类型个别截面不计算，指定为 0| D[收集结果];
    D -->|循环足够的次数把相应截面全都计算完| B;
    style A fill:#f9f,stroke:#333,stroke-width:4px;
    style B fill:#90EE90;
    style C fill:#f9f,stroke:#333,stroke-width:4px;
    style D fill:#f9f,stro
```

**文件结构**：

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

**流程图**：

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

**文件结构**：

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

**流程图**：

```mermaid
graph TB
    A[读取 slhaReaderOutput.csv] --> B[根据 Index 找到对应输入文件 ProspinoIn_Index.txt];
    B-->C[以 Index=1 为例, 把 ProspinoIn_1.txt 转换为 prospino.in.les_houches];
    C-->D[运行 prospino_2.run 适当打印结果];
```

**文件结构**：

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

**文件结构**：

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

**Program_CrossSection.py 流程图**：

```mermaid
graph TB
    A[读取 slhaReaderOutput.csv] -->|根据 Index 找到对应输入文件 ProspinoIn_1.txt| B[把 ProspinoIn_1.txt 转换为 prospino.in.les_houches];
    B-->C[运行 prospino_2.run 适当打印结果];
    C-->D[读取 prospino.dat 里的数值结果];
    D-->E[把数值结果存入表格 cross_section 里];
    E-->F[把 cross_section 输出为一个 csv 文件];
```
