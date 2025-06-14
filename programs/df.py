import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
df = pl.read_csv("auto_data.csv", null_values=["?"])
to_float = ['normalized-losses', 'bore', 'stroke', 'horsepower', 'peak-rpm', 'price', "city-mpg", "highway-mpg"]
for col in to_float:
    df = df.with_columns([pl.col(col).cast(pl.Float64)])
df = df.with_columns([pl.col("symboling").cast(pl.Int64)])


def heatmap():
    # Подбор данных
    numeric_cols = [col for col, dtype in zip(df.columns, df.dtypes) if dtype in [pl.Float64, pl.Int64]]

    # Строим тепловую карту
    cor_matrix = df.select(numeric_cols).to_pandas().corr()

    # Рисуем
    plt.figure(figsize=(12, 10))
    sns.heatmap(cor_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Тепловая карта")
    plt.tight_layout()
    plt.show()

def body_style_pie():
    kus = df['body-style']
    #создание новой таблицы с значением числа  названия кузовняка
    kus_ch = df.group_by('body-style').agg([pl.len().alias('num')])
    
    # Переводим в pandas для визуализации(
    kus_pd =  kus_ch.to_pandas()

    # рисуем
    plt.figure(figsize=(7, 7))
    plt.pie(kus_ch['num'], labels=kus_ch['body-style'], autopct='%1.1f%%')
    plt.title("кузова")
    plt.show()

#отображение графика зав мощности и расходов(на трассе и в городе)
def hp_mghc_mghh():
    df_i = df
    # Удаляем строки с пропущенными значениями в этих колонках
    df_clean = df_i.drop_nulls(["horsepower", "city-mpg", "highway-mpg"])
    # Сортируем по мощности
    df_sorted = df_clean.sort("horsepower") 
    # привод в pandas
    df_plot = df_sorted.select(["horsepower", "city-mpg", "highway-mpg"]).to_pandas()
    # рисуем
    plt.figure(figsize=(10, 6))
    plt.plot(df_plot["horsepower"], df_plot["city-mpg"], label="расход в городе", color="blue", linewidth=2)
    plt.plot(df_plot["horsepower"], df_plot["highway-mpg"], label="расход на трассе", color="grey", linewidth=2)
    plt.title("Зависимость расхода топлива от мощности двигателя", fontsize=14)
    plt.xlabel("Мощность (horsepower)", fontsize=12)
    plt.ylabel("Расход топлива (mpg)", fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def reliability_top():
    #Создаем копию что бы ничего не натворить с оригиналом 
    df_i = df
    # Группируем по марке и считаем среднее значение symboling
    avg_symboling = (df.group_by("make").agg(pl.col("symboling").mean().alias("avg_symboling")).sort("avg_symboling"))

    # Вывод
    top = avg_symboling.head(10)
    print(top)

def drive_heels_pie():
    prv = df['drive-wheels']
    #создание новой таблицы с значением числа различных приводов 
    prv_ch = df.group_by('drive-wheels').agg([pl.len().alias('num')])
    # Переводим в pandas для визуализации(
    prv_pd =  prv_ch.to_pandas()
    # рисуем
    plt.figure(figsize=(7, 7))
    plt.pie(prv_ch['num'], labels=prv_ch['drive-wheels'], autopct='%1.1f%%')
    plt.title("Приводы")
    plt.show()

def hp_rpm_graf():
    #собрираем и подшотавливаем спец. копию
    df_i = df
    df_clean = df_i.drop_nulls(["horsepower", "peak-rpm"])
    df_sorted = df_clean.sort("peak-rpm")

    # Переводим в pandas
    df_plot = df_sorted.select(["peak-rpm", "horsepower"]).to_pandas()

    # рисуем
    plt.figure(figsize=(10, 6))
    plt.plot(df_plot["peak-rpm"], df_plot["horsepower"], 'o-', color="purple")
    plt.title("Зависимость мощности от максимальных оборотов двигателя", fontsize=14)
    plt.xlabel("Обороты")
    plt.ylabel("Мощность")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def price_top():
    #подготовка
    df_i = df
    df_i = df_i.drop_nulls(["price"])

    # Группировка и расчет средней цены
    sr_price = (df_i.group_by("make").agg(pl.col("price").mean().alias("sr_price")).sort("sr_price", descending=True))
    top =sr_price.head(10)
    tail = sr_price.tail(10)

    # Выводим
    print(top)
    print(tail)

def price_sym_graf():
    df_i = df
    df_clean = df_i.drop_nulls(["price", "symboling"])

    # Группируем по марке и считаем среднюю цену и рейтинг надёжности
    avg_data = (
        df_clean.group_by("make").agg([pl.col("price").mean().alias("avg_price"),pl.col("symboling").mean().alias("avg_symboling")]).sort("avg_symboling"))

    # Переводим в pandas
    df_plot = avg_data.to_pandas()

    # Строим график
    plt.figure(figsize=(10, 6))
    plt.scatter(df_plot["avg_symboling"], df_plot["avg_price"], color="darkorange", s=80)
    for i, row in df_plot.iterrows():
        plt.text(row["avg_symboling"] + 0.05, row["avg_price"], row["make"], fontsize=9)
    plt.title("Зависимость средней цены от рейтинга надёжности (symboling)", fontsize=14)
    plt.xlabel("Средний рейтинг symboling (меньше = надёжнее)")
    plt.ylabel("Средняя цена ($)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    #heatmap()
    #body_style_pie()
    #hp_mghc_mghh()
    #reliability_top()
    #drive_heels_pie()
    #hp_rpm_graf()
    #price_top()
    #price_sym_graf()

if __name__ == '__main__':
    main()