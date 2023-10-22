#定义PyPivot类
class PyPivot:
    def __init__(self):
        self.dataset = {}
        self.rows = 0
        self.pivot_fields = {
            'Columns': [],
            'Rows': [],
            'Values': {}
        }#初始化一些关键变量


    def initialise_dataset(self):
        if self.dataset:
            confirm = input("已存在数据集。确认重新初始化吗? (yes/no) ")
            if confirm.lower() != "yes":
                return
        self.dataset = {}
        self.rows = 0
        print("数据集已初始化。")

    def load_test_dataset(self):
        try:
            with open("pypivot.csv", "r") as file:
                lines = file.readlines()
                headers = lines[0].strip().split(",")
                for header in headers:
                    self.dataset[header] = []
                for line in lines[1:]:
                    values = line.strip().split(",")
                    for i, header in enumerate(headers):
                        self.dataset[header].append(values[i])
                self.rows = len(lines) - 1
                print("数据集已加载。")
        except FileNotFoundError:
            print("找不到pypivot.csv文件。")

    def add_column(self):
        attribute_name = input("请输入新列的名称: ")
        if attribute_name in self.dataset:
            print("该名称已存在。")
            return
        self.dataset[attribute_name] = []
        default_value = ""
        if self.rows > 0:
            default_value = input(f"请输入新列 {attribute_name} 的默认值: ")
            self.dataset[attribute_name] = [default_value] * self.rows
        print(f"{attribute_name} 列已添加。")

    def delete_column(self):
        attribute_name = input("请输入要删除的列名称: ")
        if attribute_name not in self.dataset:
            print("该列不存在。")
            return
        del self.dataset[attribute_name]
        print(f"{attribute_name} 列已删除。")

    def add_row(self):
        if not self.dataset:
            print("错误：数据集中至少应有一列。")
            return
        for column in self.dataset:
            value = input(f"输入 {column} 的值: ")
            self.dataset[column].append(value)
        self.rows += 1
        print("行已添加。")

    def delete_row(self):
        try:
            row_id = int(input("输入要删除的行号: "))
            if row_id > self.rows or row_id <= 0:
                print("该行不存在。")
                return
            for column in self.dataset:
                del self.dataset[column][row_id - 1]
            self.rows -= 1
            print("行已删除。")
        except ValueError:
            print("请输入有效的行号。")
            
    def add_pivot_table_field(self):
        attribute_name = input("请输入属性名称: ")
        if attribute_name not in self.dataset:
            print("该属性不存在。")
            return
        field_type = input("请输入字段类型 (Columns/Rows/Values): ")
        if field_type not in self.pivot_fields:
            print("无效的字段类型。")
            return
        if attribute_name in self.pivot_fields[field_type]:
            print("该属性已作为数据透视表字段添加。")
            return
    
        if field_type == "Values":
            aggregation = input("选择聚合函数 (Count/Sum/Average/Minimum/Maximum): ")
            if aggregation not in ["Count", "Sum", "Average", "Minimum", "Maximum"]:
                print("无效的聚合函数。")
                return
            self.pivot_fields['Values'][attribute_name] = aggregation
        else:
            self.pivot_fields[field_type].append(attribute_name)
        print(f"{attribute_name} 已作为 {field_type} 类型的数据透视表字段添加。")
        
    def delete_pivot_table_field(self):
        attribute_name = input("请输入要删除的属性名称: ")
        found = False
        for key, value in self.pivot_fields.items():
            if isinstance(value, list) and attribute_name in value:
                value.remove(attribute_name)
                found = True
            elif isinstance(value, dict) and attribute_name in value:
                del value[attribute_name]
                found = True
        if not found:
            print("该属性未作为数据透视表字段添加。")
        else:
            print(f"{attribute_name} 已从数据透视表字段中删除。")

    def view_pivot_table_fields(self):
        print("\nColumns:")
        for col in self.pivot_fields['Columns']:
            print(f"• {col}")
        print("\nRows:")
        for row in self.pivot_fields['Rows']:
            print(f"• {row}")
        print("\nValues:")
        for attr, func in self.pivot_fields['Values'].items():
            print(f"• {attr} – {func}")

    def generate_pivot_table(self):
            # 首先确保数据集存在
            if not self.dataset:
                print("请先加载数据集.")
                return
            
            # 初始化透视表
            pivot_table = {}
            
            for row_id in range(self.rows):
                row_key = "-".join([self.dataset[field][row_id] for field in self.pivot_fields['Rows']])
                
                col_key = "-".join([self.dataset[field][row_id] for field in self.pivot_fields['Columns']])
                
                if row_key not in pivot_table:
                    pivot_table[row_key] = {}
                
                for attr, func in self.pivot_fields['Values'].items():
                    if col_key not in pivot_table[row_key]:
                        if func == "Count":
                            pivot_table[row_key][col_key] = 1
                        elif func == "Sum":
                            pivot_table[row_key][col_key] = int(self.dataset[attr][row_id])
                        elif func == "Average":
                            pivot_table[row_key][col_key] = [int(self.dataset[attr][row_id]), 1]
                        # 您可以继续为其他函数添加实现...
                    else:
                        if func == "Count":
                            pivot_table[row_key][col_key] += 1
                        elif func == "Sum":
                            pivot_table[row_key][col_key] += int(self.dataset[attr][row_id])
                        elif func == "Average":
                            pivot_table[row_key][col_key][0] += int(self.dataset[attr][row_id])
                            pivot_table[row_key][col_key][1] += 1
                        # 您可以继续为其他函数添加实现...
    
            # 如果是平均值，我们需要除以总数来得到真正的平均值
            for row_key, columns in pivot_table.items():
                for col_key, value in columns.items():
                    if isinstance(value, list):  # 这意味着它是一个平均值
                        pivot_table[row_key][col_key] = value[0] / value[1]
            
            # 打印透视表
            print("\t", end="")
            for col_key in set([col for _, columns in pivot_table.items() for col in columns]):
                print(col_key, end="\t")
            print()
            for row_key, columns in pivot_table.items():
                print(row_key, end="\t")
                for col_key in set([col for _, columns in pivot_table.items() for col in columns]):
                    print(columns.get(col_key, ""), end="\t")
                print()

    def print_pivot_table_with_summary(self):
            # 首先确保数据集存在
            if not self.dataset:
                print("请先加载数据集.")
                return
            
            # 初始化透视表
            pivot_table = {}
            
            for row_id in range(self.rows):
                row_key = "-".join([self.dataset[field][row_id] for field in self.pivot_fields['Rows']])
                
                col_key = "-".join([self.dataset[field][row_id] for field in self.pivot_fields['Columns']])
                
                if row_key not in pivot_table:
                    pivot_table[row_key] = {}
                
                for attr, func in self.pivot_fields['Values'].items():
                    if col_key not in pivot_table[row_key]:
                        if func == "Count":
                            pivot_table[row_key][col_key] = 1
                        elif func == "Sum":
                            pivot_table[row_key][col_key] = int(self.dataset[attr][row_id])
                        elif func == "Average":
                            pivot_table[row_key][col_key] = [int(self.dataset[attr][row_id]), 1]
                        # 您可以继续为其他函数添加实现...
                    else:
                        if func == "Count":
                            pivot_table[row_key][col_key] += 1
                        elif func == "Sum":
                            pivot_table[row_key][col_key] += int(self.dataset[attr][row_id])
                        elif func == "Average":
                            pivot_table[row_key][col_key][0] += int(self.dataset[attr][row_id])
                            pivot_table[row_key][col_key][1] += 1
                        # 您可以继续为其他函数添加实现...
    
            # 如果是平均值，我们需要除以总数来得到真正的平均值
            for row_key, columns in pivot_table.items():
                for col_key, value in columns.items():
                    if isinstance(value, list):  # 这意味着它是一个平均值
                        pivot_table[row_key][col_key] = value[0] / value[1]
            
                row_summaries = {}
                grand_total = 0
            
            # 计算每个cell的值
            for row_key, columns in pivot_table.items():
                for col_key, value in columns.items():
                    if isinstance(value, list):  # 如果是一个平均值
                        pivot_table[row_key][col_key] = value[0] / value[1]
            
            row_summaries = {}
            grand_total = 0
            
            for row_key, columns in pivot_table.items():
                row_total = 0
                for col_key, value in columns.items():
                    if isinstance(value, list):
                        cell_value = value[0] / value[1]
                    else:
                        cell_value = value
                    row_total += cell_value
            
                    if col_key not in row_summaries:  # 初始化列总计
                        row_summaries[col_key] = 0
                    row_summaries[col_key] += cell_value  # 累加到列总计
            
                columns["Row Total"] = row_total  # 将行总计添加到当前行
                grand_total += row_total  # 累加到总总计
            
            # 添加列总计和总总计到pivot_table中
            pivot_table["Column Total"] = row_summaries
            pivot_table["Column Total"]["Grand Total"] = grand_total
            
            # 首先提取所有的列名，并确保它们的顺序
            all_column_keys = []
            for _, columns in pivot_table.items():
                for col_key in columns:
                    if col_key not in all_column_keys:
                        all_column_keys.append(col_key)
            
            # 输出列名
            print("\t", end="")
            for col_key in all_column_keys:
                print(col_key, end="\t")
            print()
            
            # 输出Pivot Table的内容
            for row_key, columns in pivot_table.items():
                print(row_key, end="\t")
                for col_key in all_column_keys:
                    print(columns.get(col_key, ""), end="\t")
                print()

            

        
def main():
    pp = PyPivot()
    while True:
        print("\n1. 初始化数据集")
        print("2. 加载测试数据集")
        print("3. 添加列")
        print("4. 删除列")
        print("5. 添加行")
        print("6. 删除行")
        print("7. 添加数据透视表字段")
        print("8. 删除数据透视表字段")
        print("9. 查看现有数据透视表字段")
        print("10. 生成透视表")
        print("11.生成透视表聚合值")
        print("12. 退出")
        choice = input("选择操作: ")
        if choice == "1":
            pp.initialise_dataset()
        elif choice == "2":
            pp.load_test_dataset()
        elif choice == "3":
            pp.add_column()
        elif choice == "4":
            pp.delete_column()
        elif choice == "5":
            pp.add_row()
        elif choice == "6":
            pp.delete_row()
        elif choice == "7":
            pp.add_pivot_table_field()
        elif choice == "8":
            pp.delete_pivot_table_field()
        elif choice == "9":
            pp.view_pivot_table_fields()
        elif choice == "10":
            pp.generate_pivot_table()
        elif choice == "11":
            pp.print_pivot_table_with_summary()
        elif choice == "12":
            break
        else:
            print("无效的选择。")

if __name__ == "__main__":
    main()
