import pandas as pd
import glob

# Đường dẫn đến thư mục chứa các file CSV cần merge
folder_path = 'data'

# Đọc tất cả các file CSV trong thư mục
all_files = glob.glob(folder_path + "/*.csv")

# Tạo một list để chứa các đối tượng DataFrame từ các file CSV
dfs = []

# Đọc từng file CSV và thêm vào list
for file in all_files:
    df = pd.read_csv(file)
    dfs.append(df)

# Merge các DataFrame trong list thành một DataFrame lớn
merged_df = pd.concat(dfs, ignore_index=True)

# Lưu DataFrame lớn ra file CSV mới
merged_df.to_csv('merged_data.csv', index=False)

