import blessed

term = blessed.Terminal()

print("解码 ===")
print()
print("模式：1-输入式（键盘单行输入） 2-文件式（从文件读取）")
mods = None
while not mods in ["1","2"]:
    mods = input("请输入 1 或 2：").strip()
    if not mods in ["1","2"]:
        print("无效选择")

content = None
if mods == "1":
    content = input("请输入一段文本（单行，回车结束）：")
else:
    path = input("请输入文件路径：").strip()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"文件 {path} 不存在")
        exit(1)

# print(content)

# i in [0xE0100, 0xE01FF] -> encoded
print()
print("检测中:")

def is_hidden(ch: str):
    return 0xE0100 <= ord(ch) and ord(ch) <= 0xE01FF

phase = []
# content+=" "
l = len(content)
for i in range(0,l):
    # 第一个字符不可能是加密字符
    ch = content[i]
    if (is_hidden(ch)):
        if (is_hidden(content[i-1])):
            phase[-1].append(ord(ch))
        else:
            phase.append([ord(ch)])
        continue
    # 不是第一个 且 前面是加密字符
    if (i != 0 and is_hidden(content[i-1])):
        print(term.yellow_on_red(ch),end="")
        continue
    # 不是最后一个 且 后面是加密字符
    if (i != l-1 and is_hidden(content[i+1])):
        print(term.yellow_on_red(ch+f"({len(phase)+1})"),end="")
        continue
    # 啥都不是
    print(term.yellow(ch),end="")

print()
print()
# print(phase)
# print([[format(j, '04X') for j in i] for i in phase])
print("解码结果:")

for i in range(len(phase)):
    # ori: U+10FFFF
    # sec: [0xE0100, 0xE01FF, 0xE01FF]
    # sec - 0xE0100 -> [0, 0xFF, 0xFF]
    # [0, 0xFF, 0xFF] => 0x00 FF FF => a*0x10000 + b*0x100 + c
    print(f"第 {i+1} 段密文:")
    sec = phase[i]
    if ((len(sec) % 3) != 0):
        print(term.red("密文损坏"))
        print("密文 UniCode:", sec)
        continue

    sec = [(i-0xE0100) for i in sec]
    ori = [
        chr(sec[i]*0x10000 + sec[i+1]*0x100 + sec[i+2])
        for i in range(0, len(sec), 3)
    ]
    print((term.white_on_green) + term.bold("".join(ori)))
