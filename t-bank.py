import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

polzovately = pd.read_excel('dannye.xlsx', sheet_name='Пользователи')
platezhi = pd.read_excel('dannye.xlsx', sheet_name='Платежи')

# на обеих страницах есть пользователь со странными номерами больше 2500, видимо можно удалить
platezhi = platezhi[platezhi['payment_id'] <= 7657]
polzovately = polzovately[polzovately['user_id'] <= 2500]

platezhi = platezhi.drop('payment_id', axis=1)

table = pd.merge(platezhi, polzovately, on='user_id', how='inner')
#table = table.drop('user_id', axis=1)

table_binary = table[['step1_opened', 'step2_entered', 'step3_confirmed', 'step4_success']].notna().astype(int)
table[['step1_opened', 'step2_entered', 'step3_confirmed', 'step4_success']] = table_binary

flags = ['step1_opened', 'step2_entered', 'step3_confirmed', 'step4_success']
table_new = table.groupby('user_id')[flags].sum().reset_index()

user_info = polzovately.drop_duplicates('user_id')  # на всякий случай
table = pd.merge(table_new, user_info, on='user_id', how='inner')

table['step2_%'] = table['step2_entered']/table['step1_opened']*100
table['step3_%'] = table['step3_confirmed']/table['step1_opened']*100
table['step4_%'] = table['step4_success']/table['step1_opened']*100
print(table)


#table = table[table['group'] == 'B']  # можно поменять на А и посмотреть по А

# Добавляем столбец для шага 1 (100% для всех)
table['step1_%'] = 100

# Вычисляем средние проценты по каждому шагу
avg_conv = table[['step1_%', 'step2_%', 'step3_%', 'step4_%']].mean()

# Строим столбчатую диаграмму
plt.figure(figsize=(8, 5))
avg_conv.plot(kind='bar', color=['blue', 'orange', 'green', 'red'])
plt.title('Средняя конверсия по шагам воронки для группы B', fontsize=20)
plt.ylabel('Процент от первого шага, %', fontsize=20)
plt.xlabel('Шаг', fontsize=20)
plt.ylim(0, 100)
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

avg_conv = table[['age', 'group']]  # добавляем группу
plt.figure(figsize=(10, 6))
sns.histplot(data=avg_conv, x='age', hue='group', kde=True, alpha=0.5, bins=15)
plt.title('Гистограмма возраста по группам', fontsize=22)
plt.xlabel('Возраст',  fontsize=22)
plt.ylabel('Частота',  fontsize=22)
plt.show()

avg_conv = table[['city', 'group']]  # добавляем группу
plt.figure(figsize=(10, 6))
sns.histplot(data=avg_conv, x='city', hue='group', kde=True, alpha=0.5, bins=15)
plt.title('Гистограмма городов по группам',  fontsize=22)
plt.xlabel('Город',  fontsize=22)
plt.ylabel('Частота',  fontsize=22)
plt.show()

avg_conv = table[['device_type', 'group']]  # добавляем группу
plt.figure(figsize=(10, 6))
sns.histplot(data=avg_conv, x='device_type', hue='group', kde=True, alpha=0.5, bins=15)
plt.title('Гистограмма типа устройства по группам', fontsize=22)
plt.xlabel('Тип устройства', fontsize=22)
plt.ylabel('Частота', fontsize=22)
plt.show()


