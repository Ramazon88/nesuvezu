from datetime import timedelta, date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils.datetime_safe import date

from confcontrol.models import *
from django.db.models.signals import post_save, pre_delete
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Update, Bot
from config.settings import NESU_TOKEN
from django.dispatch import receiver


def inform(obj):
    info = f"<strong>Номер доставка:</strong> {obj.id}\n"
    info += f"<strong>Тип доставка:</strong> {obj.type_delever1}\n"
    info += f"<strong>Товар:</strong> {obj.name_model}\n"
    info += f"<strong>Тип приобретения:</strong> {obj.type_pay}\n"
    info += f"<strong>Тип оплаты:</strong> {obj.pay}\n"
    if obj.price == "":
        pass
    else:
        info += f"<strong>Сумма:</strong> {obj.price}\n"
    info += f"<strong>Имя клиента:</strong> {obj.name_customer}\n"
    info += f"<strong>Номер клиента:</strong> {obj.phone_customer}\n"
    info += f"<strong>Время доставки: </strong>{obj.date_delever}\n"
    if obj.weight <= 5:
        info += "<strong>Вес Товара: </strong>0.1-5 Кг\n"
    elif obj.weight <= 10:
        info += "<strong>Вес Товара: </strong>5.1-10 Кг\n"
    elif obj.weight <= 20:
        info += "<strong>Вес Товара: </strong>10.1-20 Кг\n"

    if obj.to_location[:5] == "https":
        info += f"<strong>Куда доставить:</strong> <a href='{obj.to_location}'>Локация</a>\n"
    else:
        info += f"<strong>Куда доставить:</strong> {obj.to_location}\n"
    if obj.from_location[:5] == "https":
        info += f"<strong>Откуда доставить:</strong> <a href='{obj.from_location}'>{obj.shop}</a>\n"
    else:
        info += f"<strong>Откуда доставить:</strong> {obj.from_location}\n"

    if obj.comment == "":
        pass
    else:
        info += f"<strong>Комментарии:</strong> {obj.comment}\n"
    info += f"<strong>Партнер:</strong> {obj.partner}\n"
    info += f"<strong>Оператор:</strong> {obj.admin_name}"
    return info


class Kuryer_step(models.Model):
    admin_id = models.BigIntegerField()
    step = models.BigIntegerField(default=0, blank=True)
    obj = models.BigIntegerField(default=0, blank=True)


class Disp_step(models.Model):
    admin_id = models.BigIntegerField()
    step = models.BigIntegerField(default=0, blank=True)
    obj = models.BigIntegerField(default=0, blank=True)


class Step(models.Model):
    admin_id = models.BigIntegerField()
    step = models.BigIntegerField(default=1, blank=True)
    type_delever = models.CharField(default="", max_length=100, verbose_name="ТИП ДОСТАВКА", blank=True)
    type_delever1 = models.CharField(default="", max_length=100, verbose_name="ТИП ДОСТАВКА1", blank=True)
    name_model = models.CharField(default="", max_length=300, verbose_name="Mahsulot nomi", blank=True)
    pay = models.CharField(default="", max_length=100, verbose_name="To`lov usuli", blank=True)
    type_pay = models.CharField(default="", max_length=100, verbose_name="ТИП ПРИОБРЕТЕНИЯ", blank=True)
    price = models.CharField(default="", max_length=100, verbose_name="Summa", blank=True)
    name_customer = models.CharField(default="", max_length=100, verbose_name="Mijoz ismi")
    phone_customer = models.CharField(default="", max_length=100, verbose_name="Telefon raqami", blank=True)
    date_delever = models.CharField(default="", max_length=100, verbose_name="Yetkazib berish vaqti", blank=True)
    from_location = models.CharField(default="", max_length=500, verbose_name="Qayerdan", blank=True)
    to_location = models.CharField(default="", max_length=500, verbose_name="Qayerga", blank=True)
    shop = models.CharField(default="", max_length=100, verbose_name="Do`kon", blank=True)
    weight = models.IntegerField(verbose_name="Масса", default=0)
    comment = models.CharField(default="", max_length=512, verbose_name="Kamentariya", blank=True)


