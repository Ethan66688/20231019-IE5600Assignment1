#定义PyPivot类
#Define the class “PyPivot”
class PyPivot:
    
    #初始化一些关键变量dataset、rows、values、pivot_fields
    #Initialize some key variables like dataset, rows, values, pivot_fields,etc
    def __init__(self):
        self.dataset = {}
        self.rows = 0
        self.pivot_fields = {
            'Columns': [],
            'Rows': [],
            'Values': {}
        }

    #实现New Dataset功能，初始化Pypivot为空文件，如果已存在文件，要提醒用户是否需要重新初始化（Usecase1）
    # Implement the New Dataset function to initialize Pypivot as an empty file. If the file already exists, remind the user whether it needs to be re-initialized(Usecase1)
    def initialise_dataset(self):
        if self.dataset:
            confirm = input("已存在数据集。确认重新初始化吗?An existing data set. Are you sure to reinitialize? (yes/no) ")
            if confirm.lower() != "yes":
                return
        self.dataset = {}
        self.rows = 0
        print("数据集已初始化。The dataset has been initialized.")

    #加载测试数据，将其自动填充到dataset中（Usecase2）
    # Load test data and automatically populate it into the dataset (Usecase2)
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
                print("数据集已加载。The dataset has been loaded successfully!:)")
        except FileNotFoundError:
            print("找不到pypivot.csv文件。There is no pypivot.csv!")
            
    #提示用户添加列（Usecase3）
    # Prompt user to add column (Usecase3)
    def add_column(self):
        attribute_name = input("请输入新列的名称Please enter a name for the new column: ")
        if attribute_name in self.dataset:
            print("该名称已存在。Opps，the name already exists.")
            return
        self.dataset[attribute_name] = []
        default_value = ""
        if self.rows > 0:
            default_value = input(f"请输入新列 {attribute_name} 的默认值Enter the default value for the new column: ")
            self.dataset[attribute_name] = [default_value] * self.rows
        print(f"{attribute_name} 列已添加。The column has been added successfully!:)")

    #提示用户删除列（Usecase4）
    # Prompt user to delete column (Usecase4)
    def delete_column(self):
        attribute_name = input("请输入要删除的列名称Please enter the column name you want to delete: ")
        if attribute_name not in self.dataset:
            print("该列不存在。Opps, there is no such a column")
            return
        del self.dataset[attribute_name]
        print(f"{attribute_name} 列已删除。The column has been deleted!")

    #提示用户添加行（Usecase5）
    #Prompt user to add a new row(UseCase5)
    def add_row(self):
        if not self.dataset:
            print("错误：数据集中至少应有一列。Error: There should be at least one column in the dataset.")
            return
        for column in self.dataset:
            value = input(f"输入 {column} 的值Enter the value for the column: ")
            self.dataset[column].append(value)
        self.rows += 1
        print("行已添加。The row has been added successfully!:)")

    #提示用户删除行（Usecase6）
    #Prompt user to delete a row(UseCase6)
    def delete_row(self):
        try:
            row_id = int(input("输入要删除的行号Please enter the row identifier you want to delete: "))
            if row_id > self.rows or row_id <= 0:
                print("该行不存在。")
                return
            for column in self.dataset:
                del self.dataset[column][row_id - 1]
            self.rows -= 1
            print("行已删除The row has been deleted。")
        except ValueError:
            print("请输入有效的行号Please enter a valid row identifier。")

    #添加透视表区域（Usecase7）
    #Prompt user to add a pivot table field(UseCase7)
    def add_pivot_table_field(self):
        attribute_name = input("请输入属性名称Please enter the attribute name: ")
        if attribute_name not in self.dataset:
            print("该属性不存在。There is no such an attribute in the dataset!")
            return
        field_type = input("请输入字段类型Please choose the type of the field (Columns/Rows/Values): ")
        if field_type not in self.pivot_fields:
            print("无效的字段类型，请注意区分大小写。The type is not valid，please be case sensitive)")
            return
        if attribute_name in self.pivot_fields[field_type]:
            print("该属性已作为数据透视表字段添加。This attribute has already been added as a PivotTable field.")
            return
    
        if field_type == "Values":
            aggregation = input("选择聚合函数Please choose the aggregation you want to use (Count/Sum/Average/Minimum/Maximum): ")
            if aggregation not in ["Count", "Sum", "Average", "Minimum", "Maximum"]:
                print("无效的聚合函数。The function is not valid!")
                return
            self.pivot_fields['Values'][attribute_name] = aggregation
        else:
            self.pivot_fields[field_type].append(attribute_name)
        print(f"{attribute_name} 已作为 {field_type} 类型的数据透视表字段添加。{attribute_name} has been added as a pivot table field of type {field_type}.")

    #删除透视表区域（UseCase8）
    #Prompt user to delete a pivot table field(Usecase8)
    def delete_pivot_table_field(self):
        attribute_name = input("请输入要删除的属性名称Please enter the attribute name you want to delete: ")
        found = False
        for key, value in self.pivot_fields.items():
            if isinstance(value, list) and attribute_name in value:
                value.remove(attribute_name)
                found = True
            elif isinstance(value, dict) and attribute_name in value:
                del value[attribute_name]
                found = True
        if not found:
            print("该属性未作为数据透视表字段添加。This attribute has not been added as a PivotTable field!")
        else:
            print(f"{attribute_name} 已从数据透视表字段中删除。{attribute_name} has been deleted from the pivot table fields.")

    #查看当前透视表区域（UseCase9）
    #View Current pivot table fields（UseCase9）
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

    #生成透视表（UseCase10）
    #Generate the pivot table（UseCase10）
    def generate_pivot_table(self):
            # 首先确保数据集存在
            # Firstly, make sure the data set exists
            if not self.dataset:
                print("请先加载数据集。Please load a dataset first.")
                return
            
            # 初始化透视表
            # initialize the pivot table
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
                        elif func == "Minimum":
                            pivot_table[row_key][col_key] = int(self.dataset[attr][row_id])
                        elif func == "Maximum":
                            pivot_table[row_key][col_key] = int(self.dataset[attr][row_id])
                    else:
                        if func == "Count":
                            pivot_table[row_key][col_key] += 1
                        elif func == "Sum":
                            pivot_table[row_key][col_key] += int(self.dataset[attr][row_id])
                        elif func == "Average":
                            pivot_table[row_key][col_key][0] += int(self.dataset[attr][row_id])
                            pivot_table[row_key][col_key][1] += 1
                        elif func == "Minimum":
                            if pivot_table[row_key][col_key] > int(self.dataset[attr][row_id]):
                              pivot_table[row_key][col_key] = int(self.dataset[attr][row_id])
                        elif func == "Maximum":
                            if pivot_table[row_key][col_key] < int(self.dataset[attr][row_id]):
                              pivot_table[row_key][col_key] = int(self.dataset[attr][row_id])
                            
    
            # 如果是平均值，我们需要除以总数来得到真正的平均值
            # If it is the average, we need to divide by the total to get the true average
            for row_key, columns in pivot_table.items():
                for col_key, value in columns.items():
                    if isinstance(value, list):  # 这意味着它是一个平均值This means it is the average.
                        pivot_table[row_key][col_key] = value[0] / value[1]
            
            # 打印透视表Print the pivot table
            print("\t", end="")
            for col_key in set([col for _, columns in pivot_table.items() for col in columns]):
                print(col_key, end="\t")
            print()
            for row_key, columns in pivot_table.items():
                print(row_key, end="\t")
                for col_key in set([col for _, columns in pivot_table.items() for col in columns]):
                    print(columns.get(col_key, ""), end="\t")
                print()

    #生成透视表的汇总数据（UseCase11）
    #print the pivot table with summary（UseCase11）
    def print_pivot_table_with_summary(self):
            # 首先确保数据集存在
            # Firstly, make sure the data set exists
            if not self.dataset:
                print("请先加载数据集.Please load a dataset first.")
                return
            
            # 初始化透视表
            # initialize the pivot table
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
                        elif func == "Minimum":
                            pivot_table[row_key][col_key] = int(self.dataset[attr][row_id])
                        elif func == "Maximum":
                            pivot_table[row_key][col_key] = int(self.dataset[attr][row_id])
                    else:
                        if func == "Count":
                            pivot_table[row_key][col_key] += 1
                        elif func == "Sum":
                            pivot_table[row_key][col_key] += int(self.dataset[attr][row_id])
                        elif func == "Average":
                            pivot_table[row_key][col_key][0] += int(self.dataset[attr][row_id])
                            pivot_table[row_key][col_key][1] += 1
                        elif func == "Minimum":
                            if pivot_table[row_key][col_key] > int(self.dataset[attr][row_id]):
                              pivot_table[row_key][col_key] = int(self.dataset[attr][row_id])
                        elif func == "Maximum":
                            if pivot_table[row_key][col_key] < int(self.dataset[attr][row_id]):
                              pivot_table[row_key][col_key] = int(self.dataset[attr][row_id])
    
            # 如果是平均值，我们需要除以总数来得到真正的平均值
            # If it is the average, we need to divide by the total to get the true average
            for row_key, columns in pivot_table.items():
                for col_key, value in columns.items():
                    if isinstance(value, list):  # 这意味着它是一个平均值This means it is the average.
                        pivot_table[row_key][col_key] = value[0] / value[1]
            
                row_summaries = {}
                grand_total = 0
            
            # 计算每个cell的值Calculate the value of each cell
            for row_key, columns in pivot_table.items():
                for col_key, value in columns.items():
                    if isinstance(value, list):  # 如果是一个平均值If it is a average value
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
            
                    if col_key not in row_summaries:  # 初始化列总计initialize the summary of the rows
                        row_summaries[col_key] = 0
                    row_summaries[col_key] += cell_value 
            
                columns["Row Total"] = row_total  
                grand_total += row_total  
            
            # 添加列总计和总总计到pivot_table中
            # Add column totals and totals to pivot_table
            pivot_table["Column Total"] = row_summaries
            pivot_table["Column Total"]["Grand Total"] = grand_total
            
            # 首先提取所有的列名，并确保它们的顺序
            # First extract all column names and make sure they are in order
            all_column_keys = []
            for _, columns in pivot_table.items():
                for col_key in columns:
                    if col_key not in all_column_keys:
                        all_column_keys.append(col_key)
            
            # 输出列名
            #Output the columns
            print("\t", end="")
            for col_key in all_column_keys:
                print(col_key, end="\t")
            print()
            
            # 输出Pivot Table的内容
            #Output the Pivot Table
            for row_key, columns in pivot_table.items():
                print(row_key, end="\t")
                for col_key in all_column_keys:
                    print(columns.get(col_key, ""), end="\t")
                print()

#下面则是主程序入口，依次提示了用户可以选择的操作
#The following is the main program entry, which in turn prompts the user to select operations
def main():
    pp = PyPivot()
    while True:
        print("\n1. 初始化数据集 Initialize the dataset")
        print("2. 加载测试数据集 Load the test dataset")
        print("3. 添加列 add a column")
        print("4. 删除列 delete a column")
        print("5. 添加行 add a row")
        print("6. 删除行 delete a row")
        print("7. 添加数据透视表字段 add a pivot table field")
        print("8. 删除数据透视表字段 delete a pivot table field")
        print("9. 查看现有数据透视表字段 view current pivot table fields")
        print("10. 生成透视表 generate the pivot table")
        print("11.生成透视表聚合值 generate the pivot table with grouped summary")
        print("12. 退出 exit")
        choice = input("选择操作Please choose your operation: ")
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
            print("无效的选择。Invalid choice.")

if __name__ == "__main__":
    main()
