students = []
for i in range(5):
    name = input(f"請輸入第{i+1}位學生的姓名: ")
    math = float(input(f"請輸入{name}的數學成績: "))
    english = float(input(f"請輸入{name}的英文成績: "))
    physics = float(input(f"請輸入{name}的物理成績: "))
    average = (math + english + physics) / 3
    students.append([name, math, english, physics, average])

# Output in tabular format
print("姓名      數學    英文    物理    平均")
print("========================================")
for student in students:
    print(f"{student[0]:<10} {student[1]:<7} {student[2]:<7} {student[3]:<7} {student[4]:.1f}")