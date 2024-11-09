
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import numpy as np
import matplotlib.ticker as mtick
import os


# DATA EXPLORATION - CONHECENDO OS DADOS

# CAMINHO DO ARQUIVO
folder_path = '/Users/joaokasprowicz/Desktop/archive/'

#CRIANDO UM DATA FRAME VAZIO PARA TODAS AS VENDAS
combined_data = pd.DataFrame()

# CONCATENANDO TODOS OS ARQUIVOS CSV QUE ESTAO NO DIRETORIO
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        combined_data = pd.concat([combined_data, df])

#RENOMEANDO AS COLUNAS
combined_data = combined_data.rename(mapper=str.strip, axis='columns')
combined_data = combined_data.rename(columns={'Order ID':'Order_id','Quantity Ordered':'Quantity','Price Each': 'Price','Order Date': 'Date', 'Purchase Address': 'Address'})

#COLOCANDO EM LETRAS MINUSCULAS
column_name = list(combined_data.columns)
column_name = [x.lower().strip() for x in column_name]
combined_data.columns = column_name

#MOSTRANDO AS INFORMAÇOES DOS DADOS
print(combined_data.info())
print(combined_data.head())

#DATA CLEANING - LIMPEZA DOS DADOS
#VERIFICANDO TODAS AS LINHAS QUE POSSUEM NULL VALUES
print('rows contain null:')
print(combined_data.isnull().sum())

#VERIFICANDO LINHAS DUPLICADAS
print('rows contain duplicates:', combined_data.duplicated().sum())

#VERIFICANDO ITENS NÃO NUMERICOS EM COLUNAS
print('non-numeric in order_id:', combined_data['order_id'].loc[pd.to_numeric(combined_data['order_id'], errors='coerce').isnull()].unique())
print('non-numeric in quantity:', combined_data['quantity'].loc[pd.to_numeric(combined_data['quantity'], errors='coerce').isnull()].unique())
print('non-numeric in price:', combined_data['price'].loc[pd.to_numeric(combined_data['price'], errors='coerce').isnull()].unique())

#EXCLUINDO LINHAS COM NULL VALUES
clean_sales_df = combined_data.dropna(how='all')

#EXCLUINDO LINHAS COM VALORES DUPLICADOS (ID)
clean_sales_df = clean_sales_df[~ clean_sales_df.duplicated()]

#EXCLUINDO VALORES NÃO NUMERICOS EM ORDER_ID, QUANTIDADE E PREÇO
clean_sales_df = clean_sales_df[pd.to_numeric(clean_sales_df['order_id'], errors='coerce').notnull()]
clean_sales_df = clean_sales_df[pd.to_numeric(clean_sales_df['quantity'], errors='coerce').notnull()]
clean_sales_df = clean_sales_df[pd.to_numeric(clean_sales_df['price'], errors='coerce').notnull()]

#VERIFICANDO O RESULTADO DO DATA CLEANING
print('linhas contendo null values:')
print(clean_sales_df.isnull().sum())

print('linhas contendo duplicados')
print(clean_sales_df.duplicated().sum())

#MUDAR OS TIPOS DE DADOS PADRONIZANDO ( INTEGERS, FLOATS, DATES E ENDEREÇOS)
clean_sales_df['quantity'] = clean_sales_df['quantity'].astype(int)
clean_sales_df['price'] = clean_sales_df['price'].astype(float)
clean_sales_df['date'] = pd.to_datetime(clean_sales_df['date'], format='%m/%d/%y %H:%M')
clean_sales_df['address'] = clean_sales_df['address'].astype(str)

#ADICIONAR COLUNAS COMO CIDADE E ESTADO
clean_sales_df['city'] = clean_sales_df['address'].apply(lambda x: x.split(',')[1].strip())
clean_sales_df['state'] = clean_sales_df['address'].apply(lambda x: x.split(',')[2].split(' ')[1].strip())

#ADICIONAR UMA COLUNA DE VENDA TOTAL QUE BASICAMENTE MULTIPLICA A COLUNA PREÇO PELA QUANTIDADE COMPRADA.
clean_sales_df['total_sales'] = clean_sales_df['quantity'] * clean_sales_df['price']

#manipulação dos dados
clean_sales_2019_df = pd.DataFrame(clean_sales_df[clean_sales_df['date'].dt.year == 2019])
clean_sales_2020_df = pd.DataFrame(clean_sales_df[clean_sales_df['date'].dt.year == 2020])


#Somando o total de vendas por ano
vendas_2019 = clean_sales_2019_df['total_sales'].sum()
vendas_2020 = clean_sales_2020_df['total_sales'].sum()


