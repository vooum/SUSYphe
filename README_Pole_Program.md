
### recPoints.csv是原始的扫描结果文件。

### Data_Extract.py是从recPoints.csv提取出需要的部分数据的程序，这些提取出的数据将以行（hang）为单位替换到prospino输入谱文件的对应位置。
### extracted.csv是Data_Extract.py的输出文件。

### test2.csv是将extracted.csv取头十行的文件。extracted.csv数据量较大，取头十行方便接下来的测试。

### Parameter_Write.py的作用是将test2.csv以行（hang）为单位分别替换prospino输入谱文件，并将新文件分别写入一个指定文件夹Prospino_Input中保存。用于替换到模板谱文件prospinoIn_1.txt也放在了Prospino_Input中。Parameter_Write.py要调prospinoIn_1.txt，需要用test2.csv数据替换的地方使用了"Pole_..."标记。

### Prospino_Input保存了Parameter_Write.py的所有输出文件，里面的文件用于粘贴到Prospino中计算截面。

### Program_CrossSection_multipoint.py的作用是先把Prospino_Input中每一个结尾为.in.les_houches的文件改名为prospino.in.les_houches，粘贴到peospino目录下，然后对每一个文件粘贴后，运行./prospino_2.run，找到结果文件prospino.dat的截面，将其提取粘贴到results.txt中。results.txt记录了所有点的截面值。

### prospino_main.f90为预先设定好的文件，每份Prospino包只计算一个截面。

### 手动将results.txt改成了results.csv。

### 三个python程序运行命令分别为(忽略所在文件夹/home/bzy)：
### python Data_Extract.py
### python Parameter_Write.py
### python Program_CrossSection_multipoint.py

### 在测试中，Prospino2在目录home/bzy/Prospino_total下；results.txt，prospino_i.in.les_houches（i为不同点的变量）在目录/home/bzy/Prospino_Input下；python文件Data_Extract.py，Parameter_Write.py以及Program_CrossSection_multipoint.py在目录/home/bzy下；csv文件recPoints.csv，extracted.csv，test2.csv在目录/home/bzy下。



