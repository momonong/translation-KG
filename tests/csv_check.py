with open("data/conceptnet.csv", "r", encoding="utf-8") as f:
    for i in range(5):  # 顯示前 5 行
        line = f.readline()
        print(f"Line {i+1}: {line.strip()}")
