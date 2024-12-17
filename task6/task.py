import json
import typing as tp

# Входные данные
INPUT_DATA = """{
    "холодно": [
        [0, 1],
        [16, 1],
        [20, 0],
        [50, 0]
    ],
    "комфортно": [
        [16, 0],
        [20, 1],
        [22, 1],
        [26, 0]
    ],
    "жарко": [
        [0, 0],
        [22, 0],
        [26, 1],
        [50, 1]
    ]
}"""

REGULATOR_DATA = """
{
    "слабо": [[0, 1], [6, 1], [10, 0], [20, 0]],
    "умеренно": [[6, 0], [10, 1], [12, 1], [16, 0]],
    "интенсивно": [[0, 0], [12, 0], [16, 1], [20, 1]]
}
"""

RULES = """
{
    "холодно": "интенсивно",
    "комфортно": "умеренно",
    "жарко": "слабо"
}
"""


class LinearFunctionSegment:
    """Класс для представления линейного сегмента функции."""

    def __init__(self, k: float, b: float, left: float, right: float) -> None:
        self.k = k  # Коэффициент перед x
        self.b = b  # Свободный член
        self.left = left  # Левая граница
        self.right = right  # Правая граница

    def __str__(self):
        return f"y = {self.k}*x + {self.b}; x ∈ [{self.left}, {self.right}]"

    def __repr__(self):
        return self.__str__()


def calculate_linear_params(p1: tp.Tuple[float, float], p2: tp.Tuple[float, float]) -> tp.Tuple[float, float]:
    """Вычисление коэффициентов k и b для линейной функции через две точки."""
    if p2[1] == p1[1]:
        return 0, p2[1]
    k = (p2[1] - p1[1]) / (p2[0] - p1[0])
    b = p2[1] - k * p2[0]
    return k, b


def create_function_segments(points: tp.List[tp.List[float]]) -> tp.List[LinearFunctionSegment]:
    """Создание линейных сегментов для заданного множества точек."""
    segments = []
    for i in range(1, len(points)):
        k, b = calculate_linear_params(points[i - 1], points[i])
        segments.append(LinearFunctionSegment(k, b, points[i - 1][0], points[i][0]))
    return segments


def parse_input_to_functions(input_data: tp.Dict[str, tp.List[tp.List[float]]]) -> tp.Dict[str, tp.List[LinearFunctionSegment]]:
    """Парсинг входных данных и создание функций."""
    return {key: create_function_segments(value) for key, value in input_data.items()}


def fuzzify(rule: str, value: float, functions: tp.Dict[str, tp.List[LinearFunctionSegment]]) -> float:
    """Фаззификация значения по указанному правилу."""
    for segment in functions[rule]:
        if segment.left <= value <= segment.right:
            return max(0.0, segment.k * value + segment.b)
    return 0.0


def activate(rule: str, fuzz_value: float, functions: tp.Dict[str, tp.List[LinearFunctionSegment]]) -> float:
    """Активация функции по фаззифицированному значению."""
    for segment in functions[rule]:
        if segment.k != 0:
            x = (fuzz_value - segment.b) / segment.k
            if segment.left <= x <= segment.right:
                return x
    return 0.0


def main(input_value: float) -> float:
    """Основная функция для расчёта по правилам."""
    temperature_data = json.loads(INPUT_DATA)
    temperature_functions = parse_input_to_functions(temperature_data)

    regulator_data = json.loads(REGULATOR_DATA)
    regulator_functions = parse_input_to_functions(regulator_data)

    rules_mapping = json.loads(RULES)

    fuzzified_values = {}
    activated_values = {}
    rule_results = []

    for temp_rule, regulator_rule in rules_mapping.items():
        # Фаззификация
        fuzz_value = fuzzify(temp_rule, input_value, temperature_functions)
        fuzzified_values[temp_rule] = fuzz_value

        # Активация
        activated_value = activate(regulator_rule, fuzz_value, regulator_functions)
        activated_values[regulator_rule] = activated_value

        # Агрегация
        rule_results.append(min(fuzz_value, activated_value))

    print("Фаззификация:", fuzzified_values)
    print("Активация:", activated_values)
    print("Результаты правил:", rule_results)

    # Выбор наилучшего результата
    best_result_index = rule_results.index(max(rule_results))
    selected_rule = list(activated_values.keys())[best_result_index]

    # Поиск ближайшего максимума
    for point in regulator_data[selected_rule]:
        if point[1] == 1 and point[0] > activated_values[selected_rule]:
            return point[0]
    return 0.0


if __name__ == "__main__":
    result = main(17)
    print("Результат:", result)
