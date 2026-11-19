"""Визуализация пузырьковой сортировки и сохранение результата в GIF."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from bubble_sort import bubble_sort_steps


# Значения из примера, приложенного к заданию.
DEFAULT_ARRAY = [3, 44, 38, 5, 47, 15, 36, 26, 27, 2, 46, 4, 19, 50, 48]


def read_array():
    """Запрашивает массив целых чисел. Enter запускает пример из задания."""
    raw = input(
        "Введите целые числа через пробел (Enter — использовать пример): "
    ).strip()

    if not raw:
        return DEFAULT_ARRAY.copy()

    try:
        values = [int(item) for item in raw.split()]
    except ValueError:
        print("Ошибка: вводите только целые числа, разделённые пробелами.")
        raise SystemExit(1)

    if not values:
        print("Массив не должен быть пустым.")
        raise SystemExit(1)

    return values


def format_number(value):
    """Преобразует число в короткую подпись для столбца."""
    return str(value)


def main():
    values = read_array()
    frames, sorted_values = bubble_sort_steps(values)

    # Создаём окно для столбчатой диаграммы.
    figure, axis = plt.subplots(figsize=(12, 6))
    figure.canvas.manager.set_window_title("Визуализация пузырьковой сортировки")
    figure.suptitle("Сортировка пузырьком", fontsize=17, fontweight="bold")

    # Границы вертикальной оси рассчитываем с учётом отрицательных чисел.
    minimum = min(0, min(values))
    maximum = max(0, max(values))
    value_range = max(1, maximum - minimum)
    bottom = minimum - value_range * 0.18
    top = maximum + value_range * 0.25

    def draw_frame(frame_index):
        frame = frames[frame_index]
        current_values = frame["values"]
        compared = frame["compared"]
        sorted_from = frame["sorted_from"]

        axis.clear()
        axis.set_ylim(bottom, top)
        axis.set_xlim(-0.6, len(current_values) - 0.4)
        axis.set_xticks(range(len(current_values)))
        axis.set_xticklabels([str(i + 1) for i in range(len(current_values))])
        axis.set_xlabel("Номер элемента массива")
        axis.set_ylabel("Значение элемента")
        axis.set_title(frame["message"], fontsize=10, pad=14)
        axis.grid(axis="y", linestyle="--", alpha=0.25)
        axis.set_axisbelow(True)

        colors = []
        for position in range(len(current_values)):
            if compared is not None and position in compared:
                colors.append("#F2A541")       # Оранжевый: сравниваемая пара.
            elif position >= sorted_from:
                colors.append("#55A979")       # Зелёный: элемент уже на месте.
            else:
                colors.append("#59B9DF")       # Голубой: ещё не отсортирован.

        bars = axis.bar(
            range(len(current_values)),
            current_values,
            color=colors,
            edgecolor="white",
            linewidth=1.0,
            width=0.78,
        )

        # Подписываем каждый столбец его значением.
        label_offset = value_range * 0.025
        for bar, value in zip(bars, current_values):
            label_y = value + label_offset if value >= 0 else value - label_offset
            vertical_alignment = "bottom" if value >= 0 else "top"
            axis.text(
                bar.get_x() + bar.get_width() / 2,
                label_y,
                format_number(value),
                ha="center",
                va=vertical_alignment,
                fontsize=9,
            )

        axis.text(
            0.99,
            0.97,
            f"Кадр {frame_index + 1} из {len(frames)}",
            transform=axis.transAxes,
            ha="right",
            va="top",
            fontsize=9,
            color="#555555",
        )

    animation = FuncAnimation(
        figure,
        draw_frame,
        frames=len(frames),
        interval=300,
        repeat=False,
        cache_frame_data=False,
    )

    # GIF сохраняется рядом с файлами программы.
    output_path = Path(__file__).with_name("bubble_sort.gif")
    print("Создаю GIF-анимацию. Это может занять некоторое время...")
    animation.save(output_path, writer=PillowWriter(fps=5), dpi=90)

    print("Исходный массив:      ", values)
    print("Отсортированный массив:", sorted_values)
    print("Анимация сохранена:   ", output_path)
    print("Закройте окно анимации, чтобы завершить программу.")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
