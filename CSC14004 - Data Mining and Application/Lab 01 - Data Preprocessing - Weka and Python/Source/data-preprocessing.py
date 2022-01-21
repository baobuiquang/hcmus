# MSSV: 19120454
# Họ tên: Bùi Quang Bảo

# =============== Cú pháp tham số dòng lệnh =================
# Chức năng 1: python data-preprocessing.py input.csv list-cols-missing
# Chức năng 2: python data-preprocessing.py input.csv count-rows-missing
# Chức năng 3: python data-preprocessing.py input.csv fill-missing mean/median output.csv
# Chức năng 4: python data-preprocessing.py input.csv remove-rows-missing missing_limit output.csv
# Chức năng 5: python data-preprocessing.py input.csv remove-cols-missing missing_limit output.csv
# Chức năng 6: python data-preprocessing.py input.csv remove-duplicates output.csv

# ====================== Một số lưu ý =======================
# * Python version: 3.9.7
# * Ở các chức năng 3, 4, 5, 6, tham số output.csv có thể có hoặc không
#   Nếu không có thì chương trình sẽ mặc định tên file output, tuỳ thuộc vào chức năng
# * Ở chức năng 4 và 5, "tỉ lệ thiếu cho trước" phải nằm trong khoảng từ 0 tới 1,
#   Nếu vượt ra ngoài mặc định là 0 (nếu nhỏ hơn 0) hoặc 1 (nếu lớn hơn 1)

# ======== Lệnh đã được sử dụng để demo trong báo cáo ========
# python data-preprocessing.py house-prices.csv list-cols-missing
# python data-preprocessing.py house-prices.csv count-rows-missing
# python data-preprocessing.py house-prices.csv fill-missing mean fill-missing-mean.csv
# python data-preprocessing.py house-prices.csv fill-missing median fill-missing-median.csv
# python data-preprocessing.py house-prices.csv remove-rows-missing 0.1 remove-rows-missing-0.1.csv
# python data-preprocessing.py house-prices.csv remove-rows-missing 0.08 remove-rows-missing-0.08.csv
# python data-preprocessing.py house-prices.csv remove-cols-missing 0.5 remove-cols-missing-0.5.csv
# python data-preprocessing.py house-prices.csv remove-cols-missing 0.1 remove-cols-missing-0.1.csv
# python data-preprocessing.py house-prices.csv remove-duplicates remove-duplicates.csv

# Nhập thư viện
import sys # chỉ được sử dụng để đọc tham số dòng lệnh
import csv # chỉ được sử dụng để đọc/ghi tập tin csv

# Hàm kiểm tra giá trị có phải numeric hay không
def isNumeric(num):
    try:
        temp = float(num)
    except:
        return False
    return True

