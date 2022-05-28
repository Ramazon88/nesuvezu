from datetime import datetime, timezone

import pytz
import requests
from django.db.models import Q
from django.shortcuts import render, redirect
from telegram.ext import CallbackContext

from .models import *
from confcontrol.models import *

start_button = ReplyKeyboardMarkup([[KeyboardButton("🆕Создать заказ")]],
                                   resize_keyboard=True, one_time_keyboard=True)


def start_button_kuryer(user_id):
    button = [[KeyboardButton("Поиск заказа")]]
    try:
        kuryer = Kuryer.objects.get(kuryer_telegram_id=user_id)
    except:
        kuryer = Kuryer.objects.filter(kuryer_telegram_id=user_id)[0]
    if kuryer.inwork:
        button.append([KeyboardButton("🔚Завершить работу")])
    else:
        button.append([KeyboardButton("🔛Начало работы")])
    return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)


back = ReplyKeyboardMarkup([[KeyboardButton("🔙Назад")]],
                           resize_keyboard=True, one_time_keyboard=True)


def timecount():
    a = []
    for i in range(int(datetime.now(pytz.timezone('ASIA/Tashkent')).strftime("%H")) + 2, 21):
        a.append([KeyboardButton(f"{i}:00"), KeyboardButton(f"{i}:30")])
    a.append([KeyboardButton("🔙Назад")])
    return ReplyKeyboardMarkup(a, resize_keyboard=True, one_time_keyboard=True)


def timeto():
    a = []
    for i in range(int(datetime.now(pytz.timezone('ASIA/Tashkent')).strftime("%H")) + 1, 20):
        a.append([KeyboardButton(f"{i}:00")])
    a.append([KeyboardButton("🔙Назад")])
    return ReplyKeyboardMarkup(a, resize_keyboard=True, one_time_keyboard=True)


def timefrom():
    a = []
    for i in range(int(datetime.now(pytz.timezone('ASIA/Tashkent')).strftime("%H")) + 3, 22):
        a.append([KeyboardButton(f"{i}:00")])
    a.append([KeyboardButton("🔙Назад")])
    return ReplyKeyboardMarkup(a, resize_keyboard=True, one_time_keyboard=True)


def ttime():
    a = []
    for i in range(9, 21, 2):
        a.append([KeyboardButton(f"{i}:00"), KeyboardButton(f"{i + 1}:00")])
    a.append([KeyboardButton("🔙Назад")])
    return ReplyKeyboardMarkup(a, resize_keyboard=True, one_time_keyboard=True)


def text(user_id):
    step = Step.objects.get(admin_id=user_id)
    text = ""
    if step.type_delever == "":
        pass
    elif step.type_delever == "A-B-A":
        text += f"<strong>Тип доставка:</strong> {step.type_delever}\n"
    elif step.type_delever == "A-B":
        text += f"<strong>Тип доставка:</strong> {step.type_delever}\n"
    text += "<strong>Товар:</strong> "
    if step.name_model == "":
        text += "(необходимые)\n"
    else:
        text += step.name_model + "\n"
    text += "<strong>Тип приобретения:</strong> "
    if step.type_pay == "":
        text += "(необходимые)\n"
    else:
        text += step.type_pay + "\n"
    text += "<strong>Тип оплаты:</strong> "
    if step.pay == "":
        text += "(необходимые)\n"
    else:
        text += step.pay + "\n"
    if step.price == "":
        pass
    else:
        text += f"<strong>Сумма:</strong> {step.price}\n"
    if step.name_customer == "":
        text += "<strong>Имя клиента:</strong> (необходимые)\n"
    else:
        text += f"<strong>Имя клиента:</strong> {step.name_customer}\n"
    if step.phone_customer == "":
        text += "<strong>Номер клиента:</strong> (необходимые)\n"
    else:
        text += f"<strong>Номер клиента:</strong> {step.phone_customer}\n"
    if step.date_delever == "":
        text += "<strong>Время доставки: </strong>(необходимые)\n"
    else:
        text += f"<strong>Время доставки: </strong>{step.date_delever}\n"
    if step.weight == 0:
        text += "<strong>Вес Товара: </strong>(необходимые)\n"
    elif step.weight <= 5:
        text += "<strong>Вес Товара: </strong>0.1-5 Кг\n"
    elif step.weight <= 10:
        text += "<strong>Вес Товара: </strong>5.1-10 Кг\n"
    elif step.weight <= 20:
        text += "<strong>Вес Товара: </strong>10.1-20 Кг\n"
    if step.to_location == "":
        text += "<strong>Куда доставить:</strong> (необходимые)\n"
    elif step.to_location[:5] == "https":
        text += f"<strong>Куда доставить:</strong> <a href='{step.to_location}'>Локация</a>\n"
    else:
        text += f"<strong>Куда доставить:</strong> {step.to_location}\n"
    if step.from_location == "":
        text += "<strong>Откуда доставить:</strong> (необходимые)\n"
    elif step.from_location[:5] == "https":
        text += f"<strong>Откуда доставить:</strong> <a href='{step.from_location}'>{step.shop}</a>\n"
    else:
        text += f"<strong>Откуда доставить:</strong> {step.from_location}\n"
    if step.comment == "":
        pass
    else:
        text += f"<strong>Комментарии:</strong> {step.comment}\n"
    try:
        text += f"<strong>Партнер:</strong> {Operator.objects.get(telegram_id=user_id).partner}\n"
        text += f"<strong>Оператор:</strong> {Operator.objects.get(telegram_id=user_id).name}"
    except:
        pass
    return text


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


def inline():
    button = [
        [InlineKeyboardButton("Товар", callback_data="model"), InlineKeyboardButton("Тип оплаты", callback_data="pay"),
         InlineKeyboardButton("Имя клиента", callback_data="name")],
        [InlineKeyboardButton("Номер клиента", callback_data="phone"),
         InlineKeyboardButton("Тип приобретения", callback_data="type")],
        [InlineKeyboardButton("Время доставки", callback_data="time"),
         InlineKeyboardButton("Куда доставить", callback_data="to"),
         InlineKeyboardButton("Откуда доставить", callback_data="from")],
        [InlineKeyboardButton("Вес товара", callback_data="weight"),
         InlineKeyboardButton("Комментарии", callback_data="comment")],
        [InlineKeyboardButton("📤Отправить", callback_data="send"),
         InlineKeyboardButton("🏠Главная страница", callback_data="home")]]
    return InlineKeyboardMarkup(button)


def list_admin():
    admin = Operator.objects.all()
    admins = []
    for i in admin:
        admins.append(i.telegram_id)
    return admins


def list_kuryer():
    admin = Kuryer.objects.all()
    admins = []
    for i in admin:
        admins.append(i.kuryer_telegram_id)
    return admins


def list_disp():
    admin = Dispatcher.objects.all()
    admins = []
    for i in admin:
        admins.append(i.dispatcher_telegram_id)
    return admins


def start(update, context):
    user_id = update.message.from_user.id
    admin = list_admin()
    if user_id in admin:
        update.message.delete()
        user_ids = []

        a = Step.objects.all()
        for i in a:
            user_ids.append(i.admin_id)
        if user_id in user_ids:
            Step.objects.filter(admin_id=user_id).update(step=0)
            pass
        else:
            b = Step()
            b.admin_id = user_id
            b.save()
            Step.objects.filter(admin_id=user_id).update(step=0)
        update.message.reply_text("Привет!", reply_markup=start_button)
    elif user_id in list_kuryer():
        update.message.delete()
        user_ids = []

        a = Kuryer_step.objects.all()
        for i in a:
            user_ids.append(i.admin_id)
        if user_id in user_ids:
            Kuryer_step.objects.filter(admin_id=user_id).update(step=0)
            pass
        else:
            b = Kuryer_step()
            b.admin_id = user_id
            b.save()
        update.message.reply_text(f"<i>Ассалому алейкум! <ins><b>{update.message.from_user.first_name}</b></ins></i>\n"
                                  f"<i>Роль: <ins><b>Курьер</b></ins></i>",
                                  reply_markup=start_button_kuryer(user_id), parse_mode="HTML")
    elif user_id in list_disp():
        update.message.delete()
        user_ids = []

        a = Disp_step.objects.all()
        for i in a:
            user_ids.append(i.admin_id)
        if user_id in user_ids:
            Disp_step.objects.filter(admin_id=user_id).update(step=0)
            pass
        else:
            b = Disp_step()
            b.admin_id = user_id
            b.save()
        update.message.reply_text(f"<i>Ассалому алейкум! <ins><b>{update.message.from_user.first_name}</b></ins></i>\n"
                                  f"<i>Роль: <ins><b>Диспетчер</b></ins></i>",
                                  parse_mode="HTML")
    else:
        update.message.delete()
        update.message.reply_text(f"ID: {user_id}")


