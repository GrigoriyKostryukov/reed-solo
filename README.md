# Код Рида-Соломона + декодер Питерсона

## Запуск
```
> python app.py source_filename.txt
```

## Параметры поля и декодера
Параметры поля - константы в классе Field.
Параметры кода (j0, t) передаются через конструктор класса ReedSolomon

## Формат входного файла
```
1
001 041 310 424 441 141 022 423 022 030 401 012
```
* 1 строка:
0 - закодировать
1 - декодировать
* 2 строка:
Коэффициенты при степенях х от старшего к младшему (группы цифр).
Каждая группа цифр - коэффициенты многочлена поля (от старшего к младшему)