#criando o grafico de barras (bar plot)
total_sales_data = [vendas_2019, vendas_2020]
plt.bar(['2019', '2020'], total_sales_data, color='skyblue')
plt.xlabel('Ano')
plt.ylabel('Dolares')
plt.title('Vendas totais (2019 vs. 2020)')
plt.gca().get_yaxis().set_major_formatter('${x:,.0f}')



for i, value in enumerate(total_sales_data):
    plt.text(i, value, f'${value:,.0f}', ha='center', va='bottom', fontweight='bold')

#customizando o estilo do grafico
plt.grid(axis='y', linestyle='--')
plt.ylim(0, max(total_sales_data) * 1.1)
plt.show()

monthly_sales_2019 = clean_sales_2019_df.groupby(clean_sales_2019_df['date'].dt.month)['total_sales'].sum()

# CALCULANDO A MEDIA DE VENDAS PARA ADICIONAR NO GRAFICO
average_sales = monthly_sales_2019.mean()
plt.text(monthly_sales_2019.index[-1], average_sales, f'Média: ${average_sales:,.0f}', ha='right', va='bottom', fontweight='bold', fontsize=8)


#Criando um grafico de linhas
plt.plot(monthly_sales_2019.index, monthly_sales_2019.values, marker='o', linestyle='-', color='skyblue')

plt.axhline(average_sales, color='lightgray', linestyle='--', linewidth=1, label='Average')


#Legendas da grafico
plt.xlabel('Mês')
plt.ylabel('Dolares')
plt.title('Vendas Mensais em 2019')

#Rotação das legendas do eixo x para melhorar a visualização
month_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Maio', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
plt.xticks(monthly_sales_2019.index, month_labels, fontsize=8, rotation=45, ha='right')

#Editando o grafico de linha, retirando os resultado disponibilizados em notação cientifica uma vez que são resultados em milhares de dolares.
plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.ylim(0, max(monthly_sales_2019) * 1.1)
plt.gca().get_yaxis().get_major_formatter().set_scientific(False)
plt.gca().get_yaxis().set_major_formatter('${x:,.0f}')


#editando as legendas do eixo y
plt.gca().get_yaxis().set_major_formatter('${x:,.0f}')


# adicionando vendas totais como legenda
for x, y in zip(monthly_sales_2019.index, monthly_sales_2019.values):
    plt.text(x, y, f'${y:,.0f}', ha='center', va='top', fontsize=8, fontweight='bold')

#adicionando um background
plt.grid(color='lightgray', linestyle='--', linewidth=0.5, alpha=0.5)


#explorar vendas por estado e cidades plotando graficos, para criação de estratégias para empresa
vendas_por_cidade = clean_sales_2019_df.groupby(clean_sales_2019_df['city'])['total_sales'].sum()
plt.figure(figsize=(10,6))
plt.bar(vendas_por_cidade.index, vendas_por_cidade.values)
plt.title('Vendas por Cidade', fontsize=16)
plt.xlabel('Cidades', fontsize=14)
plt.ylabel('Vendas Totais', fontsize=14)
plt.gca().get_yaxis().set_major_formatter('${x:,.0f}')
plt.xticks(rotation=45, ha='right')

#pedidos por horas
clean_sales_2019_df['hour'] = clean_sales_2019_df['date'].dt.hour
hours = [hour for hour, ft in clean_sales_2019_df.groupby('hour')]
plt.figure(figsize=(14,8))
plt.plot(hours, clean_sales_2019_df.groupby(['hour']).count())
# let's add grid
plt.grid(True)
plt.title( # title
    "Qual horário deve ser divulgado as promoções?",
    weight="bold", # weight
    fontsize=35, # font-size
    pad=30
)
plt.xlabel( # x-label
    "Horas",
    weight="bold", # weight
    color="purple", # color
    fontsize=25, # font-size
    loc="center" # location
)
plt.xticks( # x-ticks
    ticks=hours, # labels
    weight="bold", # weight
    fontsize=15 # font-size
)
plt.ylabel( # y-label
    "Numero de Pedidos",
    weight="bold", # weight
    color="black", # color
    fontsize=20 # font-size
)
plt.yticks( # y-ticks
    weight="bold", # weight
    fontsize=15 # font-size
);

#Qual produto vendeu mais? Quais produtos mais populares? Relação
produtos_vendidos = clean_sales_2019_df.groupby(clean_sales_2019_df['product'])['quantity'].sum()
top_selling = produtos_vendidos.sort_values(ascending=False)[:10]
plt.figure(figsize=(10,6))
plt.barh(top_selling.index, top_selling.values, color='blue')
plt.title('Top 10 Selling Products', fontsize=16)
plt.xlabel('Quantity Ordered', fontsize=14)
plt.ylabel('Product', fontsize=14)
plt.gca().invert_yaxis()


#criação dos graficos
plt.tight_layout()
plt.show()