def order(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    msg = update.message.text
    photo = update.message.photo
    admin = list_admin()
    if user_id in admin:
        step = Step.objects.get(admin_id=user_id)
        msg = update.message.text
        location = update.message.location
        if step.step == 0 and msg == "🆕Создать заказ":
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())
        elif step.step == 0 and location:
            update.message.delete()
            update.message.reply_text(str(location), reply_markup=start_button)
        elif step.step == 1 and msg != "🔙Назад" and msg:
            Step.objects.filter(admin_id=user_id).update(name_model=msg)
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())
        elif step.step == 20 and msg != "🔙Назад" and msg:
            Step.objects.filter(admin_id=user_id).update(type_pay=msg)
            if msg == "Рассрочка":
                Step.objects.filter(admin_id=user_id).update(type_delever="A-B-A", type_delever1="A-B-A")
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())
        elif step.step == 2 and msg == "Наличные" and msg != "🔙Назад":
            Step.objects.filter(admin_id=user_id).update(pay=msg)
            Step.objects.filter(admin_id=user_id).update(step=3)
            update.message.delete()
            update.message.reply_text("Сумма?", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🔙Назад")]],
                                                                                 one_time_keyboard=True,
                                                                                 resize_keyboard=True))

        elif step.step == 2 and (msg == "Payme" or msg == "Apelsin" or msg == "Click") and msg != "🔙Назад":
            Step.objects.filter(admin_id=user_id).update(pay=msg)
            Step.objects.filter(admin_id=user_id).update(type_delever="A-B", type_delever1="A-B")
            Step.objects.filter(admin_id=user_id).update(price="")
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())
        elif step.step == 25 and msg != "🔙Назад" and msg in ["5,1-10 Кг", "0,1-5 Кг", "10,1-20 Кг"]:
            if msg == "5,1-10 Кг":
                Step.objects.filter(admin_id=user_id).update(weight=6)
            elif msg == "0,1-5 Кг":
                Step.objects.filter(admin_id=user_id).update(weight=2)
            elif msg == "10,1-20 Кг":
                Step.objects.filter(admin_id=user_id).update(weight=12)
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())
        elif step.step == 25 and msg != "🔙Назад" and msg not in ["5,1-1 Кг", "0,1-5 Кг", "10,1-20 Кг"]:
            update.message.delete()
            update.message.reply_html(
                text="Введите вес продукта",
                reply_markup=ReplyKeyboardMarkup([[KeyboardButton("0,1-5 Кг"),
                                                   KeyboardButton("5,1-10 Кг")],
                                                  [KeyboardButton(
                                                      "10,1-20 Кг")],
                                                  [KeyboardButton(
                                                      "🔙Назад")]],
                                                 one_time_keyboard=True,
                                                 resize_keyboard=True))

        elif step.step == 2 and msg != "Наличные" and msg != "Payme" and msg != "Apelsin" and msg != "Click" and not msg == "🔙Назад":
            update.message.delete()
            update.message.reply_text("Тип оплаты?", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Payme"),
                                                                                        KeyboardButton("Click"),
                                                                                        KeyboardButton("Apelsin")],
                                                                                       [KeyboardButton("Наличные")],
                                                                                       [KeyboardButton("🔙Назад")]],
                                                                                      one_time_keyboard=True,
                                                                                      resize_keyboard=True))

        elif step.step == 3 and msg == "🔙Назад":
            Step.objects.filter(admin_id=user_id).update(step=2)
            update.message.delete()
            update.message.reply_text("Тип оплаты?", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Payme"),
                                                                                        KeyboardButton("Click"),
                                                                                        KeyboardButton("Apelsin")],
                                                                                       [KeyboardButton("Наличные")],
                                                                                       [KeyboardButton("🔙Назад")]],
                                                                                      one_time_keyboard=True,
                                                                                      resize_keyboard=True))
        elif step.step == 3 and not msg == "🔙Назад" and msg:
            Step.objects.filter(admin_id=user_id).update(price=msg)
            Step.objects.filter(admin_id=user_id).update(type_delever="A-B-A", type_delever1="A-B-A")
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())

        elif step.step == 4 and msg and msg != "🔙Назад":
            Step.objects.filter(admin_id=user_id).update(name_customer=msg)
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())

        elif step.step == 5 and msg and msg != "🔙Назад":
            Step.objects.filter(admin_id=user_id).update(phone_customer=msg)
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())

        elif step.step == 6 and msg == "В течение дня":
            Step.objects.filter(admin_id=user_id).update(date_delever=msg)
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())

        elif step.step == 6 and msg != "В течение дня" and msg != "До скольки" and msg != "Промежуток" and msg != "Завтра" and msg != "🔙Назад":
            update.message.delete()
            update.message.reply_text("Время доставки?( В течение дня | До скольки | Промежуток | Завтра )",
                                      reply_markup=ReplyKeyboardMarkup([[KeyboardButton("В течение дня"),
                                                                         KeyboardButton("До скольки")],
                                                                        [KeyboardButton("Промежуток"),
                                                                         KeyboardButton("Завтра")],
                                                                        [KeyboardButton("🔙Назад")]],
                                                                       one_time_keyboard=True, resize_keyboard=True))

        elif step.step == 6 and msg == "До скольки":
            Step.objects.filter(admin_id=user_id).update(step=7)
            update.message.delete()
            update.message.reply_text("До скольки?", reply_markup=timecount())

        elif step.step == 7 and msg == "🔙Назад" and msg:
            Step.objects.filter(admin_id=user_id).update(step=6)
            update.message.delete()
            update.message.reply_text("Время доставки?",
                                      reply_markup=ReplyKeyboardMarkup([[KeyboardButton("В течение дня"),
                                                                         KeyboardButton("До скольки")],
                                                                        [KeyboardButton("Промежуток"),
                                                                         KeyboardButton("Завтра")],
                                                                        [KeyboardButton("🔙Назад")]],
                                                                       one_time_keyboard=True, resize_keyboard=True))
        elif step.step == 7 and msg and msg != "🔙Назад":
            Step.objects.filter(admin_id=user_id).update(date_delever=f"до {msg}")
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())

        elif step.step == 6 and msg == "Промежуток":
            Step.objects.filter(admin_id=user_id).update(step=8)
            update.message.delete()
            update.message.reply_text("Начало премужутка?", reply_markup=timeto())

        elif step.step == 7 and msg == "🔙Назад":
            Step.objects.filter(admin_id=user_id).update(step=6)
            update.message.delete()
            update.message.reply_text("Время доставки?",
                                      reply_markup=ReplyKeyboardMarkup([[KeyboardButton("В течение дня"),
                                                                         KeyboardButton("До скольки")],
                                                                        [KeyboardButton("Промежуток"),
                                                                         KeyboardButton("Завтра")],
                                                                        [KeyboardButton("🔙Назад")]],
                                                                       one_time_keyboard=True, resize_keyboard=True))

        elif step.step == 8 and msg != "🔙Назад" and msg:
            Step.objects.filter(admin_id=user_id).update(step=9)
            Step.objects.filter(admin_id=user_id).update(date_delever=msg)
            update.message.delete()
            update.message.reply_text("Конец премужутка?", reply_markup=timefrom())

        elif step.step == 9 and msg == "🔙Назад":
            Step.objects.filter(admin_id=user_id).update(step=8)
            Step.objects.filter(admin_id=user_id).update(date_delever="")
            update.message.delete()
            update.message.reply_text("Начало премужутка?", reply_markup=timeto())

        elif step.step == 9 and msg != "🔙Назад" and msg:
            obj = Step.objects.get(admin_id=user_id)
            Step.objects.filter(admin_id=user_id).update(date_delever=f"промежуток {obj.date_delever}-{msg}")
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())

        elif step.step == 6 and msg == "Завтра":
            Step.objects.filter(admin_id=user_id).update(step=10)
            update.message.delete()
            update.message.reply_text("Время доставки?",
                                      reply_markup=ReplyKeyboardMarkup([[KeyboardButton("В течение дня"),
                                                                         KeyboardButton("До скольки")],
                                                                        [KeyboardButton("Промежуток")],
                                                                        [KeyboardButton("🔙Назад")]],
                                                                       one_time_keyboard=True, resize_keyboard=True))
        elif step.step == 10 and msg == "В течение дня":
            Step.objects.filter(admin_id=user_id).update(date_delever="Завтра в течение дня")
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())



        elif step.step == 10 and msg == "🔙Назад":
            Step.objects.filter(admin_id=user_id).update(step=6)
            update.message.delete()
            update.message.reply_text("Время доставки?",
                                      reply_markup=ReplyKeyboardMarkup([[KeyboardButton("В течение дня"),
                                                                         KeyboardButton("До скольки")],
                                                                        [KeyboardButton("Промежуток"),
                                                                         KeyboardButton("Завтра")],
                                                                        [KeyboardButton("🔙Назад")]],
                                                                       one_time_keyboard=True, resize_keyboard=True))

        elif step.step == 10 and msg == "До скольки":
            Step.objects.filter(admin_id=user_id).update(step=11)
            update.message.delete()
            update.message.reply_text("До скольки?", reply_markup=ttime())

        elif step.step == 11 and msg == "🔙Назад":
            Step.objects.filter(admin_id=user_id).update(step=10)
            update.message.delete()
            update.message.reply_text("Время доставки?",
                                      reply_markup=ReplyKeyboardMarkup([[KeyboardButton("В течение дня"),
                                                                         KeyboardButton("До скольки")],
                                                                        [KeyboardButton("Промежуток")],
                                                                        [KeyboardButton("🔙Назад")]],
                                                                       one_time_keyboard=True, resize_keyboard=True))

        elif step.step == 11 and msg and msg != "🔙Назад":
            Step.objects.filter(admin_id=user_id).update(date_delever=f"Завтра до {msg}")
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())

        elif step.step == 10 and msg == "Промежуток":
            Step.objects.filter(admin_id=user_id).update(step=12)
            update.message.delete()
            update.message.reply_text("Начало премужутка?", reply_markup=ttime())

        elif step.step == 12 and msg == "🔙Назад":
            Step.objects.filter(admin_id=user_id).update(step=10)
            update.message.delete()
            update.message.reply_text("Время доставки?",
                                      reply_markup=ReplyKeyboardMarkup([[KeyboardButton("В течение дня"),
                                                                         KeyboardButton("До скольки")],
                                                                        [KeyboardButton("Промежуток")],
                                                                        [KeyboardButton("🔙Назад")]],
                                                                       one_time_keyboard=True, resize_keyboard=True))

        elif step.step == 12 and msg != "🔙Назад" and msg:
            Step.objects.filter(admin_id=user_id).update(step=13)
            Step.objects.filter(admin_id=user_id).update(date_delever=msg)
            update.message.delete()
            update.message.reply_text("Конец премужутка?", reply_markup=ttime())

        elif step.step == 13 and msg == "🔙Назад":
            Step.objects.filter(admin_id=user_id).update(step=12)
            Step.objects.filter(admin_id=user_id).update(date_delever="")
            update.message.delete()
            update.message.reply_text("Начало премужутка?", reply_markup=ttime())

        elif step.step == 13 and msg != "🔙Назад" and msg:
            obj = Step.objects.get(admin_id=user_id)
            Step.objects.filter(admin_id=user_id).update(date_delever=f"Завтра промежуток {obj.date_delever}-{msg}")
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())

        elif step.step == 14 and location:
            Step.objects.filter(admin_id=user_id).update(
                from_location=f"https://yandex.ru/maps/?pt={location['longitude']},{location['latitude']}&z=18&l=map")
            Step.objects.filter(admin_id=user_id).update(shop="Локация")
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())
        elif step.step == 14 and msg and msg != "🔙Назад":
            Step.objects.filter(admin_id=user_id).update(
                from_location=msg)
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())

        elif step.step == 15 and location:
            Step.objects.filter(admin_id=user_id).update(
                to_location=f"https://yandex.ru/maps/?pt={location['longitude']},{location['latitude']}&z=18&l=map")
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())

        elif step.step == 15 and msg and msg != "🔙Назад":
            Step.objects.filter(admin_id=user_id).update(
                to_location=msg)
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())

        elif step.step == 16 and msg and msg != "🔙Назад":
            Step.objects.filter(admin_id=user_id).update(
                comment=msg)
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())
        elif msg == "🔙Назад":
            update.message.delete()
            update.message.reply_html(text(user_id), disable_web_page_preview=True, reply_markup=inline())
    elif user_id in list_kuryer():
        step = Kuryer_step.objects.get(admin_id=user_id)
        if step.step == 0 and msg == "Поиск заказа":
            update.message.delete()
            Kuryer_step.objects.filter(admin_id=user_id).update(step=1)
            update.message.reply_text("Введите номер заказа",
                                      reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🏠Главный страница")]],
                                                                       resize_keyboard=True, one_time_keyboard=True))
        elif step.step == 1 and msg != "🏠Главный страница":
            try:
                obj = Order.objects.get(pk=msg)
                kuryer = Kuryer.objects.get(kuryer_name=obj.kuryer)
                if str(kuryer.kuryer_telegram_id) == str(user_id):
                    if obj.status == "Курьер назначен" or obj.status == "Курьер принял заказ" or obj.status == "Отгуржается" or obj.status == "Доставляется":
                        buttons = InlineKeyboardMarkup(
                            [[InlineKeyboardButton("Принятие", callback_data=f"{obj.id}_prin")]])
                        update.message.reply_text(parse_mode="HTML",
                                                  disable_web_page_preview=True,
                                                  text=inform(obj), reply_markup=buttons)
                    elif obj.status == "Доставка платежа или документ партнеру":
                        buttons = InlineKeyboardMarkup(
                            [[InlineKeyboardButton("✅Я доставил товар покупателю", callback_data=f"{obj.id}_start")]])
                        update.message.reply_text(parse_mode="HTML",
                                                  disable_web_page_preview=True,
                                                  text=inform(obj), reply_markup=buttons)
                    else:
                        update.message.reply_text("🔴Этот заказ завершен")
                else:
                    update.message.reply_text("Этот заказ был передан другому курьеру")
            except:
                update.message.reply_text("🤷‍♂️На этот номер нет заказа")
        elif step.step == 0 and msg == "🔛Начало работы":
            update.message.delete()
            Kuryer_step.objects.filter(admin_id=user_id).update(step=2)
            update.message.reply_text("📎 Сделайте селфи внешнего вида",
                                      reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🏠Главный страница")]],
                                                                       resize_keyboard=True, one_time_keyboard=True))
        elif step.step == 2 and len(photo) > 0:
            update.message.delete()
            try:
                kuryer = Kuryer.objects.get(kuryer_telegram_id=user_id)
            except:
                kuryer = Kuryer.objects.filter(kuryer_telegram_id=user_id)[0]
            group = Kuryer_came_group.objects.all()
            for i in group:
                try:
                    context.bot.send_photo(chat_id=i.kuryer_id, photo=photo[0].file_id,
                                           caption=f"Курьер: {kuryer.kuryer_name}\nКурьер начал работу")
                except:
                    pass
            Kuryer_step.objects.filter(admin_id=user_id).update(step=0)
            Kuryer.objects.filter(kuryer_telegram_id=user_id).update(inwork=True)
            update.message.reply_text(reply_markup=start_button_kuryer(user_id), text="😊Удачи в работе, не уставай")
        elif step.step == 0 and msg == "🔚Завершить работу":
            update.message.delete()
            Kuryer_step.objects.filter(admin_id=user_id).update(step=3)
            update.message.reply_text("Вы подтверждаете, что выполнили свою работу?",
                                      reply_markup=ReplyKeyboardMarkup([[KeyboardButton("✅Подтверждение")],
                                                                        [KeyboardButton("🏠Главный страница")]],
                                                                       resize_keyboard=True, one_time_keyboard=True))
        elif step.step == 3 and msg == "✅Подтверждение":
            update.message.delete()
            Kuryer_step.objects.filter(admin_id=user_id).update(step=0)
            Kuryer.objects.filter(kuryer_telegram_id=user_id).update(inwork=False)
            update.message.reply_text(reply_markup=start_button_kuryer(user_id), text="🥱Хорошего отдыха до завтра")

        elif len(photo) == 0 and Order.objects.get(
                pk=step.obj).step == 0 and step.step == 4 and msg != "🏠Главный страница":
            update.message.delete()
            update.message.reply_text("❗️❗️❗️🤨  Только фото")

        elif len(photo) > 0 and Order.objects.get(pk=step.obj).step == 0 and step.step == 4:
            Order.objects.filter(pk=step.obj).update(before_image=photo[0].file_id)
            obj = Order.objects.get(pk=step.obj)
            update.message.delete()
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("Я отправился", callback_data=f"{obj.id}_go")]])
            update.message.reply_photo(photo=obj.before_image, caption=inform(obj),
                                       reply_markup=buttons, parse_mode="HTML")
            Kuryer_step.objects.filter(admin_id=user_id).update(step=0)
        elif len(photo) == 0 and Order.objects.get(
                pk=step.obj).step == 1 and step.step == 5 and msg != "🏠Главный страница":
            update.message.delete()
            update.message.reply_text("❗️❗️❗️🤨  Только фото")

        elif len(photo) > 0 and Order.objects.get(pk=step.obj).step == 1 and step.step == 5:
            Order.objects.filter(pk=step.obj).update(after_image=photo[0].file_id)
            Kuryer_step.objects.filter(admin_id=user_id).update(step=0)
            obj = Order.objects.get(pk=step.obj)
            try:
                time = datetime.now(timezone.utc) - obj.datetime
                date, _ = str(time).split(".")
                a, b, s = date.split(":")
                Order.objects.filter(pk=obj.id).update(done_time=a + ":" + b)
            except:
                pass
            update.message.delete()
            if obj.type_delever1 == "A-B":
                Order.objects.filter(pk=obj.id).update(status="✅Завершен", step=2)
                disp = Dispatcher.objects.all()
                kuryer_group = Kuryer_group.objects.all()
                for i in disp:
                    context.bot.send_photo(chat_id=i.dispatcher_telegram_id, photo=obj.after_image,
                                           parse_mode="HTML",
                                           caption=f"✅№{obj.id} заказ завершён\nТовар: {obj.name_model}")
                for i in kuryer_group:
                    try:
                        context.bot.send_photo(chat_id=i.kuryer_id, photo=obj.after_image, parse_mode="HTML",
                                               caption=f"✅№{obj.id} заказ завершён\nТовар: {obj.name_model}")
                    except:
                        pass
                try:
                    context.bot.send_photo(chat_id=obj.admin_id,
                                           photo=obj.after_image, parse_mode="HTML",
                                           caption=f"✅№{obj.id} заказ завершён\nТовар: {obj.name_model}")
                except:
                    pass

                update.message.reply_photo(photo=obj.before_image)
                update.message.reply_photo(photo=obj.after_image, parse_mode="HTML",
                                           caption=f"{inform(obj)}")
                update.message.reply_text(text=f"🤙№{obj.id} заказ завершён")
                if obj.api:
                    try:
                        requests.post(url=Partner.objects.get(partner=obj.partner).status_api_url, data={
                            "order_number": obj.id,
                            "status": "Завершен"
                        })
                    except:
                        pass

            else:
                Order.objects.filter(pk=obj.id).update(status="Доставка платежа или документ партнеру", step=2)
                disp = Dispatcher.objects.all()
                kuryer_group = Kuryer_group.objects.all()
                for i in disp:
                    context.bot.send_photo(chat_id=i.dispatcher_telegram_id, photo=obj.after_image,
                                           parse_mode="HTML",
                                           caption=f"✅№{obj.id} заказ доставлен\nТовар: {obj.name_model}\nКурьер доставляет платеж или документ партнеру")
                for i in kuryer_group:
                    try:
                        context.bot.send_photo(chat_id=i.kuryer_id, photo=obj.after_image, parse_mode="HTML",
                                               caption=f"✅№{obj.id} заказ доставлен\nТовар: {obj.name_model}\nКурьер доставляет платеж или документ партнеру")
                    except:
                        pass
                try:
                    context.bot.send_photo(chat_id=obj.admin_id,
                                           photo=obj.after_image, parse_mode="HTML",
                                           caption=f"✅№{obj.id} заказ доставлен\nТовар: {obj.name_model}\nКурьер доставляет оплату или документ")
                except:
                    pass

                update.message.reply_photo(photo=obj.before_image)
                update.message.reply_photo(photo=obj.after_image, parse_mode="HTML",
                                           caption=f"{inform(obj)}",
                                           reply_markup=InlineKeyboardMarkup([[
                                               InlineKeyboardButton("Я доставил платеж или документ партнеру",
                                                                    callback_data=f"{obj.id}_done")]]))
                if obj.api:
                    try:
                        requests.post(url=Partner.objects.get(partner=obj.partner).status_api_url, data={
                            "order_number": obj.id,
                            "status": "Доставка платежа или документ партнеру"
                        })
                    except:
                        pass

        elif msg == "🏠Главный страница":
            update.message.delete()
            Kuryer_step.objects.filter(admin_id=user_id).update(step=0)
            update.message.reply_text(reply_markup=start_button_kuryer(user_id), text="<i>Главный страница</i>",
                                      parse_mode="HTML")


