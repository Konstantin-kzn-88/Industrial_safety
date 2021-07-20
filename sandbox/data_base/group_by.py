# SELECT count(user_id) FROM games WHERE iser_id = 1
# SELECT count(score) FROM games WHERE iser_id = 1
# SELECT count(user_id) as count FROM games WHERE iser_id = 1
# count() sum() avr() (ср.арифм) min() max()

# уникальные игроки
# SELECT count(DISTINCT user_id) as count FROM games
# SELECT DISTINCT user_id as count FROM games


# сумма очков которые набрал первый игрок
# SELECT sum(score) as scores FROM games WHERE user_id =1
# макс. очки которые набрал первый игрок
# SELECT max(score) as scores FROM games WHERE user_id =1

# Группировка сумма очков для каждого из игроков сортировкой
# SELECT user_id, sum(score) as sum
# FROM games
# GROUP BY user_id
# ORDER BY sum DESC

# Группировка сумма очков для каждого из игроков сортировкой
# и условием что число очков больше 300
# SELECT user_id, sum(score) as sum
# FROM games
# WHERE score > 300
# GROUP BY user_id
# ORDER BY sum DESC

# Группировка сумма очков для каждого из игроков сортировкой
# и условием что число очков больше 300 и граничением по
# числу выдаваемых записей
# SELECT user_id, sum(score) as sum
# FROM games
# WHERE score > 300
# GROUP BY user_id
# ORDER BY sum DESC
# LIMIT 1