from django.db import models


class Dispatcher(models.Model):
    dispatcher_telegram_id = models.BigIntegerField(verbose_name="Диспетчер Telegram ID")
    dispatcher_name = models.CharField(default="", max_length=100, verbose_name="Имя диспетчера", blank=True)

    def __str__(self):
        return self.dispatcher_name

    class Meta:
        verbose_name = "Диспетчер"
        verbose_name_plural = "Диспетчеры"


class Kuryer(models.Model):
    kuryer_telegram_id = models.BigIntegerField(verbose_name="Курьер Telegram ID")
    kuryer_name = models.CharField(default="", max_length=100, verbose_name="Имя курьера", blank=True)
    inwork = models.BooleanField(default=False, verbose_name="Работает?")

    def __str__(self):
        return self.kuryer_name

    class Meta:
        verbose_name = "Курьер"
        verbose_name_plural = "Курьеры"


class Kuryer_group(models.Model):
    kuryer_id = models.BigIntegerField(verbose_name="Group ID")

    def __str__(self):
        return str(self.kuryer_id)

    class Meta:
        verbose_name = "Заказы Telegram Группа"
        verbose_name_plural = "Заказы Telegram Группа"


class Partner(models.Model):
    partner = models.CharField(default="", max_length=512, verbose_name="Партнер")
    status_api_url = models.CharField(default="", max_length=512, blank=True)

    def __str__(self):
        return self.partner

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"


class Shop(models.Model):
    shop = models.CharField(default="", max_length=512, verbose_name="Магазин")
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="Партнер")
    location = models.CharField(default="https://yandex.ru/maps/?pt=longitude,latitude&z=18&l=map", max_length=512,
                                verbose_name="Локация")

    def __str__(self):
        return f"{self.shop}-{self.partner}"

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"


class Operator(models.Model):
    name = models.CharField(max_length=512, verbose_name="Имя оператора")
    telegram_id = models.BigIntegerField(verbose_name="Оператор ID")
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="Партнер")

    def __str__(self):
        return f"{self.name}-{self.partner}"

    class Meta:
        verbose_name = "Оператор"
        verbose_name_plural = "Операторы"


class Kuryer_came_group(models.Model):
    kuryer_id = models.BigIntegerField(verbose_name="Group ID")

    def __str__(self):
        return str(self.kuryer_id)

    class Meta:
        verbose_name = "Группа пришла и ушла"
        verbose_name_plural = "Группа пришла и ушла"

class Price(models.Model):
    a = models.IntegerField(verbose_name="Цена пункта A")
    b1 = models.IntegerField(verbose_name="Цена пункта B(0.1-5 Кг)")
    b2 = models.IntegerField(verbose_name="Цена пункта B(5.1-10 Кг)")
    b3 = models.IntegerField(verbose_name="Цена пункта B(10.1-20 Кг)")
    comis = models.IntegerField(verbose_name="Комиссия NesuVezu %")

    class Meta:
        verbose_name = "Настройки цены"
        verbose_name_plural = "Настройки цены"

