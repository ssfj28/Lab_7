"""Реализация пузырьковой сортировки с сохранением шагов для анимации."""


def bubble_sort_steps(numbers):
    """Сортирует список по возрастанию и возвращает кадры анимации и результат.

    На каждом проходе сравниваются соседние элементы. Если левый элемент
    больше правого, они меняются местами. После завершения прохода самый
    большой элемент неотсортированной части оказывается в её конце.
    """
    array = numbers.copy()  # Не изменяем исходный список пользователя.
    frames = []
    n = len(array)

    # Первый кадр показывает исходное состояние массива.
    frames.append({
        "values": array.copy(),
        "compared": None,
        "sorted_from": n,
        "message": "Исходный массив. Начинаем сортировку.",
    })

    # После каждого прохода один максимальный элемент встаёт на своё место.
    for pass_number in range(n - 1):
        swapped = False
        remaining_count = n - pass_number

        # В ходе текущего прохода ещё не выделяем новый отсортированный элемент.
        # Он гарантированно встанет на место только после завершения прохода.
        for index in range(remaining_count - 1):
            left = array[index]
            right = array[index + 1]

            if left > right:
                # Кадр до перестановки: подсвечиваем сравниваемую пару.
                frames.append({
                    "values": array.copy(),
                    "compared": (index, index + 1),
                    "sorted_from": remaining_count,
                    "message": f"Сравниваем {left} и {right}: {left} > {right}.",
                })

                # Меняем соседние элементы местами.
                array[index], array[index + 1] = array[index + 1], array[index]
                swapped = True

                # Кадр после перестановки.
                frames.append({
                    "values": array.copy(),
                    "compared": (index, index + 1),
                    "sorted_from": remaining_count,
                    "message": f"Меняем местами: теперь {array[index]} и {array[index + 1]}.",
                })
            else:
                # Если порядок правильный, оставляем элементы на местах.
                frames.append({
                    "values": array.copy(),
                    "compared": (index, index + 1),
                    "sorted_from": remaining_count,
                    "message": f"Сравниваем {left} и {right}: порядок правильный, обмен не нужен.",
                })

        # Только теперь последний элемент прохода можно отметить зелёным.
        frames.append({
            "values": array.copy(),
            "compared": None,
            "sorted_from": remaining_count - 1,
            "message": f"Проход {pass_number + 1} завершён. Самый большой элемент этой части на месте.",
        })

        # Если за проход не было обменов, весь массив уже отсортирован.
        if not swapped:
            break

    # Финальный кадр: весь массив отсортирован.
    frames.append({
        "values": array.copy(),
        "compared": None,
        "sorted_from": 0,
        "message": "Сортировка завершена! Массив упорядочен по возрастанию.",
    })

    return frames, array


if __name__ == "__main__":
    # Небольшой пример запуска алгоритма без анимации.
    sample = [3, 44, 38, 5, 47, 15, 36, 26, 27, 2, 46, 4, 19, 50, 48]
    steps, result = bubble_sort_steps(sample)

    print("Исходный массив:", sample)
    print("Отсортированный массив:", result)
    print("Количество кадров для анимации:", len(steps))
