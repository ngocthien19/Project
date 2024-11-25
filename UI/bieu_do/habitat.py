import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def HabitatChart():
    # Đọc dữ liệu từ file CSV đã làm sạch
    data = pd.read_csv(r"D:\VScode\Python\Project\database\Cleaned_Animal_Dataset.csv")

    # Trích xuất môi trường sống đầu tiên từ mỗi mục trong cột 'Habitat'
    data['Primary Habitat'] = data['Habitat'].apply(lambda x: x.split(',')[0].strip())

    # Đếm tần suất của từng loại môi trường sống chính
    habitat_counts = data['Primary Habitat'].value_counts()

    # Chuyển đổi tần suất thành phần trăm
    habitat_heatmap_data = (habitat_counts / habitat_counts.sum()) * 100

    # Tạo DataFrame để chuẩn bị cho bản đồ nhiệt
    heatmap_df = pd.DataFrame(habitat_heatmap_data).reset_index()
    heatmap_df.columns = ['Habitat', 'Percentage']  # Đặt lại tên cột cho DataFrame

    # Xoay dữ liệu để tương thích với bản đồ nhiệt
    heatmap_df = heatmap_df.pivot_table(index='Habitat', values='Percentage')

    # Tạo đối tượng Figure
    fig, ax = plt.subplots(figsize=(8, 6))

    sns.heatmap(
        heatmap_df,
        annot=True,  # Hiển thị giá trị trên các ô
        fmt=".1f",  # Định dạng giá trị hiển thị (1 chữ số thập phân)
        cmap="YlGnBu",  # Bảng màu 'Yellow-Green-Blue'
        cbar=True,  # Hiển thị thanh chú thích màu
        linewidths=0.5,  # Đường viền giữa các ô
        annot_kws={"size": 10}  # Kích thước font của giá trị hiển thị
    )

    # Thêm tiêu đề và nhãn trục
    plt.title('Heatmap of Habitat Frequencies (%)', fontsize=14)  # Tiêu đề với kích thước chữ 14
    plt.xlabel('')  # Để trống vì bản đồ nhiệt không cần nhãn trục X
    plt.ylabel('Habitat', fontsize=12)  # Nhãn trục Y với kích thước chữ 12

    # Điều chỉnh lề để tránh tràn nội dung
    plt.tight_layout()  # Tự động điều chỉnh các thành phần trong Figure để tránh bị cắt

    return fig