# Tất cả các chức năng được viết dưới dạng phương thức
class DataPreprocessing:

    # Khởi tạo, đọc file, tạo 1 dictionary lưu dữ liệu để sử dụng chung cho tất cả chức năng
    def __init__(self, input_file):
        self.input_file = input_file
        with open(input_file, 'r') as f:
            reader = csv.reader(f)
            self.data_dict = {}
            cols = []
            rows = []
            # Lưu tên thuộc tính
            cols = next(reader)
            # Lưu các dòng giá trị
            for row in reader:
                rows.append(row)
            # Chuyển từ list sang dictionary
            for i, col in enumerate(cols):
                self.data_dict[col] = []
                for row in rows:
                    self.data_dict[col].append(row[i])

    # Hàm dùng để ghi file output (sử dụng chung cho nhiều chức năng)
    def outputCSV(self, output_file):
        
        data = self.data_dict
        rows = []
        
        rows.append([col_name for col_name in data])
        
        for col in data:
            for i, value in enumerate(data[col]):
                if len(rows) <= i+1:
                    rows.append([])
                rows[i+1].append(value)
        
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            for row in rows:
                writer.writerow(row)
            print(f'Write to {output_file} successfully!')

    # ================== Chức năng 1 ==================
    # Liệt kê số cột (thuộc tính) bị thiếu dữ liệu
    def listColsMissing(self):
        cols_missing_values = []
        for col in self.data_dict:
            if '' in self.data_dict[col] and col not in cols_missing_values:
                cols_missing_values.append(col)
        print('List columns that have missing values:')
        print(cols_missing_values)

    # ================== Chức năng 2 ==================
    # Đếm số dòng (mẫu) bị thiếu dữ liệu
    def countRowsMissing(self):
        rows_missing_values = []

        for col in self.data_dict:
            for i, value in enumerate(self.data_dict[col]):
                if value == '' and i not in rows_missing_values:
                    rows_missing_values.append(i)
        
        print('Count rows that have missing values:')
        print(len(rows_missing_values))
    
    # ================== Chức năng 3 ==================
    # Điền giá trị bị thiếu
    # Đối với thuộc tính categorical:
    #     * Phương pháp mode (mặc định)
    # Đối với thuộc tính numeric:
    #     * Phương pháp mean (mặc định)
    #     * Phương pháp median
    def fillMissing(self, method = 'mean', output_file = 'fillMissing.csv'):
        for col in self.data_dict:
            # Tiến hành fill values với những cột cần thiết
            if '' in self.data_dict[col]:
                # Xác định thuộc tính là numeric hay categorical
                is_numeric = True
                for value in self.data_dict[col]:
                    if value != '' and isNumeric(value) == False:
                        is_numeric = False
                        break
                # Nếu thuộc tính là categorical
                if not is_numeric:
                    lst = [e for e in self.data_dict[col] if e != '']
                    mode = max(set(lst), key=lst.count) # Mode
                    for i, value in enumerate(self.data_dict[col]):
                        if value == '':
                            self.data_dict[col][i] = mode
                            
                # Nếu thuộc tính là numeric
                else:
                    lst = [float(e) for e in self.data_dict[col] if e != '']
                    lst = [0] if lst == [] else lst
                    
                    # Nếu theo phương pháp mean (mặc định):
                    if method == 'mean':
                        mean = sum(lst)/len(lst)
                        # print(f'mean = {mean}')
                        for i, value in enumerate(self.data_dict[col]):
                            if value == '':
                                self.data_dict[col][i] = str(mean)
                        
                    # Nếu theo phương pháp median:
                    elif method == 'median':
                        lst.sort()
                        n = len(lst)
                        if n % 2 == 0:
                            median = (lst[n//2] + lst[n//2 - 1])/2
                        else:
                            median = lst[n//2]
                        # print(f'median = {median}')
                        for i, value in enumerate(self.data_dict[col]):
                            if value == '':
                                self.data_dict[col][i] = str(median)
        self.outputCSV(output_file)
    
    # ================== Chức năng 4 ==================
    # Xóa các dòng bị thiếu dữ liệu với ngưỡng tỉ lệ thiếu cho trước
    # Quy ước: 0 <= missing_limit <= 1
    # Những dòng bị xoá là những dòng có: missing_ratio > missing_limit
    def removeRowsMissing(self, missing_limit = 1, output_file = 'removeRowsMissing.csv'):
        missing_limit = 0 if missing_limit < 0 else (1 if missing_limit > 1 else missing_limit)
        
        rows_to_remove = []
        
        # Chuyển từ dictionary qua list
        data = self.data_dict
        rows = []
        for col in data:
            for i, value in enumerate(data[col]):
                if len(rows) <= i:
                    rows.append([])
                rows[i].append(value)
        
        for i, row in enumerate(rows):
            missing_ratio = row.count('') / len(row)
            if missing_ratio > missing_limit:
                rows_to_remove.append(i)

        print('List of rows will be removed:')
        print(rows_to_remove)
        
        for row in reversed(rows_to_remove): # reverse để xoá đúng index
            for col in self.data_dict:
                del self.data_dict[col][row]
            
        self.outputCSV(output_file)

    # ================== Chức năng 5 ==================
    # Xóa các cột bị thiếu dữ liệu với ngưỡng tỉ lệ thiếu cho trước
    # Quy ước: 0 <= missing_limit <= 1
    # Những cột bị xoá là những cột có: missing_ratio > missing_limit
    def removeColsMissing(self, missing_limit = 1, output_file = 'removeColsMissing.csv'):
        missing_limit = 0 if missing_limit < 0 else (1 if missing_limit > 1 else missing_limit)
        
        cols_to_remove = []
        
        for col in self.data_dict:
            missing_ratio = self.data_dict[col].count('') / len(self.data_dict[col])
            if missing_ratio > missing_limit:
                cols_to_remove.append(col)
        
        print('List of columns will be removed:')
        print(cols_to_remove)
        
        for col in cols_to_remove:
            del self.data_dict[col]
            
        self.outputCSV(output_file)

    # ================== Chức năng 6 ==================
    # Xóa các mẫu bị trùng lặp
    def removeDuplicates(self, output_file = 'removeDuplicates.csv'):
        
        rows_to_remove = []
        
        # Chuyển từ dictionary qua list
        data = self.data_dict
        rows = []
        for col in data:
            for i, value in enumerate(data[col]):
                if len(rows) <= i:
                    rows.append([])
                rows[i].append(value)
        
        for i, row in enumerate(rows):
            if row in rows[:i]:
                rows_to_remove.append(i)

        print('List of rows will be removed:')
        print(rows_to_remove)
        
        for row in reversed(rows_to_remove): # reverse để xoá đúng index
            for col in self.data_dict:
                del self.data_dict[col][row]
            
        self.outputCSV(output_file)



# Tiến hành xử lý tham số và thực hiện đúng chức năng
if len(sys.argv) <= 2:
    print('>\n> Please add more parameter(s)\n>')
else:
    input_file = sys.argv[1]
    dp = DataPreprocessing(input_file)
    try:
        print('\n----------------------------------------------')
        # ====================== Chức năng 1 ======================
        if sys.argv[2] == 'list-cols-missing':
            dp.listColsMissing()
        # ====================== Chức năng 2 ======================
        elif sys.argv[2] == 'count-rows-missing':
            dp.countRowsMissing()
        # ====================== Chức năng 3 ======================
        elif sys.argv[2] == 'fill-missing':
            if len(sys.argv) == 3:
                dp.fillMissing()
            elif len(sys.argv) == 4:
                dp.fillMissing(sys.argv[3])
            else:
                dp.fillMissing(sys.argv[3], sys.argv[4])
        # ====================== Chức năng 4 ======================
        elif sys.argv[2] == 'remove-rows-missing':
            if len(sys.argv) == 3:
                dp.removeRowsMissing()
            elif len(sys.argv) == 4:
                dp.removeRowsMissing(float(sys.argv[3]))
            else:
                dp.removeRowsMissing(float(sys.argv[3]), sys.argv[4])
        # ====================== Chức năng 5 ======================
        elif sys.argv[2] == 'remove-cols-missing':
            if len(sys.argv) == 3:
                dp.removeColsMissing()
            elif len(sys.argv) == 4:
                dp.removeColsMissing(float(sys.argv[3]))
            else:
                dp.removeColsMissing(float(sys.argv[3]), sys.argv[4])
        # ====================== Chức năng 6 ======================
        elif sys.argv[2] == 'remove-duplicates':
            if len(sys.argv) == 3:
                dp.removeDuplicates()
            else:
                dp.removeDuplicates(sys.argv[3])
        print('----------------------------------------------\n')
    except:
        print('>\n> Please use the right parameter(s)\n>')
        print(sys.argv)