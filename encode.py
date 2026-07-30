# import pyperclip

print("编码 ===")
print("模式：1-输入式（单行输入） 2-文件式（从文件读取）")
mod = None
while not mod in ["1", "2"]:
    mod = input("请输入 1 或 2：")
    if (not mod in ["1", "2"]):
        print("无效选择")

# print(mod)
print()

content = None
if mod == "1":
    content = input("请输入一段文本（单行，回车结束）：")
else:
    path = input("请输入文件路径：").strip()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"文件 {path} 不存在")
        exit(1)

print()

print("最终输出的格式为(没有空格) `{载体}{隐写数据}/`")
carrier = input("请输入载体文本（单行，回车结束）：")

# max U+10FFFF
# each content => 0xE0100 - 0xE01FF (255)
# each byte => 2 hex chars
# 10FFFF => 10, FF, FF => 0xE0110 0xE01FF 0xE01FF

uni = [ord(ch) for ch in content]
sec = []
for i in uni:
    # i = 10ffff => 10,ff,ff
    a,b,c = None,None,None
    c = int(i % 0x100)
    i //= 0x100
    b = int(i % 0x100)
    i //= 0x100
    a = int(i % 0x100)
    # print("%02X %02X %02X" % (a, b, c))

    sec.append(chr(0xE0100+a))
    sec.append(chr(0xE0100+b))
    sec.append(chr(0xE0100+c))

print("输出:")
print("\033[31m" + carrier + ''.join(sec) + "/\033[0m")
