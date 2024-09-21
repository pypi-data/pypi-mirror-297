import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder, TargetEncoder


def read_data(filepath, delimiter=None, dtype_dict=None):
    """
    Загрузка данных с указанием типов данных

    filepath: путь к файлу с данными
    delimiter: разделитель признаков
    dtype_dict: словарь типов столбцов
    """

    df = pd.read_csv(filepath, delimiter=delimiter, dtype=dtype_dict, on_bad_lines='skip', low_memory=False)

    return df


def print_info(data):
    """
    Вывод информации о датасете

    data: датасет
    """
    print("Сведения о признаках:")
    print(data.info())
    print("Распределение значений в столбцах: \n", data.describe(percentiles=[0.25, 0.5, 0.75]))
    print("Пеример данных: \n", data.sample(10))

    numerical_cols = data.select_dtypes(include=['int', 'float']).columns
    datetime_cols = data.select_dtypes(include=['datetime']).columns
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns

    # Исключаем временные столбцы из категориальных
    categorical_cols = [col for col in categorical_cols if col not in datetime_cols]

    # Гистограммы для числовых переменных
    data[numerical_cols].hist(bins=20, figsize=(15, 10), color='skyblue', edgecolor='black')
    plt.suptitle('Гистограммы числовых признаков')
    plt.show()

    # boxplot для числовых переменных
    plt.figure(figsize=(15, 7))
    sns.boxplot(data=data[numerical_cols], palette="Set2")
    plt.title('Диаграммы размаха числовых признаков')
    plt.xticks(rotation=45)
    plt.show()

    # Стобчатые либо круговые диаграммы для категориальных переменных
    for col in categorical_cols:
        # количество уникальных значений
        num_categories = data[col].nunique()

        # Если количество категорий > 10, то горизонтальный barplot
        if num_categories > 10:
            plt.figure(figsize=(10, 8))
            # Отображаем только топ-10 категорий
            top_categories = data[col].value_counts().nlargest(10)
            sns.barplot(y=top_categories.index, x=top_categories.values, palette="viridis")
            plt.title(f'Топ-10 значений в столбце {col}')
            plt.xlabel('Количество')
            plt.ylabel(col)
            plt.show()
        else:
            # В остальных случаях строим круговую диаграмму
            plt.figure(figsize=(8, 6))
            data[col].value_counts().plot(kind='pie', autopct='%1.1f%%')
            plt.title(f'Распределение значений в столбце {col}')
            plt.ylabel('')
            plt.show()

    # Матрица корреляции для числовых переменных
    plt.figure(figsize=(10, 8))
    sns.heatmap(data[numerical_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Матрица корреляции числовых признаков')
    plt.show()

    # # pairplot для числовых переменных
    # if len(numerical_cols) > 1:
    #     sns.pairplot(data[numerical_cols])
    #     plt.suptitle('Парные графики для числовых переменных', y=1.02)
    #     plt.show()

    # Анализ временных переменных, если они есть
    if len(datetime_cols) > 0:
        # Преобразуем дату в нужный формат
        for col in datetime_cols:
            data[col] = pd.to_datetime(data[col])

        # Временные графики по годам, месяцам, дням и часам
        for col in datetime_cols:
            data['year'] = data[col].dt.year
            data['month'] = data[col].dt.month
            data['day'] = data[col].dt.day
            data['hour'] = data[col].dt.hour

            plt.figure(figsize=(15, 5))
            plt.subplot(2, 2, 1)
            data['year'].value_counts().sort_index().plot(kind='bar')
            plt.title('Количество записей по годам')

            plt.subplot(2, 2, 2)
            data['month'].value_counts().sort_index().plot(kind='bar')
            plt.title('Количество записей по месяцам')

            plt.subplot(2, 2, 3)
            data['day'].value_counts().sort_index().plot(kind='bar')
            plt.title('Количество записей по дням')

            plt.subplot(2, 2, 4)
            data['hour'].value_counts().sort_index().plot(kind='bar')
            plt.title('Количество записей по часам')

            plt.tight_layout()
            plt.show()

        # Удаляем вспомогательные колонки
        data.drop(['year', 'month', 'day', 'hour'], axis=1, inplace=True)


def add_time_to_date(data, date_column, time_column, new_column_name=None):
    """
    Объединение столбцов даты и времени

    data: датасет
    date_column: столбец с датой
    time_column: столбец со временем
    """
    if new_column_name is not None:
        new_column = new_column_name
    else:
        new_column = date_column + 'time'

    # Преобразование даты и времени в единый временной формат
    data[new_column] = pd.to_datetime(data[date_column] + ' ' + data[time_column], dayfirst=True)

    # Удаление исходных столбцов времени и даты
    data.drop([time_column, date_column], axis=1, inplace=True)

    return new_column

def drop_columns(data, columns_to_drop):
    """
    Удаление столбцов из датасета

    data: Список столбцов для удаления
    """
    columns_to_drop = [col for col in columns_to_drop if col in data.columns]
    new_data = data.drop(columns_to_drop, axis=1)

    return new_data

def fill_nan(data, columns=None):
    """
    Заполнение пропущенных значений в признаках пустыми строками

    data: датасет
    columns: столбцы, в которых нужно заполнить пропущенные значения
    """
    if columns is not None:
        data[columns] = data[columns].fillna('')
    else:
        data = data.fillna('')

    return data


def category_to_num(df, encoding_method='label', target_column=None, ordinal_categories=None):
    """
    Преобразование категориальных признаков в числовые с выбором метода кодирования.

    df:  входной датасет
    encoding_method: метод кодирования ('label', 'onehot', 'ordinal', 'target')
    target_column: имя целевой переменной (необходимо для target encoding)
    ordinal_categories: dict, словарь с порядком категорий для ordinal encoding
                               (ключ - имя столбца, значение - список категорий в нужном порядке)

    return:  датасет с закодированными признаками
    """

    data = df.copy(deep=True)
    categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()

    if encoding_method == 'label':
        label_encoder = LabelEncoder()
        for col in categorical_columns:
            data[col] = label_encoder.fit_transform(data[col])

    elif encoding_method == 'onehot':
        onehot_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        encoded_features = onehot_encoder.fit_transform(data[categorical_columns])
        feature_names = onehot_encoder.get_feature_names_out(categorical_columns)
        encoded_df = pd.DataFrame(encoded_features, columns=feature_names, index=data.index)
        data = pd.concat([data.drop(columns=categorical_columns), encoded_df], axis=1)

    elif encoding_method == 'ordinal':
        if ordinal_categories is None:
            ordinal_categories = {}

        for col in categorical_columns:
            if col in ordinal_categories:
                ordinal_encoder = OrdinalEncoder(categories=[ordinal_categories[col]])
                data[[col]] = ordinal_encoder.fit_transform(data[[col]])
            else:
                label_encoder = LabelEncoder()
                data[col] = label_encoder.fit_transform(data[col].astype(str))

    elif encoding_method == 'target':
        if target_column is None:
            raise ValueError("Target column must be specified for target encoding")
        target_encoder = TargetEncoder()
        data[categorical_columns] = target_encoder.fit_transform(data[categorical_columns], data[target_column])

    else:
        raise ValueError("Invalid encoding method.")

    return data

def get_test_train(data, target_column, columns_to_drop):
    """
    Разделение данных на обучающую и тестовую выборки

    data: датасет
    target_column: целеаой признак
    columns_to_drop: список признаков, которые не нужно использовать при обучении
    """
    # Определение целевой переменной и признаков
    columns_to_drop.append(target_column)

    X = data.drop(columns_to_drop, axis=1)
    y = data[target_column]

    # Разделение на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test