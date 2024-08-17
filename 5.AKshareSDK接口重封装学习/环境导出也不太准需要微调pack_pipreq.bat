chcp 65001 % 解决命令行中文输出乱码的问题%
echo 使用 [pipreqs] 模块代替 [pip freeze] 命令

%pip install pipreqs%

C:\Users\opink\miniconda3\envs\python3.9\Scripts\pipreqs.exe ./ --encoding=utf8 --force

echo 查看 [bat] 脚本同级的 ./requirements.txt 文件
pause