def callback(update: Update, context: CallbackContext):
    user_id = update.callback_query.from_user.id
    data = update.callback_query.data
    datas = data.split("_")
    if data == "model":
        Step.objects.filter(admin_id=user_id).update(step=1)
        update.callback_query.message.delete()
        context.bot.send_message(
            text="Введите название товара",
            chat_id=update.callback_query.message.chat_id, reply_markup=back)
    elif data == "type":
        Step.objects.filter(admin_id=user_id).update(step=20)
        update.callback_query.message.delete()
        context.bot.send_message(
            text="Тип приобретения?",
            chat_id=update.callback_query.message.chat_id,
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Рассрочка"),
                                               KeyboardButton("Покупка")],
                                              [KeyboardButton(
                                                  "🔙Назад")]],
                                             one_time_keyboard=True,
                                             resize_keyboard=True))
    elif data == "weight":
        Step.objects.filter(admin_id=user_id).update(step=25)
        update.callback_query.message.delete()
        context.bot.send_message(
            text="Введите вес продукта",
            chat_id=update.callback_query.message.chat_id,
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("0,1-5 Кг"),
                                               KeyboardButton("5,1-10 Кг")],
                                              [KeyboardButton(
                                                  "10,1-20 Кг")],
                                              [KeyboardButton(
                                                  "🔙Назад")]],
                                             one_time_keyboard=True,
                                             resize_keyboard=True))
    elif data == "pay":
        Step.objects.filter(admin_id=user_id).update(step=2)
        update.callback_query.message.delete()
        context.bot.send_message(
            text="Тип оплаты?",
            chat_id=update.callback_query.message.chat_id, reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Payme"),
                                                                                              KeyboardButton("Click"),
                                                                                              KeyboardButton(
                                                                                                  "Apelsin")],
                                                                                             [KeyboardButton(
                                                                                                 "Наличные")],
                                                                                             [KeyboardButton(
                                                                                                 "🔙Назад")]],
                                                                                            one_time_keyboard=True,
                                                                                            resize_keyboard=True))
    elif data == "name":
        Step.objects.filter(admin_id=user_id).update(step=4)
        update.callback_query.message.delete()
        context.bot.send_message(
            text="Введите имя клиента",
            chat_id=update.callback_query.message.chat_id, reply_markup=back)

    elif data == "phone":
        Step.objects.filter(admin_id=user_id).update(step=5)
        update.callback_query.message.delete()
        context.bot.send_message(
            text="Введите номер телефона клиента",
            chat_id=update.callback_query.message.chat_id, reply_markup=back)

    elif data == "time":
        Step.objects.filter(admin_id=user_id).update(step=6)
        update.callback_query.message.delete()
        context.bot.send_message(
            text="Время доставка",
            chat_id=update.callback_query.message.chat_id,
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("В течение дня"),
                                               KeyboardButton("До скольки")],
                                              [KeyboardButton("Промежуток"),
                                               KeyboardButton("Завтра")],
                                              [KeyboardButton("🔙Назад")]],
                                             one_time_keyboard=True, resize_keyboard=True))
    elif data == "from":
        op = Operator.objects.get(telegram_id=user_id)
        shop = Shop.objects.filter(partner=op.partner)
        button = []
        for i in range(1, len(shop), 2):
            if len(shop) > 1:
                button.append([InlineKeyboardButton(f"{shop[i - 1].shop}", callback_data=f"{shop[i - 1].id}_shops"),
                               InlineKeyboardButton(f"{shop[i].shop}", callback_data=f"{shop[i].id}_shops")])
        if len(shop) % 2 == 1:
            button.append(
                [InlineKeyboardButton(f"{shop[len(shop) - 1].shop}", callback_data=f"{shop[len(shop) - 1].id}_shops")])
        button.append(
            [InlineKeyboardButton(f"📍Другие", callback_data="other"),
             InlineKeyboardButton(f"🔙Назад", callback_data="back")])

        update.callback_query.message.edit_text("Выберите магазин", reply_markup=InlineKeyboardMarkup(button))

    elif len(datas) == 2 and datas[1] == "shops":
        shop = Shop.objects.get(pk=datas[0])
        Step.objects.filter(admin_id=user_id).update(from_location=shop.location)
        Step.objects.filter(admin_id=user_id).update(shop=shop.shop)
        update.callback_query.message.edit_text(text=text(user_id), disable_web_page_preview=True, parse_mode="HTML",
                                                reply_markup=inline())

    elif data == "back":
        update.callback_query.message.edit_text(text=text(user_id), disable_web_page_preview=True, parse_mode="HTML",
                                                reply_markup=inline())

    elif data == "other":
        Step.objects.filter(admin_id=user_id).update(step=14)
        update.callback_query.message.delete()
        context.bot.send_message(
            text="Откуда доставить, отправить местоположение",
            chat_id=update.callback_query.message.chat_id, reply_markup=back)

    elif data == "to":
        Step.objects.filter(admin_id=user_id).update(step=15)
        update.callback_query.message.delete()
        context.bot.send_message(
            text="Куда доставить, отправить местоположение",
            chat_id=update.callback_query.message.chat_id, reply_markup=back)

    elif data == "comment":
        Step.objects.filter(admin_id=user_id).update(step=16)
        update.callback_query.message.delete()
        context.bot.send_message(
            text="Вы можете написать дополнительную информацию",
            chat_id=update.callback_query.message.chat_id, reply_markup=back)

    elif data == "home":
        Step.objects.filter(admin_id=user_id).update(step=0, comment="", shop="", to_location="", from_location="",
                                                     date_delever="", phone_customer="", name_customer="", price="",
                                                     pay="", type_pay="", name_model="", type_delever="")
        update.callback_query.message.delete()
        context.bot.send_message(
            text="Начнем с самого начала!",
            chat_id=update.callback_query.message.chat_id, reply_markup=start_button)

    elif data == "send":
        op = Operator.objects.get(telegram_id=user_id)
        partner = Partner.objects.get(pk=op.partner_id)
        step = Step.objects.get(admin_id=user_id)
        if step.name_model == "" or step.weight == 0 or step.pay == "" or step.type_pay == "" or step.name_customer == "" or step.phone_customer == "" or step.date_delever == "" or step.from_location == "" or step.to_location == "":
            update.callback_query.message.delete()
            context.bot.send_message(
                text=text(user_id) + "\n\n👆 Заполните форму полностью🤨", parse_mode="HTML",
                disable_web_page_preview=True,
                chat_id=update.callback_query.message.chat_id, reply_markup=inline())

        else:
            obj = Order()
            obj.admin_id = step.admin_id
            obj.partner = partner.partner
            obj.admin_name = op.name
            obj.type_delever = step.type_delever
            obj.type_delever1 = step.type_delever1
            obj.name_model = step.name_model
            obj.pay = step.pay
            obj.price = step.price
            obj.name_customer = step.name_customer
            obj.phone_customer = step.phone_customer
            obj.date_delever = step.date_delever
            obj.from_location = step.from_location
            obj.to_location = step.to_location
            obj.shop = step.shop
            obj.weight = step.weight
            obj.comment = step.comment
            obj.type_pay = step.type_pay
            obj.api = False
            try:
                price = Price.objects.all()[0]
                obj.a = price.a
                obj.comis = price.comis
                if step.weight <= 5:
                    obj.b = price.b1
                    obj.b1 = price.b1
                elif step.weight <= 10:
                    obj.b = price.b2
                    obj.b2 = price.b2
                elif step.weight <= 20:
                    obj.b = price.b3
                    obj.b3 = price.b3
            except:
                pass
            obj.save()
            kuryer = Kuryer.objects.filter(inwork=True)
            kuryer_group = Kuryer_group.objects.all()
            disp = Dispatcher.objects.all()
            update.callback_query.message.edit_text(f"{inform(obj)}\n\n✅Заказ отправлен курьеру!", parse_mode="HTML",
                                                    disable_web_page_preview=True)
            context.bot.send_message(
                text="Начнем с самого начала!",
                chat_id=update.callback_query.message.chat_id, reply_markup=start_button)
            button = []
            for i in range(1, len(kuryer), 2):
                if len(kuryer) > 1:
                    button.append([InlineKeyboardButton(f"{kuryer[i - 1].kuryer_name}",
                                                        callback_data=f"{obj.id}_{kuryer[i - 1].id}_kuryer"),
                                   InlineKeyboardButton(f"{kuryer[i].kuryer_name}",
                                                        callback_data=f"{obj.id}_{kuryer[i].id}_kuryer")])
            if len(kuryer) % 2 == 1:
                button.append([InlineKeyboardButton(f"{kuryer[len(kuryer) - 1].kuryer_name}",
                                                    callback_data=f"{obj.id}_{kuryer[len(kuryer) - 1].id}_kuryer")])
            button.append([InlineKeyboardButton("🔄Обновить",
                                                callback_data=f"{obj.id}_update")])
            button.append([InlineKeyboardButton("❌Отменить заказ",
                                                callback_data=f"{obj.id}_cancelapply")])

            for i in kuryer_group:
                try:
                    context.bot.send_message(chat_id=i.kuryer_id, parse_mode="HTML", disable_web_page_preview=True,
                                             text=f"{inform(obj)}")
                except:
                    pass

            for i in disp:
                try:
                    context.bot.send_message(chat_id=i.dispatcher_telegram_id, parse_mode="HTML",
                                             disable_web_page_preview=True,
                                             text=f"{inform(obj)}\n\nВыберите КУРЬЕР 👇",
                                             reply_markup=InlineKeyboardMarkup(button))
                except:
                    pass

            Step.objects.filter(admin_id=user_id).update(step=0, weight=0, comment="", shop="", to_location="",
                                                         from_location="",
                                                         date_delever="", phone_customer="", name_customer="", price="",
                                                         pay="", type_pay="", name_model="", type_delever="")
            update.callback_query.answer(f"№{obj.id} ✅Заказ отправлен курьеру!")
    elif len(datas) == 3 and datas[2] == "kuryer":
        old_obj = Order.objects.get(pk=datas[0])
        kuryer = Kuryer.objects.get(pk=datas[1])
        Order.objects.filter(pk=datas[0]).update(kuryer=kuryer.kuryer_name)
        Order.objects.filter(pk=datas[0]).update(status="Курьер назначен", multiorder="Простой заказ", shop_came=False)
        objk = Order.objects.get(pk=datas[0])
        group = Kuryer_group.objects.all()

        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("Принятие", callback_data=f"{objk.id}_prin")]])
        update.callback_query.message.edit_text(
            text=inform(objk) + "\n" + f'<strong>Курьер:</strong> {kuryer.kuryer_name}',
            parse_mode="HTML", disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔀Переназначить курьера",
                                                                     callback_data=f"{objk.id}_select")],
                                               [InlineKeyboardButton("🔁Возврат товара",
                                                                     callback_data=f"{objk.id}_returnapply")],
                                               [InlineKeyboardButton("❌Отменить заказ",
                                                                     callback_data=f"{objk.id}_cancelapply")]]))
        update.callback_query.message.reply_text(f"✅Заказ №{objk.id} отправлен {kuryer.kuryer_name}!")
        context.bot.send_message(chat_id=kuryer.kuryer_telegram_id, parse_mode="HTML", disable_web_page_preview=True,
                                 text=inform(objk), reply_markup=buttons)
        try:
            obj = Order.objects.filter(
                (Q(status="Курьер назначен") | Q(status="Курьер принял заказ") | Q(status="Отгуржается")) & Q(
                    kuryer=f"{kuryer.kuryer_name}") & Q(from_location=f"{objk.from_location}") & Q(
                    partner=f"{objk.partner}"))
            if len(obj) < 2:
                raise Exception
            else:
                s = 0
                for i in obj:
                    if i.id == objk.id:
                        continue
                    o = objk
                    if (o.type_delever[0] != "A" and s == 0) or s == 0:
                        o.type_delever = o.type_delever1.replace("-B", "-B-B", 1)
                        o.parent_delevery = f"{i.id}"
                    else:
                        o.type_delever = o.type_delever.replace("-B", "-B-B", 1)
                        o.parent_delevery = f"{o.parent_delevery} {i.id}"
                    o.multi = True
                    o.save()
                    if i.type_delever1[-1] == "A" and o.type_delever[-1] != "A":
                        o.type_delever = o.type_delever + "-A"
                        o.save()
                    i.type_delever = "Объединены в мультизаказ"
                    i.parent_delevery = o.id
                    i.multiorder = f"Заказ был объединен 👉№{o.id}"
                    i.multi = True
                    i.save()
                    s += 1
                orders = ""
                for i in obj:
                    orders += f"{i.id}, "
                ords = objk
                ords.multiorder = f"№ {orders} Комбинация Мултизаказов"
                ords.save()
                try:
                    update.callback_query.message.reply_text(f"Заказы №{orders} заменены на мультизаказы")
                    for i in group:
                        context.bot.send_message(chat_id=i.kuryer_id,
                                                 text=f"Заказы №{orders} заменены на мультизаказы")
                    context.bot.send_message(chat_id=objk.admin_id,
                                             text=f"Заказы №{orders} заменены на мультизаказы")
                except:
                    pass
                if old_obj.multi and (
                        old_obj.kuryer != objk.kuryer or old_obj.from_location != objk.from_location or old_obj.shop_came != objk.shop_came):
                    if old_obj.type_delever[0] != "A":
                        b_obj = Order.objects.get(pk=old_obj.parent_delevery)
                        len_ob = b_obj.parent_delevery.split(" ")
                        if len_ob[0] == "":
                            len_ob = len_ob[1:]
                        if len(len_ob) == 1:
                            Order.objects.filter(pk=b_obj.id).update(type_delever=b_obj.type_delever1, multi=False,
                                                                     parent_delevery="", multiorder="Простой заказ")
                        elif len(len_ob) > 1:
                            orders = ""
                            orderss = ""
                            s = 0
                            for i in len_ob:
                                if i == str(old_obj.id):
                                    continue
                                if Order.objects.get(pk=i).type_delever1[-1] == "A":
                                    s += 1
                                orders += " " + i
                                orderss += i + ", "
                            if b_obj.type_delever1[-1] != "A" and s == 0 and b_obj.type_delever[-1] == "A":
                                b_obj.type_delever = b_obj.type_delever.replace("-B-A", "", 1)
                            else:
                                b_obj.type_delever = b_obj.type_delever.replace("-B", "", 1)
                            b_obj.parent_delevery = orders
                            b_obj.multiorder = f"№ {orderss}{b_obj.id} Комбинация Мултизаказов"
                            b_obj.save()
                    elif old_obj.type_delever[0] == "A":
                        len_ob = old_obj.parent_delevery.split(" ")
                        if len_ob[0] == "":
                            len_ob = len_ob[1:]
                        if len(len_ob) == 1:
                            obj = Order.objects.get(pk=len_ob[0])
                            Order.objects.filter(pk=obj.id).update(type_delever=obj.type_delever1, multi=False,
                                                                   parent_delevery="", multiorder="Простой заказ")
                        elif len(len_ob) > 1:
                            orders = ""
                            orderss = ""
                            s = 0
                            for i in len_ob[:len(len_ob) - 1]:
                                orders += i + ", "
                                orderss += " " + i
                                o = Order.objects.get(pk=i)
                                o.parent_delevery = len_ob[-1]
                                o.multiorder = f"Заказ был объединен 👉№{len_ob[-1]}"
                                o.save()
                                if o.type_delever1[-1] == "A":
                                    s += 1
                            last = Order.objects.get(pk=len_ob[-1])

                            if s == 0 and last.type_delever1[-1] != "A" and old_obj.type_delever[-1] == "A":
                                last.type_delever = old_obj.type_delever.replace("-B-A", "")
                            else:
                                last.type_delever = old_obj.type_delever.replace("-B", "", 1)
                            last.multiorder = f"№ {orders}{last.id} Комбинация Мултизаказов"
                            last.parent_delevery = orderss
                            last.save()





        except:
            if objk.multi:
                multi = objk.parent_delevery.split(" ")
                if multi[0] == "":
                    multi = multi[1:]
                # Asosiy buyurtmani o`zgarishi
                if len(multi) > 1 and objk.type_delever[0] == "A":
                    orders = ""
                    orderss = ""
                    s = 0
                    for i in multi[:len(multi) - 1]:
                        orders += i + ", "
                        orderss += " " + i
                        o = Order.objects.get(pk=i)
                        o.parent_delevery = multi[-1]
                        o.multiorder = f"Заказ был объединен 👉№{multi[-1]}"
                        o.save()
                        if o.type_delever1[-1] == "A":
                            s += 1
                    last = Order.objects.get(pk=multi[-1])
                    if s == 0 and last.type_delever1[-1] != "A" and objk.type_delever[-1] == "A":
                        last.type_delever = objk.type_delever.replace("-B-A", "")
                    else:
                        last.type_delever = objk.type_delever.replace("-B", "", 1)
                    last.multiorder = f"№ {orders}{last.id} Комбинация Мултизаказов"
                    last.parent_delevery = orderss
                    last.save()
                # Asosiy emas buyurtmani o`zgarishi
                elif len(multi) == 1 and objk.type_delever[0] != "A":
                    obj = Order.objects.get(pk=multi[0])
                    len_obj = obj.parent_delevery.split(" ")
                    if len_obj[0] == "":
                        len_obj = len_obj[1:]
                    if len(len_obj) > 1:
                        orders = ""
                        orderss = ""
                        s = 0
                        for i in len_obj:
                            if i == str(objk.id):
                                continue
                            orders += i + ", "
                            orderss += " " + i
                            if Order.objects.get(pk=i).type_delever1[-1] == "A":
                                s += 1
                        obj.parent_delevery = orderss
                        obj.multiorder = f"№ {orders} {obj.id} Комбинация Мултизаказов"
                        if s == 0 and obj.type_delever1[-1] != "A" and obj.type_delever[-1] == "A":
                            obj.type_delever = obj.type_delever.replace("-B-A", "")
                        else:
                            obj.type_delever = obj.type_delever.replace("-B", "", 1)

                        obj.save()
                    elif len(len_obj) == 1:
                        obj.type_delever = obj.type_delever1
                        obj.multi = False
                        obj.multiorder = "Простой заказ"
                        obj.parent_delevery = ""
                        obj.save()
                elif len(multi) == 1 and objk.type_delever[0] == "A":
                    obj = Order.objects.get(pk=multi[0])
                    obj.type_delever = obj.type_delever1
                    obj.multi = False
                    obj.multiorder = "Простой заказ"
                    obj.parent_delevery = ""
                    obj.save()

                Order.objects.filter(pk=objk.id).update(type_delever=objk.type_delever1, multi=False,
                                                        parent_delevery="")

        if objk.api:
            try:
                requests.post(url=Partner.objects.get(partner=objk.partner).status_api_url, data={
                    "order_number": objk.id,
                    "status": "Курьер назначен"
                })
            except:
                pass

    elif len(datas) == 2 and datas[1] == "prin":

        objk = Order.objects.get(pk=datas[0])
        if objk.status != "Заказ отменен" and objk.status != "🔁Возврат товара" and objk.status != "✅Завершен":
            if Kuryer.objects.get(kuryer_name=objk.kuryer).kuryer_telegram_id == user_id:
                Order.objects.filter(pk=datas[0]).update(status="Курьер принял заказ")
                buttons = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Я пришел в магазин", callback_data=f"{objk.id}_came")]])
                update.callback_query.message.edit_text(text=inform(objk),
                                                        parse_mode="HTML", disable_web_page_preview=True,
                                                        reply_markup=buttons)
                if objk.api:
                    try:
                        requests.post(url=Partner.objects.get(partner=objk.partner).status_api_url, data={
                            "order_number": objk.id,
                            "status": "Курьер принял заказ"
                        })
                    except:
                        pass

            else:
                update.callback_query.message.delete()
                update.callback_query.answer("Этот заказ был передан другому курьеру")
        else:
            update.callback_query.message.edit_text(f"Заказ <strong>№{objk.id}</strong> уже выполнен",
                                                    parse_mode="HTML")
    elif len(datas) == 2 and datas[1] == "came":
        objk = Order.objects.get(pk=datas[0])
        if objk.status != "Заказ отменен" and objk.status != "🔁Возврат товара" and objk.status != "✅Завершен":
            if Kuryer.objects.get(kuryer_name=objk.kuryer).kuryer_telegram_id == user_id:
                Order.objects.filter(pk=datas[0]).update(status="Отгуржается")
                buttons = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("📸 Сфотографировать", callback_data=f"{objk.id}_image")]])
                update.callback_query.message.edit_text(text=f"{inform(objk)}\n\n👇 Сфотографируйте продукт",
                                                        parse_mode="HTML", disable_web_page_preview=True,
                                                        reply_markup=buttons)
                if objk.api:
                    try:
                        requests.post(url=Partner.objects.get(partner=objk.partner).status_api_url, data={
                            "order_number": objk.id,
                            "status": "Отгуржается"
                        })
                    except:
                        pass
            else:
                update.callback_query.message.delete()
                update.callback_query.answer("Этот заказ был передан другому курьеру")
        else:
            update.callback_query.message.edit_text(f"Заказ <strong>№{objk.id}</strong> уже выполнен",
                                                    parse_mode="HTML")
    elif len(datas) == 2 and datas[1] == "start":
        objk = Order.objects.get(pk=datas[0])
        if objk.status != "Заказ отменен" and objk.status != "🔁Возврат товара" and objk.status != "✅Завершен":
            if Kuryer.objects.get(kuryer_name=objk.kuryer).kuryer_telegram_id == user_id:
                buttons = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("📸 Сфотографировать", callback_data=f"{objk.id}_image2")]])
                update.callback_query.message.edit_reply_markup(reply_markup=buttons)
            else:
                update.callback_query.message.delete()
                update.callback_query.answer("Этот заказ был передан другому курьеру")
        else:
            update.callback_query.message.edit_text(f"Заказ <strong>№{objk.id}</strong> уже выполнен",
                                                    parse_mode="HTML")

    elif len(datas) == 2 and datas[1] == "image":
        objk = Order.objects.get(pk=datas[0])
        if objk.status != "Заказ отменен" and objk.status != "🔁Возврат товара" and objk.status != "✅Завершен":
            if Kuryer.objects.get(kuryer_name=objk.kuryer).kuryer_telegram_id == user_id:
                Kuryer_step.objects.filter(admin_id=user_id).update(step=4, obj=datas[0])
                update.callback_query.message.delete()
                Order.objects.filter(pk=datas[0]).update(step=0)
                context.bot.send_message(chat_id=user_id, text="📎 Сфотографируйте продукт",
                                         reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🏠Главный страница")]],
                                                                          resize_keyboard=True, one_time_keyboard=True))
            else:
                update.callback_query.message.delete()
                update.callback_query.answer("Этот заказ был передан другому курьеру")
        else:
            update.callback_query.message.edit_text(f"Заказ <strong>№{datas[0]}</strong> уже выполнен",
                                                    parse_mode="HTML")


    elif len(datas) == 2 and datas[1] == "image2":
        objk = Order.objects.get(pk=datas[0])
        if objk.status != "Заказ отменен" and objk.status != "🔁Возврат товара" and objk.status != "✅Завершен":
            Kuryer_step.objects.filter(admin_id=user_id).update(step=5, obj=datas[0])
            update.callback_query.message.delete()
            Order.objects.filter(pk=datas[0]).update(step=1)
            context.bot.send_message(chat_id=user_id, text="📎 Сфотографируйте продукт",
                                     reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🏠Главный страница")]],
                                                                      resize_keyboard=True, one_time_keyboard=True))
        else:
            update.callback_query.message.edit_text(f"Заказ <strong>№{datas[0]}</strong> уже выполнен",
                                                    parse_mode="HTML")

    elif len(datas) == 2 and datas[1] == "go":

        objk = Order.objects.get(pk=datas[0])
        if objk.status != "Заказ отменен" and objk.status != "🔁Возврат товара" and objk.status != "✅Завершен":
            if objk.multi:
                if objk.type_delever[-1] == "A":
                    Order.objects.filter(pk=datas[0]).update(status="Доставляется", shop_came=True)
                    len_obj = objk.parent_delevery.split(" ")
                    if len_obj[0] == "":
                        len_obj = len_obj[1:]
                    for i in len_obj:
                        if Order.objects.get(pk=i).status == "Курьер назначен" or Order.objects.get(
                                pk=i).status == "Курьер принял заказ" or Order.objects.get(
                            pk=i).status == "Отгуржается":
                            Order.objects.filter(pk=i).update(status="Доставляется", shop_came=True)
                elif objk.type_delever[-1] != "A":
                    obj = Order.objects.get(pk=objk.parent_delevery)
                    if obj.status == "Курьер принял заказ" or obj.status == "Курьер назначен" or obj.status == "Отгуржается":
                        Order.objects.filter(pk=obj.id).update(status="Доставляется", shop_came=True)
                    len_obj = obj.parent_delevery.split(" ")
                    if len_obj[0] == "":
                        len_obj = len_obj[1:]
                    for i in len_obj:
                        if Order.objects.get(pk=i).status == "Курьер назначен" or Order.objects.get(
                                pk=i).status == "Курьер принял заказ" or Order.objects.get(
                            pk=i).status == "Отгуржается":
                            Order.objects.filter(pk=i).update(status="Доставляется", shop_came=True)
            else:
                Order.objects.filter(pk=datas[0]).update(status="Доставляется", shop_came=True)
            Order.objects.filter(pk=datas[0]).update(delete_message_id=update.callback_query.message.message_id)
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton("✅Я доставил товар покупателю", callback_data=f"{objk.id}_start")]])
            update.callback_query.message.edit_reply_markup(reply_markup=buttons)
            if objk.api:
                try:
                    requests.post(url=Partner.objects.get(partner=objk.partner).status_api_url, data={
                        "order_number": objk.id,
                        "status": "Доставляется"
                    })
                except:
                    pass

        else:
            update.callback_query.message.edit_text(f"Заказ <strong>№{objk.id}</strong> уже выполнен",
                                                    parse_mode="HTML")
    elif len(datas) == 2 and datas[1] == "done":
        objk = Order.objects.get(pk=datas[0])
        if objk.status != "Заказ отменен" and objk.status != "🔁Возврат товара" and objk.status != "✅Завершен":
            disp = Dispatcher.objects.all()
            kuryer_group = Kuryer_group.objects.all()
            if objk.pay == "Наличные":
                Order.objects.filter(pk=datas[0]).update(status="Курьер отправил запрос подтверждения")
                try:
                    context.bot.send_message(chat_id=objk.admin_id,
                                             text=f"✅№{objk.id} заказ Курьер доставил оплату или документ клиента\nТовар: {objk.name_model}\n\n👆🏽 Вы подтверждаете вышеизложенное",
                                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Подтверждение",
                                                                                                      callback_data=f'{datas[0]}_donedone')]]))
                except:
                    pass
                update.callback_query.message.edit_reply_markup()
                if objk.api:
                    try:
                        requests.post(url=Partner.objects.get(partner=objk.partner).status_api_url, data={
                            "order_number": objk.id,
                            "status": "Завершен"
                        })
                    except:
                        pass

            else:
                Order.objects.filter(pk=datas[0]).update(status="✅Завершен")
                try:
                    context.bot.send_message(chat_id=objk.admin_id,
                                             text=f"✅№{objk.id} заказ доставлен Курьер доставил документ клиента\nТовар: {objk.name_model}")
                except:
                    pass
                update.callback_query.message.edit_reply_markup()
                update.callback_query.message.reply_text(text=f"🤙№{objk.id} заказ завершён")
                for i in disp:
                    context.bot.send_message(chat_id=i.dispatcher_telegram_id,
                                             text=f"✅№{objk.id} заказ завершён")
                for i in kuryer_group:
                    try:
                        context.bot.send_message(chat_id=i.kuryer_id,
                                                 text=f"✅№{objk.id} заказ завершён")
                    except:
                        pass
                if objk.api:
                    try:
                        requests.post(url=Partner.objects.get(partner=objk.partner).status_api_url, data={
                            "order_number": objk.id,
                            "status": "Завершен"
                        })
                    except:
                        pass

        else:
            update.callback_query.message.edit_text(f"Заказ <strong>№{objk.id}</strong> уже выполнен",
                                                    parse_mode="HTML")



    elif len(datas) == 2 and datas[1] == "donedone":
        objk = Order.objects.get(pk=datas[0])
        if objk.status != "Заказ отменен" and objk.status != "🔁Возврат товара" and objk.status != "✅Завершен":
            disp = Dispatcher.objects.all()
            kuryer_group = Kuryer_group.objects.all()
            kuryer = Kuryer.objects.get(kuryer_name=objk.kuryer)
            if objk.status != "✅Завершен":
                Order.objects.filter(pk=datas[0]).update(status="✅Завершен")
                for i in disp:
                    context.bot.send_message(chat_id=i.dispatcher_telegram_id,
                                             text=f"✅№{objk.id} заказ завершён")
                for i in kuryer_group:
                    try:
                        context.bot.send_message(chat_id=i.kuryer_id,
                                                 text=f"✅№{objk.id} заказ завершён")
                    except:
                        pass
                context.bot.send_message(chat_id=kuryer.kuryer_telegram_id,
                                         text=f"🤙№{objk.id} заказ завершён")
                update.callback_query.message.edit_text(text=f"✅№{objk.id} заказ завершён")
        else:
            update.callback_query.message.edit_text(f"Заказ <strong>№{objk.id}</strong> уже выполнен",
                                                    parse_mode="HTML")




    elif len(datas) == 2 and datas[1] == "return":
        objk = Order.objects.get(pk=datas[0])
        kuryer = Kuryer.objects.get(kuryer_name=objk.kuryer)
        if objk.status != "Заказ отменен" and objk.status != "🔁Возврат товара" and objk.status != "✅Завершен":
            print("keldi")
            Order.objects.filter(pk=datas[0]).update(status="Вернуть товар", type_delever1="A-B-A")
            try:
                time = datetime.now(timezone.utc) - objk.datetime
                date, _ = str(time).split(".")
                a, b, s = date.split(":")
                Order.objects.filter(pk=objk.id).update(done_time=a + ":" + b)
            except:
                pass
            if objk.multi == False:
                Order.objects.filter(pk=datas[0]).update(type_delever="A-B-A")
            else:
                try:
                    if Order.objects.get(pk=objk.parent_delevery).type_delever[-1] != "A":
                        Order.objects.filter(pk=objk.parent_delevery).update(
                            type_delever=f"{Order.objects.get(pk=objk.parent_delevery).type_delever}-A")
                except:
                    if Order.objects.get(pk=datas[0]).type_delever[-1] != "A":
                        Order.objects.filter(pk=datas[0]).update(
                            type_delever=f"{Order.objects.get(pk=datas[0]).type_delever}-A")

            disp = Dispatcher.objects.all()
            kuryer_group = Kuryer_group.objects.all()

            for i in disp:
                context.bot.send_message(chat_id=i.dispatcher_telegram_id,
                                         text=f"🔁№{objk.id} Курьер возвращает товар")
            for i in kuryer_group:
                try:
                    context.bot.send_message(chat_id=i.kuryer_id,
                                             text=f"🔁№{objk.id} Курьер возвращает товар")
                except:
                    pass
            try:
                context.bot.send_message(chat_id=objk.admin_id,
                                         text=f"🔁№{objk.id} Курьер возвращает товар")
            except:
                pass
            try:
                context.bot.delete_message(chat_id=kuryer.kuryer_telegram_id, message_id=objk.delete_message_id)
            except:
                pass
            update.callback_query.message.edit_reply_markup()
            context.bot.send_message(chat_id=kuryer.kuryer_telegram_id, text=inform(objk), parse_mode="HTML",
                                     disable_web_page_preview=True,
                                     reply_markup=InlineKeyboardMarkup([[
                                         InlineKeyboardButton("Я вернул товар партнеру",
                                                              callback_data=f"{datas[0]}_returndone")]]))
            if objk.api:
                try:
                    requests.post(url=Partner.objects.get(partner=objk.partner).status_api_url, data={
                        "order_number": objk.id,
                        "status": "Вернуть товар"
                    })
                except:
                    pass

        else:
            update.callback_query.answer(f"Заказ №{objk.id} уже выполнен")
            update.callback_query.message.edit_text(f"Заказ <strong>№{objk.id}</strong> уже выполнен",
                                                    parse_mode="HTML")
        # update.callback_query.message.reply_text(text=f"🔁№{objk.id} заказ возврат")

    elif len(datas) == 2 and datas[1] == "returndone":
        objk = Order.objects.get(pk=datas[0])
        if objk.status != "Заказ отменен" and objk.status != "🔁Возврат товара" and objk.status != "✅Завершен":
            Order.objects.filter(pk=datas[0]).update(status="Курьер отправил запрос на возврат")
            try:
                context.bot.send_message(chat_id=objk.admin_id,
                                         text=f"🔁№{objk.id} заказ Курьер вернул товар\nТовар: {objk.name_model}\n\n👆🏽 Вы подтверждаете вышеизложенное",
                                         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Подтверждение",
                                                                                                  callback_data=f'{datas[0]}_donereturn')]]))

            except:
                pass
            update.callback_query.message.edit_reply_markup()
            if objk.api:
                try:
                    requests.post(url=Partner.objects.get(partner=objk.partner).status_api_url, data={
                        "order_number": objk.id,
                        "status": "Возврат товара"
                    })
                except:
                    pass

        else:
            update.callback_query.message.edit_text(f"Заказ <strong>№{objk.id}</strong> уже выполнен")
        # update.callback_query.message.reply_text(text=f"🔁№{objk.id} заказ возврат")

    elif len(datas) == 2 and datas[1] == "donereturn":
        objk = Order.objects.get(pk=datas[0])
        if objk.status != "Заказ отменен" and objk.status != "🔁Возврат товара" and objk.status != "✅Завершен":
            kuryer = Kuryer.objects.get(kuryer_name=objk.kuryer)
            disp = Dispatcher.objects.all()
            kuryer_group = Kuryer_group.objects.all()
            if objk.status != "🔁Возврат товара":
                Order.objects.filter(pk=datas[0]).update(status="🔁Возврат товара")
                for i in disp:
                    context.bot.send_message(chat_id=i.dispatcher_telegram_id,
                                             text=f"🔁№{objk.id} заказ возврат")
                for i in kuryer_group:
                    try:
                        context.bot.send_message(chat_id=i.kuryer_id,
                                                 text=f"🔁№{objk.id} заказ возврат")
                    except:
                        pass
                update.callback_query.message.edit_text(text=f"🔁№{objk.id} заказ возврат")
                context.bot.send_message(chat_id=kuryer.kuryer_telegram_id,
                                         text=f"🔁№{objk.id} заказ возврат")
        else:
            update.callback_query.message.edit_text(f"Заказ <strong>№{objk.id}</strong> уже выполнен")

    elif len(datas) == 2 and datas[1] == "cancel":
        obj = Order.objects.get(pk=datas[0])
        if obj.status == "Заказ оформлен":
            kuryer_group = Kuryer_group.objects.all()
            disp = Dispatcher.objects.all()
            update.callback_query.message.edit_reply_markup()
            for i in kuryer_group:
                try:
                    context.bot.send_message(chat_id=i.kuryer_id, parse_mode="HTML",
                                             text=f"Заказ <strong>№{obj.id}</strong> был ❌отменен диспетчером")
                except:
                    pass

            try:
                update.callback_query.message.edit_text(parse_mode="HTML",
                                                        text=f"Заказ <strong>№{obj.id}</strong> был ❌отменен диспетчером")
            except:
                pass
            try:
                kuryer = Kuryer.objects.get(kuryer_name=obj.kuryer)
                context.bot.send_message(chat_id=kuryer.kuryer_telegram_id, parse_mode="HTML",
                                         text=f"Заказ <strong>№{obj.id}</strong> был ❌отменен диспетчером")
            except:
                pass
            try:
                context.bot.send_message(chat_id=obj.admin_id, parse_mode="HTML",
                                         text=f"Заказ <strong>№{obj.id}</strong> был ❌отменен диспетчером")
            except:
                pass
            if obj.api:
                try:
                    requests.post(url=Partner.objects.get(partner=obj.partner).status_api_url, data={
                        "order_number": obj.id,
                        "status": "Заказ отменен"
                    })
                except:
                    pass
            obj.delete()
        elif obj.status == "Курьер принял заказ" or obj.status == "Отгуржается" or obj.status == "Курьер назначен" or obj.status == "Доставляется":
            Order.objects.filter(pk=datas[0]).update(status="Заказ отменен", type_delever1="A")
            if obj.multi == False:
                Order.objects.filter(pk=datas[0]).update(type_delever="A")
            else:
                multi = obj.parent_delevery.split(" ")
                if multi[0] == "":
                    multi = multi[1:]
                # Asosiy buyurtmani o`zgarishi
                if obj.type_delever[0] == "A":
                    s = 0
                    for i in multi:
                        if Order.objects.get(pk=i).type_delever1[-1] == "A" and len(
                                Order.objects.get(pk=i).type_delever1) > 1:
                            s += 1
                    if s == 0:
                        Order.objects.filter(pk=datas[0]).update(
                            type_delever=Order.objects.get(pk=datas[0]).type_delever.replace("-B", "", 1))
                        Order.objects.filter(pk=datas[0]).update(
                            type_delever=Order.objects.get(pk=datas[0]).type_delever.replace("-A", ""))
                    else:
                        Order.objects.filter(pk=datas[0]).update(type_delever=obj.type_delever.replace("-B", "", 1))
                # Asosiy emas buyurtmani o`zgarishi
                elif obj.type_delever[0] != "A":
                    objk = Order.objects.get(pk=obj.parent_delevery)
                    len_obj = objk.parent_delevery.split(" ")
                    if len_obj[0] == "":
                        len_obj = len_obj[1:]
                    s = 0
                    for i in len_obj:
                        if i == str(obj.id):
                            continue
                        if Order.objects.get(pk=i).type_delever1[-1] == "A" and len(
                                Order.objects.get(pk=i).type_delever1) > 1:
                            s += 1
                    if s == 0 and objk.type_delever1[-1] != "A" and len(
                            Order.objects.get(pk=objk.id).type_delever1) > 1:
                        Order.objects.filter(pk=objk.id).update(
                            type_delever=Order.objects.get(pk=objk.id).type_delever.replace("-B", "", 1))
                        Order.objects.filter(pk=objk.id).update(
                            type_delever=Order.objects.get(pk=objk.id).type_delever.replace("-A", ""))
                    else:
                        Order.objects.filter(pk=objk.id).update(type_delever=objk.type_delever.replace("-B", "", 1))

            kuryer_group = Kuryer_group.objects.all()
            disp = Dispatcher.objects.all()
            update.callback_query.message.edit_reply_markup()
            for i in kuryer_group:
                try:
                    context.bot.send_message(chat_id=i.kuryer_id, parse_mode="HTML",
                                             text=f"Заказ <strong>№{obj.id}</strong> был ❌отменен диспетчером")
                except:
                    pass

            for i in disp:
                try:
                    context.bot.send_message(chat_id=i.dispatcher_telegram_id, parse_mode="HTML",
                                             text=f"Заказ <strong>№{obj.id}</strong> был ❌отменен диспетчером")
                except:
                    pass
            try:
                kuryer = Kuryer.objects.get(kuryer_name=obj.kuryer)
                context.bot.send_message(chat_id=kuryer.kuryer_telegram_id, parse_mode="HTML",
                                         text=f"Заказ <strong>№{obj.id}</strong> был ❌отменен диспетчером")
                context.bot.send_message(chat_id=obj.admin_id, parse_mode="HTML",
                                         text=f"Заказ <strong>№{obj.id}</strong> был ❌отменен диспетчером")
            except:
                pass
            if obj.api:
                try:
                    requests.post(url=Partner.objects.get(partner=obj.partner).status_api_url, data={
                        "order_number": obj.id,
                        "status": "Заказ отменен"
                    })
                except:
                    pass

        else:
            update.callback_query.message.edit_reply_markup()
    elif len(datas) == 2 and datas[1] == "select":
        kuryers = Kuryer.objects.filter(inwork=True)
        obj = Order.objects.get(pk=datas[0])
        if obj.status == "Курьер назначен" or obj.status == "Курьер принял заказ" or obj.status == "Отгуржается" or obj.status == "Доставляется" or obj.status == "Заказ оформлен":
            buttons = []
            if len(kuryers) > 1:
                for i in range(1, len(kuryers), 2):
                    buttons.append([InlineKeyboardButton(f"{kuryers[i - 1].kuryer_name}",
                                                         callback_data=f"{obj.id}_{kuryers[i - 1].id}_kuryer"),
                                    InlineKeyboardButton(f"{kuryers[i].kuryer_name}",
                                                         callback_data=f"{obj.id}_{kuryers[i].id}_kuryer")])
            if len(kuryers) % 2 == 1:
                buttons.append([InlineKeyboardButton(f"{kuryers[len(kuryers) - 1].kuryer_name}",
                                                     callback_data=f"{obj.id}_{kuryers[len(kuryers) - 1].id}_kuryer")])
            buttons.append([InlineKeyboardButton("🔄Обновить",
                                                 callback_data=f"{obj.id}_update")])
            buttons.append([InlineKeyboardButton("🔙Назад",
                                                 callback_data=f"{datas[0]}_nazad")])
            try:
                update.callback_query.message.edit_text(parse_mode="HTML",
                                                        disable_web_page_preview=True,
                                                        text=inform(obj) + f"\n\nВыберите КУРЬЕР 👇",
                                                        reply_markup=InlineKeyboardMarkup(buttons))
            except:
                pass
        else:
            update.callback_query.answer("Товар уже покинул склад")
    elif len(datas) == 2 and datas[1] == "nazad":
        objk = Order.objects.get(pk=datas[0])
        update.callback_query.message.edit_text(
            text=inform(objk) + "\n" + f'<strong>Курьер:</strong> {objk.kuryer}',
            parse_mode="HTML", disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔀Переназначить курьера",
                                                                     callback_data=f"{objk.id}_select")],
                                               [InlineKeyboardButton("🔁Возврат товара",
                                                                     callback_data=f"{objk.id}_returnapply")],
                                               [InlineKeyboardButton("❌Отменить заказ",
                                                                     callback_data=f"{objk.id}_cancelapply")]]))
    elif len(datas) == 2 and datas[1] == "returnapply":
        objk = Order.objects.get(pk=datas[0])
        update.callback_query.message.edit_text(
            text=inform(
                objk) + "\n" + f'<strong>Курьер:</strong> {objk.kuryer}' + "\n\n" + "Вы действительно хотите вернуть заказ? 👇",
            parse_mode="HTML", disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅Да",
                                                                     callback_data=f"{objk.id}_return")],
                                               [InlineKeyboardButton("🔙Назад",
                                                                     callback_data=f"{objk.id}_nazad")]]))
    elif len(datas) == 2 and datas[1] == "cancelapply":
        objk = Order.objects.get(pk=datas[0])
        update.callback_query.message.edit_text(
            text=inform(
                objk) + "\n" + f'<strong>Курьер:</strong> {objk.kuryer}' + "\n\n" + "Вы действительно хотите отменить заказ? 👇",
            parse_mode="HTML", disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅Да",
                                                                     callback_data=f"{objk.id}_cancel")],
                                               [InlineKeyboardButton("🔙Назад",
                                                                     callback_data=f"{objk.id}_nazad")]]))
    elif len(datas) == 2 and datas[1] == "update":
        kuryers = Kuryer.objects.filter(inwork=True)
        obj = Order.objects.get(pk=datas[0])
        buttons = []
        if len(kuryers) > 1:
            for i in range(1, len(kuryers), 2):
                buttons.append([InlineKeyboardButton(f"{kuryers[i - 1].kuryer_name}",
                                                     callback_data=f"{obj.id}_{kuryers[i - 1].id}_kuryer"),
                                InlineKeyboardButton(f"{kuryers[i].kuryer_name}",
                                                     callback_data=f"{obj.id}_{kuryers[i].id}_kuryer")])
        if len(kuryers) % 2 == 1:
            buttons.append([InlineKeyboardButton(f"{kuryers[len(kuryers) - 1].kuryer_name}",
                                                 callback_data=f"{obj.id}_{kuryers[len(kuryers) - 1].id}_kuryer")])
        buttons.append([InlineKeyboardButton("🔄Обновить",
                                             callback_data=f"{obj.id}_update")])
        buttons.append([InlineKeyboardButton("❌Отменить заказ",
                                             callback_data=f"{obj.id}_cancelapply")])
        try:
            update.callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
        except:
            pass


