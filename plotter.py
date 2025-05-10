import pandas as pd
import matplotlib.pyplot as plt
import argparse

def plot_motion_data(csv_file):
    # Чтение данных из CSV
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Ошибка: файл {csv_file} не найден")
        return
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    # Проверка наличия необходимых столбцов
    required_columns = ['time', 'com_x', 'com_y', 'com_z', 'zmp_x', 'zmp_y']
    if not all(col in df.columns for col in required_columns):
        print("Ошибка: в файле отсутствуют необходимые столбцы данных")
        print(f"Найдены столбцы: {list(df.columns)}")
        print(f"Ожидаемые столбцы: {required_columns}")
        return

    # Создание фигуры с несколькими subplots
    plt.figure(figsize=(12, 8))

    # График X координат
    plt.subplot(2, 1, 1)
    plt.plot(df['time'], df['com_x'], label='CoM X', color='blue')
    plt.plot(df['time'], df['zmp_x'], label='ZMP X', color='red', linestyle='--')
    plt.xlabel('Время (с)')
    plt.ylabel('Положение (м)')
    plt.title('Сравнение CoM и ZMP по оси X')
    plt.grid(True)
    plt.legend()

    # График Y координат
    plt.subplot(2, 1, 2)
    plt.plot(df['time'], df['com_y'], label='CoM Y', color='green')
    plt.plot(df['time'], df['zmp_y'], label='ZMP Y', color='orange', linestyle='--')
    plt.xlabel('Время (с)')
    plt.ylabel('Положение (м)')
    plt.title('Сравнение CoM и ZMP по оси Y')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

    # Дополнительный график для Z координаты CoM
    plt.figure(figsize=(12, 4))
    plt.plot(df['time'], df['com_z'], label='CoM Z', color='purple')
    plt.xlabel('Время (с)')
    plt.ylabel('Высота (м)')
    plt.title('Высота центра масс (CoM Z)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Настройка аргументов командной строки
    parser = argparse.ArgumentParser(description='Визуализация данных CoM и ZMP')
    parser.add_argument('--file', type=str, default='motion_data.csv',
                       help='Путь к CSV файлу с данными (по умолчанию: motion_data.csv)')
    
    args = parser.parse_args()
    
    # Запуск визуализации
    plot_motion_data(args.file)