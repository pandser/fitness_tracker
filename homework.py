from typing import Type, Dict
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.wight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'В {self.__class__.__name__} '
                                  f'функция get_spent_calories не определена.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(str(self.__class__.__name__),
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )
        return info

    def duration_to_min(self) -> float:
        """Переводит время тренировки в минуты"""
        return self.duration * self.MIN_IN_HOUR


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_RUN_1: float = 18
    COEFF_CALORIE_RUN_2: float = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_RUN_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_RUN_2) * self.wight
                / self.M_IN_KM * self.duration_to_min())


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_WLK_1: float = 0.035
    COEFF_CALORIE_WLK_2: float = 0.029
    POWER: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_WLK_1 * self.wight
                + (self.get_mean_speed()**self.POWER // self.height)
                * self.COEFF_CALORIE_WLK_2 * self.wight)
                * self.duration_to_min())


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALORIE_SWM_1: float = 1.1
    COEFF_CALORIE_SWM_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_CALORIE_SWM_1)
                * self.COEFF_CALORIE_SWM_2 * self.wight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts: Dict[str, Type[Training]] = {'SWM': Swimming,
                                           'RUN': Running,
                                           'WLK': SportsWalking}
    try:
        return workouts[workout_type](*data)
    except KeyError:
        print('Неизвестная тренировка.')


def main(training: Training) -> None:
    """Главная функция."""
    try:
        info: InfoMessage = training.show_training_info()
        print(info.get_message())
    except AttributeError:
        print('Не удается вывести информацию о тренировке.')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
