# Есть две таблицы games(user_id,score,time) и
# users(rowid,name,sex,old,score)

# чтобы сделать сводный запрос
# SELECT name,sex,games.score FROME games
# JOIN users ON games.user_id = users.rowid

# для записей если если юзера нет
# SELECT name,sex,games.score FROME games
# LEFT JOIN users ON games.user_id = users.rowid

# рейтинг игроков
# Группировка сумма очков для каждого из игроков сортировкой
# SELECT name, sex, sum(games.score) as score
# FROM games
# JOIN users ON games.user_id = users.rowid
# GROUP BY user_id
# ORDER BY score DESC


# объединение двух таблиц tab1 (score, from) и tab2(val,type)
# только уникальные записи
# SELECT score 'from' FROM tab1
# UNION SELECT val, type FROM tab2