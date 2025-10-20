import pandas as pd

purchases = pd.read_csv('files/game_purchases.csv')

# Calculamos la fecha primera de compra(['purchase_datetime'].min()) de cada usuario ('player_id)
first_purchase_dates = purchases.groupby('player_id')[
    'purchase_datetime'].min()

# Cambiamos el nombre del Objeto Series first_purchase_dates con .name = 'first_purchase_datetime'
first_purchase_dates.name = 'first_purchase_datetime'

# Juntamos el DF (purchases) con el Series a en la columna 'player_id' así .join(first_purchase_dates, on='player_id'). Ahora tiene una columna extra
# con el nombre de 'first_purchase_datetime'.
purchases = purchases.join(first_purchase_dates, on='player_id')

# Cambiamos el formato de Object a Datetime para purchase_datetime y creamos una columna('purchase_month') para el DF 
purchases['purchase_datetime'] = pd.to_datetime(purchases['purchase_datetime'])
purchases['purchase_month'] = purchases['purchase_datetime']

# Convertmos la columna 'first_purchase_datetime' a tipo datetime y creamos una columna llamada first_purchase_month
purchases['first_purchase_datetime'] = pd.to_datetime(purchases['first_purchase_datetime'])
purchases['first_purchase_month'] = purchases['first_purchase_datetime']

# groupby(['first_purchase_month', 'purchase_month']): agrupa por cohorte (mes de primera compra) y por mes de compra (periodo).
# purchase_id: nunique → número de compras únicas en ese par (cohorte × mes). &
# player_id: nunique → número de jugadores únicos que hicieron compras en ese par.
purchases_grouped_by_cohorts = purchases.groupby(['first_purchase_month', 'purchase_month']).agg({'purchase_id': 'nunique', 'player_id': 'nunique'})

# Calculamos compras medias por jugador [purchases_id(compra por jugador) / [player_id(cada jugador)]]
purchases_grouped_by_cohorts['purchases_per_player'] = (
    purchases_grouped_by_cohorts['purchase_id']
    / purchases_grouped_by_cohorts['player_id']
)


mean_purchases_pivot  = purchases_grouped_by_cohorts.pivot_table(
                        index= 'first_purchase_month', # Cada cohorte
                        columns= 'purchase_month', # Meses relativos de los que se midieron compras
                        values= 'purchases_per_player', # Promedio de compras por jugador (resuelto en el paso anterior)
                        aggfunc= 'sum' # aquí reúne valores si hubiera múltiples filas para la misma combinación index/columns,
                                       # en este caso, tras el groupby ya hay a lo sumo una fila por combinación, así que sum devuelve ese valor
)

print(mean_purchases_pivot)