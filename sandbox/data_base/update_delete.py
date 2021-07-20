# UPDATE user SET score = 0
# UPDATE user SET score = 1000 WHERE rowid = 1
# UPDATE user SET score = score+500 WHERE sex = 1
# UPDATE user SET score = 1500 WHERE name LIKE 'Dev'
# UPDATE user SET score = score+500 WHERE name LIKE 'D%' - для всех кто начинается с D
# UPDATE user SET score = score+500 WHERE name LIKE 'D_v%' - для всех кто начинается с D,
# второй символ любой, третий v, потом любое продолжение строки
# UPDATE user SET score = 1000, old = 45 WHERE old > 40

# DELETE FROM users WHERE rowid IN(2,5) - удалить rowid 2 и 5