def index(request):
    root = Order()
    if request.POST:
        if request.POST["pay"] == "Наличные":
            root.type_delever = "A-B-A"
            root.type_delever1 = "A-B-A"
        elif request.POST["pay"] != "Наличные":
            if request.POST["type_pay"] == "Рассрочка":
                root.type_delever = "A-B-A"
                root.type_delever1 = "A-B-A"
            else:
                root.type_delever = "A-B"
                root.type_delever1 = "A-B"
        root.price = request.POST.get("price")
        root.to_location = request.POST.get("to_location")
        root.from_location = request.POST.get("from_location")
        root.name_model = request.POST.get("name_model")
        root.name_customer = request.POST.get("name_customer")
        root.phone_customer = request.POST.get("phone_customer")
        root.type_pay = request.POST.get("type_pay")
        root.pay = request.POST.get("pay")
        root.shop = request.POST.get("shop")
        root.comment = request.POST.get("comment")
        root.date_delever = request.POST.get("date_delever")
        root.admin_id = request.user.telegram_id
        root.partner = request.user.partner.partner
        root.admin_name = request.user.first_name
        root.weight = int(request.POST.get("weight"))
        root.api = True
        try:
            price = Price.objects.all()[0]
            root.a = price.a
            root.b = price.b
            root.comis = price.comis
        except:
            pass

        try:
            price = Price.objects.all()[0]
            root.a = price.a
            root.comis = price.comis
            if int(request.POST.get("weight")) <= 5:
                root.b = price.b1
                root.b1 = price.b1
            elif int(request.POST.get("weight")) <= 10:
                root.b = price.b2
                root.b2 = price.b2
            else:
                root.b = price.b3
                root.b3 = price.b3
        except:
            print("xato")
        root.save()
        return redirect("/admin/nesu/order/")
    return render(request, "index.html")
