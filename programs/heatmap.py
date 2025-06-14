import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка данных
df = pl.read_csv("auto_data.csv", null_values=["?"])

# Преобразуем строковые числовые колонки в float
to_float = ['normalized-losses', 'bore', 'stroke', 'horsepower', 'peak-rpm', 'price']
for col in to_float:
    df = df.with_columns([pl.col(col).cast(pl.Float64)])

# Оставим только числовые признаки
numeric_cols = [col for col, dtype in zip(df.columns, df.dtypes) if dtype in [pl.Float64, pl.Int64]]

# Строим корреляционную матрицу
cor_matrix = df.select(numeric_cols).to_pandas().corr()

# Визуализация
plt.figure(figsize=(12, 10))
sns.heatmap(cor_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Корреляционная матрица числовых признаков")
plt.tight_layout()
plt.show()
