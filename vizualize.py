from datetime import datetime

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns

def plot_skewness(input_file, features):
    df = pd.read_csv(input_file)
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    columns_to_plot = [col for col in numeric_columns if col not in ['datetime', 'labels', 'preciptype']]

    # Tạo một lưới có số hàng bằng chiều dài của columns_to_plot và số cột là 1
    num_plots = len(columns_to_plot)
    fig, axes = plt.subplots(num_plots, 1, figsize=(10, 5 * num_plots))

    # Vẽ biểu đồ skewness cho từng trường trong mỗi ô của lưới
    for i, col in enumerate(columns_to_plot):
        sns.histplot(df[col], kde=True, ax=axes[i])
        axes[i].set_title(f'Skewness of {col}')

    # Tối ưu hóa khoảng trống giữa các ô
    plt.tight_layout()
    plt.savefig(f'La{features}.png')
    plt.show()

def plot_line_chart(file_path, features):
    df = pd.read_csv(file_path)

    # Chuyển cột datetime sang định dạng ngày tháng
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Tạo cột mới cho năm
    df['year'] = df['datetime'].dt.year

    # Lọc dữ liệu cho từng năm
    data_1 = df[df['year'] == 2022]
    data_2 = df[df['year'] == 2023]

    # Vẽ biểu đồ line chart cho từng năm
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(data_1['datetime'], data_1[features], label=f'{features} 2022', color='blue')
    plt.title('Temperature Over Time in 2022')
    plt.xlabel('Date')
    plt.ylabel(f'{features}')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(data_2['datetime'], data_2[features], label=f'{features} 2023', color='green')
    plt.title('Temperature Over Time in 2023')
    plt.xlabel('Date')
    plt.ylabel(f'{features}')
    plt.legend()

    plt.tight_layout()

    plt.savefig(f'LineChart{features}.png')

    plt.show()

def multi_scatter_plot(file_path):
    df = pd.read_csv(file_path)

    # Loại bỏ các cột không cần thiết
    cols_to_exclude = ['preciptype']
    df_selected = df.drop(cols_to_exclude, axis=1, errors='ignore')

    # Tách dữ liệu thành hai DataFrame dựa trên giá trị labels
    df_label_0 = df_selected[df['labels'] == 0]
    df_label_1 = df_selected[df['labels'] == 1]

    # Vẽ ma trận scatter plot với màu sắc khác nhau cho từng nhóm
    sns.pairplot(df_selected, hue='labels', palette={0: 'red', 1: 'blue'})
    plt.suptitle('Pairwise Scatter Plots for Selected Fields', y=1.02)
    plt.savefig('scatterPlot.png')
    plt.show()


def scatter_plot(file_path, f1, f2):
    data = pd.read_csv(file_path)
    temp = data[f1]
    labels = data[f2]

    # Đặt màu cho các điểm dựa trên giá trị của cột 'labels'
    colors = ['red' if label == 0 else 'blue' for label in labels]

    # Vẽ Scatter Plot
    plt.scatter(temp, labels, c=colors, alpha=0.5)

    plt.title('Scatter Plot')
    plt.xlabel(f1)
    plt.ylabel(f2)
    plt.savefig(f'ScatterPlot-{f1}-{f2}.png')
    plt.show()

scatter_plot("data.csv", 'dew', 'temp')

def box_plot(file_path, f1, f2):
    df = pd.read_csv(file_path)

    plt.figure(figsize=(10, 6))
    sns.boxplot(x=f1, y=f2, data=df)
    plt.title('Box Plot')
    plt.xlabel(f1)
    plt.ylabel(f2)
    plt.show()


def bar_chart(file_path, x, y):
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['Year'] = df['datetime'].dt.year
    df['Month'] = df['datetime'].dt.month
    df['Day'] = df['datetime'].dt.day
    df['Hour'] = df['datetime'].dt.hour
    x = 'Hour'
    plt.figure(figsize=(10, 6))
    sns.countplot(x=x, hue=y, data=df)
    plt.title(f'Count Plot of Labels by {x}')
    plt.xlabel(x)
    plt.ylabel('Count')

    plt.savefig(f'BarChart-{x}.png')

    plt.show()

def pie_chart(file_path, x):
    file_path = file_path
    data = pd.read_csv(file_path)
    rows_to_drop = data[data['labels'] == 0].sample(n=10000, random_state=42).index
    data = data.drop(index=rows_to_drop).reset_index(drop=True)
    label_counts = data[x].value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(label_counts, labels=label_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution')
    plt.savefig('Pie.png')
    plt.show()


def calculate_correlation(file_path):
    # Đọc file CSV
    df = pd.read_csv(file_path)

    # Loại bỏ các trường không cần thiết
    columns_to_exclude = ['datetime', 'preciptype']
    df_corr = df.drop(columns=columns_to_exclude)

    # Tính toán ma trận mối tương quan
    correlation_matrix = df_corr.corr()

    # Vẽ heatmap mối tương quan
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Correlation Matrix')
    plt.savefig('Corre.png')
    plt.show()


def generate_pie_charts(file_path, x):
    # Đọc file CSV
    data = pd.read_csv(file_path)

    # Tạo cột 'Year' từ cột 'datetime'
    data['Year'] = pd.to_datetime(data['datetime']).dt.year

    # Tạo DataFrame cho năm 1
    data_year1 = data[data['Year'] == 2022]
    label_counts_year1 = data_year1[x].value_counts()

    # Tạo DataFrame cho năm 2
    data_year2 = data[data['Year'] == 2023]
    label_counts_year2 = data_year2[x].value_counts()

    # Tạo hai biểu đồ tròn
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    # Biểu đồ cho năm 1
    axes[0].pie(label_counts_year1, labels=label_counts_year1.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 20})
    axes[0].set_title('Distribution - Year 2022')

    # Biểu đồ cho năm 2
    axes[1].pie(label_counts_year2, labels=label_counts_year2.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 20})
    axes[1].set_title('Distribution - Year 2023')

    plt.savefig('PieCharts.png')
    plt.show()

    plt.savefig('PieCharts.png')
    plt.show()


def generate_double_bar_chart(file_path, x, y):
    # Đọc file CSV
    df = pd.read_csv(file_path)

    # Chuyển cột 'datetime' thành kiểu dữ liệu datetime
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['Month'] = df['datetime'].dt.month
    df['Day'] = df['datetime'].dt.day
    df['Hour'] = df['datetime'].dt.hour

    # Tạo cột 'Year' từ cột 'datetime'
    df['Year'] = df['datetime'].dt.year

    # Tạo DataFrame cho năm 1
    df_year1 = df[df['Year'] == 2022]

    # Tạo DataFrame cho năm 2
    df_year2 = df[df['Year'] == 2023]

    # Tạo hai biểu đồ cột
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))


    # Biểu đồ cho năm 1
    sns.countplot(x=x, hue=y, data=df_year1, ax=axes[0])
    axes[0].set_title(f'Count Plot of {y} by {x} - Year 2022')
    axes[0].set_xlabel(x)
    axes[0].set_ylabel('Count')

    # Biểu đồ cho năm 2
    sns.countplot(x=x, hue=y, data=df_year2, ax=axes[1])
    axes[1].set_title(f'Count Plot of {y} by {x} - Year 2023')
    axes[1].set_xlabel(x)
    axes[1].set_ylabel('Count')

    plt.savefig(f'DoubleBarChart-{x}.png')
    plt.show()


# Sử dụng hàm với file_path là đường dẫn đến file CSV, x là trục x và y là trục y cần phân tích
generate_double_bar_chart('data.csv', 'temp', 'labels')