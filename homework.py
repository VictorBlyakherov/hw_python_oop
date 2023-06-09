from dataclasses import dataclass


@dataclass
class InfoMessage:

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    """Информационное сообщение о тренировке."""
    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000.0
    MIN_IN_HOUR: float = 60.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод расчета калорий '
                                  'неопределен')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(training_type=type(self).__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLYER: float = 18.0
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLYER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration
                * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLYER: float = 0.035
    CALORIES_HEIGHT_MULTIPLYER: float = 0.029
    SPEED_MULTIPLYER: float = 0.278
    HEIGHT_IN_M_DIVIDER: float = 100.0
    MEAN_SPEED_POW_VALUE: float = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed_in_m_s = (self.get_mean_speed() * self.SPEED_MULTIPLYER)
        height_in_meters = self.height / self.HEIGHT_IN_M_DIVIDER
        return ((self.CALORIES_WEIGHT_MULTIPLYER * self.weight
                + (mean_speed_in_m_s**self.MEAN_SPEED_POW_VALUE
                 / height_in_meters)
                * self.CALORIES_HEIGHT_MULTIPLYER * self.weight)
                * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_SPEED_SHIFT: float = 1.1
    CALORIES_SPEED_MULTIPLYER: float = 2.0
    LEN_STEP: float = 1.38

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

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool
                * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_SPEED_SHIFT)
                * self.CALORIES_SPEED_MULTIPLYER * self.weight * self.duration)


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        return training_types[workout_type](*data)
    except KeyError:
        raise Exception('Несуществующий вид тренировки!')


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('WLK', [3000.33, 2.512, 75.8, 180.1])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
