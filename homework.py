class InfoMessage:
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    """Информационное сообщение о тренировке."""
    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; Длительность: '
                f'{self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: '
                f'{self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

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
        pass

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        """Вернуть информационное сообщение о выполненной тренировке."""
        pass


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLYER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLYER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration
                * self.MIN_IN_HOUR)


class SportsWalking(Training):
    CALORIES_WEIGHT_MULTIPLYER = 0.035
    CALORIES_HEIGHT_MULTIPLYER = 0.029
    SPEED_MULTIPLYER = 0.278
    HEIGHT_IN_M_DIVIDER = 100

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
                + (mean_speed_in_m_s**2 / height_in_meters)
                * self.CALORIES_HEIGHT_MULTIPLYER * self.weight)
                * self.duration * self.MIN_IN_HOUR)

    """Тренировка: спортивная ходьба."""


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_SPEED_SHIFT = 1.1
    CALORIES_SPEED_MULTIPLYER = 2
    LEN_STEP = 1.38

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


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking
                      }
    return_training = training_types[workout_type](*data)
    return return_training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


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
