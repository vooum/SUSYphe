####################################################################
#    PROGRAM 3: calculate cross sections(multi point)              #
#    BY: Pole                                                      #
#    2023/09/15                                                    #
####################################################################

import os, shutil, subprocess
source_folder = "/home/bzy/Prospino_Input"
target_folder = "/home/bzy/Prospino_total/Prospino2"
result_file = "/home/bzy/Prospino_Input/results.txt"
with open(result_file, 'r+') as f:
    f.truncate(0)
    result = f.read()
    #print("result file content:", result)
    for filename in os.listdir(source_folder):#如果文件名以’prospino_‘开头，并以’.in.les_houches’结尾，说明是要处理的文件
         if filename.startswith('prospino_') and filename.endswith('.in.les_houches'):
                new_filename = filename.replace('prospino_', 'prospino.')# 生成一个新的文件名，将’prospino_‘替换为’prospino.’，并赋值给new_filename变量 
                new_filepath = os.path.join(target_folder, new_filename)# 生成一个旧的文件路径，由源文件夹和旧文件名组成，并赋值给old_filepath变量
                old_filepath = os.path.join(source_folder, filename)
                print("copying file:", old_filepath, "to", new_filepath)
                shutil.copyfile(old_filepath, new_filepath)
                new_prospino_filepath = os.path.join(target_folder, "prospino.in.les_houches")
                print("renaming file:", new_filepath, "to", new_prospino_filepath)
                os.rename(new_filepath, new_prospino_filepath)
                print("running subprocess:", './prospino_2.run')
                try:
                    subprocess.run([ './prospino_2.run'],cwd=target_folder, check=True)
                except subprocess.TimeoutExpired:
                    print("The external program timed out")
                with open(os.path.join(target_folder, 'prospino.dat'), 'r') as f: 
                    output = f.read()
                    last_number = output.split("\n")[0].split()[-1]# 使用split()方法将第一行按空格分割成列表，然后取最后一个元素
                    print("last_number:", last_number)
                    result += last_number + '\n'
                    #print("removing file:", new_filepath)
                    #os.remove(new_filepath)# 删除新文件，以便下一次复制和重命名
                    
                with open(result_file, 'w') as f: 
                    print("writing result to file:", result_file)
                    f.write(result)#打开结果文件，并将result变量写入其中，然后关闭文件
                        