class Order(models.Model):
    admin_id = models.BigIntegerField(verbose_name="Оператор ID")
    partner = models.CharField(max_length=100, verbose_name="Партнер")
    api = models.BooleanField(null=True)
    admin_name = models.CharField(max_length=100, verbose_name="Имя оператора")
    datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    type_delever = models.CharField(max_length=100, verbose_name="ТИП ДОСТАВКА")
    type_delever1 = models.CharField(max_length=100, verbose_name="ПЕРСОНАЛНЫЙ ТИП ДОСТАВКА", null=True, blank=True)
    multi = models.BooleanField(default=False, verbose_name="МУЛТИДОСТАВКА")
    name_model = models.CharField(max_length=300, verbose_name="Наименование товара")
    pay = models.CharField(max_length=100, verbose_name="ТИП ОПЛАТЫ", blank=True)
    price = models.CharField(default="", max_length=100, verbose_name="Сумма", blank=True)
    name_customer = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone_customer = models.CharField(max_length=100, verbose_name="Телефонный номер")
    date_delever = models.CharField(max_length=500, verbose_name="Срок поставки")
    from_location = models.CharField(max_length=2000, verbose_name="Откуда забрать")
    to_location = models.CharField(max_length=2000, verbose_name="Куда доставить")
    type_pay = models.CharField(max_length=100, verbose_name="ТИП ПРИОБРЕТЕНИЯ")
    shop = models.CharField(max_length=256, verbose_name="Магазин")
    before_image = models.CharField(default="", max_length=100, verbose_name="Первая картинка", blank=True)
    after_image = models.CharField(default="", max_length=100, verbose_name="Вторая картинка", blank=True)
    comment = models.CharField(default="", max_length=512, verbose_name="Комментарий", blank=True)
    status = models.CharField(default="Заказ оформлен", max_length=512, verbose_name="Статус", blank=True)
    kuryer = models.CharField(default="", max_length=512, verbose_name="Курьер", blank=True)
    parent_delevery = models.CharField(default="", max_length=512, verbose_name="Корзинка", blank=True)
    multiorder = models.CharField(default="", max_length=512, verbose_name="Мултизаказ", blank=True)
    step = models.BigIntegerField(default=0, blank=True)
    # Do`kondan chiqdimi
    shop_came = models.BooleanField(default=False)
    # Dispatcher comment
    dis_comment = models.CharField(default="", max_length=512, verbose_name="Примечание", blank=True)
    delete_message_id = models.BigIntegerField(default=0, blank=True)
    a = models.IntegerField(verbose_name="Цена пункта A", default=0)
    b = models.IntegerField(verbose_name="Цена пункта B", default=0)
    b1 = models.IntegerField(verbose_name="Цена пункта B(0.1-5 Кг)", default=0)
    b2 = models.IntegerField(verbose_name="Цена пункта B(5.1-10 Кг)", default=0)
    b3 = models.IntegerField(verbose_name="Цена пункта B(10.1-20 Кг)", default=0)
    weight = models.FloatField(verbose_name="Масса", default=0)
    comis = models.IntegerField(verbose_name="Комиссия NesuVezu %", default=0)
    done_time = models.CharField(default="", blank=True, max_length=521, verbose_name="Время завершение доставки")

    @property
    def price_partner(self):
        price = 0
        full = 0
        if (self.status == "🔁Возврат товара" or self.status == "✅Завершен" or self.status == "Заказ отменен"
        ) and str(self.type_delever)[0] == "A":
            obj = Order.objects.get(pk=self.pk)
            obj = obj.parent_delevery.split(" ")
            if obj[0] == "":
                obj = obj[1:]
            for i in obj:
                if "B" in Order.objects.get(pk=i).type_delever1:
                    price += int(Order.objects.get(pk=i).b)
                if Order.objects.get(pk=i).status not in ["🔁Возврат товара", "✅Завершен", "Заказ отменен"]:
                    full += 1
            objk = str(self.type_delever).split("-")
            price += objk.count("A") * int(self.a)
            if "B" in str(self.type_delever1):
                price += int(self.b)
            if full > 0:
                return 0
            return price
        else:
            return price

    price_partner.fget.short_description = "Оплата партнера"

    def __str__(self):
        return self.name_model

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Message(models.Model):
    short_disc = models.CharField(verbose_name="Заголовок", max_length=256)
    message = models.TextField(verbose_name="Сообщение")
    image = models.ImageField(null=True, blank=True, verbose_name="Фото")
    operator = models.BooleanField(default=False, verbose_name="Оператор")
    dispatcher = models.BooleanField(default=False, verbose_name="Диспетчер")
    kuryer = models.BooleanField(default=False, verbose_name="Курьер")

    def __str__(self):
        return self.short_disc

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Pay_kuryer(models.Model):
    kuryer = models.ForeignKey(Kuryer, on_delete=models.CASCADE, verbose_name="Курьер", null=True, blank=True)
    datetime = models.DateField(verbose_name="Начало период")
    datetime_apply = models.DateField(null=True, verbose_name="Конец период")

    @property
    def price(self):
        if self.kuryer.kuryer_name == "ИТОГО":
            total_price = []
            obj = Order.objects.filter(datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                total_price.append(int(i.price_partner) * (1 - (int(i.comis) / 100)))
            return sum(total_price)

        else:
            total_price = []
            obj = Order.objects.filter(kuryer=self.kuryer.kuryer_name,
                                       datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                total_price.append(int(i.price_partner) * (1 - (int(i.comis) / 100)))
            return sum(total_price)

    price.fget.short_description = "Всего к оплате"

    @property
    def total(self):
        if self.kuryer.kuryer_name == "ИТОГО":
            total = 0
            obj = Order.objects.filter(Q(datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)]))
            for i in obj:
                if i.price_partner > 0:
                    obj = i.parent_delevery.split(" ")
                    if obj[0] == "":
                        obj = obj[1:]
                    total += len(obj) + 1
            return total

        else:
            total = 0
            obj = Order.objects.filter(kuryer=self.kuryer.kuryer_name,
                                       datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])

            for i in obj:
                if i.price_partner > 0:
                    obj = i.parent_delevery.split(" ")
                    if obj[0] == "":
                        obj = obj[1:]
                    total += len(obj) + 1
            return total

    total.fget.short_description = "Количество заказов"

    class Meta:
        verbose_name = "Оплата курьерам"
        verbose_name_plural = "Оплата курьерам"

    @property
    def average_time(self):
        if self.kuryer.kuryer_name == "ИТОГО":
            obj = Order.objects.filter(datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            h = 0
            m = 0
            for i in obj:
                if len(i.done_time) > 0:
                    time = i.done_time.split(":")
                    m += int(time[1])
                    if len(time[0]) > 2:
                        a = time[0].split(",")
                        try:
                            h += int(a[1])
                        except:
                            pass
                        a = a[0].split("days")
                        a = a[0].split("day")
                        try:
                            h += (int(a[0]) * 24)
                        except:
                            pass

                    else:
                        h += int(time[0])
            m += h * 60
            try:
                average = m // len(obj)
                av = average % 60
                if len(str(av)) < 2:
                    av = f"0{av}"
            except:
                average = 0
                av = "00"

            return f"{average // 60}:{av}"


        else:
            obj = Order.objects.filter(kuryer=self.kuryer.kuryer_name,
                                       datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            h = 0
            m = 0
            for i in obj:
                if len(i.done_time) > 0:
                    time = i.done_time.split(":")
                    m += int(time[1])
                    if len(time[0]) > 2:
                        a = time[0].split(",")
                        try:
                            h += int(a[1])
                        except:
                            pass
                        a = a[0].split("days")
                        a = a[0].split("day")
                        try:
                            h += (int(a[0]) * 24)
                        except:
                            pass

                    else:
                        h += int(time[0])
            m += h * 60
            try:
                average = m // len(obj)
                av = average % 60
                if len(str(av)) < 2:
                    av = f"0{av}"
            except:
                average = 0
                av = "00"

            return f"{average // 60}:{av}"

    average_time.fget.short_description = "Среднее время доставки"

    @property
    def total_a(self):
        if self.kuryer.kuryer_name == "ИТОГО":
            total_a = 0
            obj = Order.objects.filter(datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                if int(i.price_partner) > 0:
                    total_a += i.type_delever.count("A")
            return total_a

        else:
            total_a = 0
            obj = Order.objects.filter(kuryer=self.kuryer.kuryer_name,
                                       datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                if int(i.price_partner) > 0:
                    total_a += i.type_delever.count("A")
            return total_a

    total_a.fget.short_description = "Количество точка А"

    @property
    def total_1(self):
        if self.kuryer.kuryer_name == "ИТОГО":
            total_b = 0
            obj = Order.objects.filter(datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                if int(i.price_partner) > 0:
                    if "B" in str(i.type_delever1) and int(i.b1) > 0:
                        total_b += 1
                    objk = i.parent_delevery.split(" ")
                    if objk[0] == "":
                        objk = objk[1:]
                    for idd in objk:
                        if "B" in str(Order.objects.get(pk=int(idd)).type_delever1) and int(
                                Order.objects.get(pk=int(idd)).b1) > 0:
                            total_b += 1
            return total_b

        else:
            total_b = 0
            obj = Order.objects.filter(kuryer=self.kuryer.kuryer_name,
                                       datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                if int(i.price_partner) > 0:
                    if "B" in str(i.type_delever1) and int(i.b1) > 0:
                        total_b += 1
                    objk = i.parent_delevery.split(" ")
                    if objk[0] == "":
                        objk = objk[1:]
                    for idd in objk:
                        if "B" in str(Order.objects.get(pk=int(idd)).type_delever1) and int(
                                Order.objects.get(pk=int(idd)).b1) > 0:
                            total_b += 1
            return total_b

    total_1.fget.short_description = "Количество точка B (0.1-5 Кг)"

    @property
    def total_2(self):
        if self.kuryer.kuryer_name == "ИТОГО":
            total_b = 0
            obj = Order.objects.filter(datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                if int(i.price_partner) > 0:
                    if "B" in str(i.type_delever1) and int(i.b2) > 0:
                        total_b += 1
                    objk = i.parent_delevery.split(" ")
                    if objk[0] == "":
                        objk = objk[1:]
                    for idd in objk:
                        if "B" in str(Order.objects.get(pk=int(idd)).type_delever1) and int(
                                Order.objects.get(pk=int(idd)).b2) > 0:
                            total_b += 1
            return total_b

        else:
            total_b = 0
            obj = Order.objects.filter(kuryer=self.kuryer.kuryer_name,
                                       datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                if int(i.price_partner) > 0:
                    if "B" in str(i.type_delever1) and int(i.b2) > 0:
                        total_b += 1
                    objk = i.parent_delevery.split(" ")
                    if objk[0] == "":
                        objk = objk[1:]
                    for idd in objk:
                        if "B" in str(Order.objects.get(pk=int(idd)).type_delever1) and int(
                                Order.objects.get(pk=int(idd)).b2) > 0:
                            total_b += 1
            return total_b

    total_2.fget.short_description = "Количество точка B (5.1-10 Кг)"

    @property
    def total_3(self):
        if self.kuryer.kuryer_name == "ИТОГО":
            total_b = 0
            obj = Order.objects.filter(datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                if int(i.price_partner) > 0:
                    if "B" in str(i.type_delever1) and int(i.b3) > 0:
                        total_b += 1
                    objk = i.parent_delevery.split(" ")
                    if objk[0] == "":
                        objk = objk[1:]
                    for idd in objk:
                        if "B" in str(Order.objects.get(pk=int(idd)).type_delever1) and int(
                                Order.objects.get(pk=int(idd)).b3) > 0:
                            total_b += 1
            return total_b

        else:
            total_b = 0
            obj = Order.objects.filter(kuryer=self.kuryer.kuryer_name,
                                       datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                if int(i.price_partner) > 0:
                    if "B" in str(i.type_delever1) and int(i.b3) > 0:
                        total_b += 1
                    objk = i.parent_delevery.split(" ")
                    if objk[0] == "":
                        objk = objk[1:]
                    for idd in objk:
                        if "B" in str(Order.objects.get(pk=int(idd)).type_delever1) and int(
                                Order.objects.get(pk=int(idd)).b3) > 0:
                            total_b += 1
            return total_b

    total_3.fget.short_description = "Количество точка B (10.1-20 Кг)"

    def __str__(self):
        return f"{self.kuryer} оплата"


class Pay_partner(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="Партнер", null=True, blank=True)
    datetime = models.DateField(verbose_name="Начало период")
    datetime_apply = models.DateField(null=True, verbose_name="Конец период")

    @property
    def total(self):
        if self.partner.partner == "ИТОГО":
            total = 0
            obj = Order.objects.filter(Q(datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)]))
            for i in obj:
                if i.price_partner > 0:
                    obj = i.parent_delevery.split(" ")
                    if obj[0] == "":
                        obj = obj[1:]
                    total += len(obj) + 1
            return total

        else:
            total = 0
            obj = Order.objects.filter(Q(partner=self.partner.partner) &
                                       Q(datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)]))
            for i in obj:
                if i.price_partner > 0:
                    obj = i.parent_delevery.split(" ")
                    if obj[0] == "":
                        obj = obj[1:]
                    total += len(obj) + 1
            return total

    total.fget.short_description = "Количество заказов"

    class Meta:
        verbose_name = "Оплата партнеров"
        verbose_name_plural = "Оплата партнеров"

    @property
    def price(self):
        if self.partner.partner == "ИТОГО":
            total_price = []
            obj = Order.objects.filter(datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                total_price.append(int(i.price_partner))
            return sum(total_price)

        else:
            total_price = []
            obj = Order.objects.filter(partner=self.partner.partner,
                                       datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                total_price.append(int(i.price_partner))
            return sum(total_price)

    price.fget.short_description = "Всего к оплате"

    @property
    def total_a(self):
        if self.partner.partner == "ИТОГО":
            total_a = 0
            obj = Order.objects.filter(datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                if int(i.price_partner) > 0:
                    total_a += i.type_delever.count("A")
            return total_a

        else:
            total_a = 0
            obj = Order.objects.filter(partner=self.partner.partner,
                                       datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                if int(i.price_partner) > 0:
                    total_a += i.type_delever.count("A")
            return total_a

    total_a.fget.short_description = "Количество точка А"

    def __str__(self):
        return f"{self.partner} оплата"

    @property
    def total_1(self):
        if self.partner.partner == "ИТОГО":
            total_b = 0
            obj = Order.objects.filter(datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                if int(i.price_partner) > 0:
                    if "B" in str(i.type_delever1) and int(i.b1) > 0:
                        total_b += 1
                    objk = i.parent_delevery.split(" ")
                    if objk[0] == "":
                        objk = objk[1:]
                    for idd in objk:
                        if "B" in str(Order.objects.get(pk=int(idd)).type_delever1) and int(
                                Order.objects.get(pk=int(idd)).b1) > 0:
                            total_b += 1

            return total_b

        else:
            total_b = 0
            obj = Order.objects.filter(partner=self.partner.partner,
                                       datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                if int(i.price_partner) > 0:
                    if "B" in str(i.type_delever1) and int(i.b1) > 0:
                        total_b += 1
                    objk = i.parent_delevery.split(" ")
                    if objk[0] == "":
                        objk = objk[1:]
                    for idd in objk:
                        if "B" in str(Order.objects.get(pk=int(idd)).type_delever1) and int(Order.objects.get(pk=int(idd)).b1) > 0:
                            total_b += 1

            return total_b

    total_1.fget.short_description = "Количество точка B (0.1-5 Кг)"

    @property
    def total_2(self):
        if self.partner.partner == "ИТОГО":
            total_b = 0
            obj = Order.objects.filter(datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                if int(i.price_partner) > 0:
                    if "B" in str(i.type_delever1) and int(i.b2) > 0:
                        total_b += 1
                    objk = i.parent_delevery.split(" ")
                    if objk[0] == "":
                        objk = objk[1:]
                    for idd in objk:
                        if "B" in str(Order.objects.get(pk=int(idd)).type_delever1) and int(
                                Order.objects.get(pk=int(idd)).b2) > 0:
                            total_b += 1

            return total_b

        else:
            total_b = 0
            obj = Order.objects.filter(partner=self.partner.partner,
                                       datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                if int(i.price_partner) > 0:
                    if "B" in str(i.type_delever1) and int(i.b2) > 0:
                        total_b += 1
                    objk = i.parent_delevery.split(" ")
                    if objk[0] == "":
                        objk = objk[1:]
                    for idd in objk:
                        if "B" in str(Order.objects.get(pk=int(idd)).type_delever1) and int(
                                Order.objects.get(pk=int(idd)).b2) > 0:
                            total_b += 1

            return total_b

    total_2.fget.short_description = "Количество точка B (5.1-10 Кг)"

    @property
    def total_3(self):
        if self.partner.partner == "ИТОГО":
            total_b = 0
            obj = Order.objects.filter(datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                if int(i.price_partner) > 0:
                    if "B" in str(i.type_delever1) and int(i.b3) > 0:
                        total_b += 1
                    objk = i.parent_delevery.split(" ")
                    if objk[0] == "":
                        objk = objk[1:]
                    for idd in objk:
                        if "B" in str(Order.objects.get(pk=int(idd)).type_delever1) and int(
                                Order.objects.get(pk=int(idd)).b3) > 0:
                            total_b += 1
            return total_b

        else:
            total_b = 0
            obj = Order.objects.filter(partner=self.partner.partner,
                                       datetime__range=[self.datetime, self.datetime_apply + timedelta(days=1)])
            for i in obj:
                if int(i.price_partner) > 0:
                    if "B" in str(i.type_delever1) and int(i.b3) > 0:
                        total_b += 1
                    objk = i.parent_delevery.split(" ")
                    if objk[0] == "":
                        objk = objk[1:]
                    for idd in objk:
                        if "B" in str(Order.objects.get(pk=int(idd)).type_delever1) and int(
                                Order.objects.get(pk=int(idd)).b3) > 0:
                            total_b += 1
            return total_b

    total_3.fget.short_description = "Количество точка B (10.1-20 Кг)"


class Customuser(AbstractUser):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="Партнер", null=True, blank=True)
    telegram_id = models.BigIntegerField(verbose_name="Телеграм ID", null=True, blank=True)


bot = Bot(token=NESU_TOKEN)


@receiver(post_save, sender=Order)
def post_save_order(sender, instance, created, *args, **kwargs):
    if created and instance.api:
        kuryer = Kuryer.objects.filter(inwork=True)
        kuryer_group = Kuryer_group.objects.all()
        disp = Dispatcher.objects.all()
        button = []
        for i in range(1, len(kuryer), 2):
            if len(kuryer) > 1:
                button.append([InlineKeyboardButton(f"{kuryer[i - 1].kuryer_name}",
                                                    callback_data=f"{instance.id}_{kuryer[i - 1].id}_kuryer"),
                               InlineKeyboardButton(f"{kuryer[i].kuryer_name}",
                                                    callback_data=f"{instance.id}_{kuryer[i].id}_kuryer")])
        if len(kuryer) % 2 == 1:
            button.append([InlineKeyboardButton(f"{kuryer[len(kuryer) - 1].kuryer_name}",
                                                callback_data=f"{instance.id}_{kuryer[len(kuryer) - 1].id}_kuryer")])
        button.append([InlineKeyboardButton("🔄Обновить",
                                            callback_data=f"{instance.id}_update")])
        button.append([InlineKeyboardButton(f"❌Отменить заказ",
                                            callback_data=f"{instance.id}_cancelapply")])

        for i in kuryer_group:
            bot.send_message(chat_id=i.kuryer_id, parse_mode="HTML", disable_web_page_preview=True,
                             text=f"{inform(instance)}")

        for i in disp:
            bot.send_message(chat_id=i.dispatcher_telegram_id, parse_mode="HTML",
                             disable_web_page_preview=True,
                             text=f"{inform(instance)}\n\nВыберите КУРЬЕР 👇",
                             reply_markup=InlineKeyboardMarkup(button))


@receiver(post_save, sender=Message)
def post_seve_order(sender, instance, created, *args, **kwargs):
    if created:
        operator = Operator.objects.all()
        group = Kuryer_group.objects.all()
        kuryer = Kuryer.objects.all()
        dispatcher = Dispatcher.objects.all()
        if instance.operator:
            for i in operator:
                try:
                    try:
                        bot.send_photo(chat_id=i.telegram_id,
                                       photo=open(f"media/{instance.image}", "rb"), caption=instance.message)
                    except:
                        bot.send_message(chat_id=i.telegram_id,
                                         text=instance.message)
                except:
                    pass

        if instance.kuryer:
            for i in kuryer:
                try:
                    try:
                        bot.send_photo(chat_id=i.kuryer_telegram_id,
                                       photo=open(f"media/{instance.image}", "rb"), caption=instance.message)
                    except:
                        bot.send_message(chat_id=i.kuryer_telegram_id,
                                         text=instance.message)
                except:
                    pass

        if instance.dispatcher:
            for i in dispatcher:
                try:
                    try:
                        bot.send_photo(chat_id=i.dispatcher_telegram_id,
                                       photo=open(f"media/{instance.image}", "rb"), caption=instance.message)
                    except:
                        bot.send_message(chat_id=i.dispatcher_telegram_id,
                                         text=instance.message)
                except:
                    pass

        for i in group:
            try:
                try:
                    bot.send_photo(chat_id=i.kuryer_id,
                                   photo=open(f"media/{instance.image}", "rb"), caption=instance.message)
                except:
                    bot.send_message(chat_id=i.kuryer_id,
                                     text=instance.message)
            except:
                pass
