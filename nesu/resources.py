from import_export import resources
from import_export.fields import Field

from .models import Order

class OrderResource(resources.ModelResource):
    id = Field(attribute="id", column_name="НОМЕР ЗАКАЗ")
    partner = Field(attribute="partner", column_name="Партнер")
    admin_name = Field(attribute="admin_name", column_name="Имя оператора")
    datetime = Field(attribute="datetime", column_name="Дата")
    done_time = Field(attribute="done_time", column_name="Время завершение доставки")
    type_delever = Field(attribute="type_delever", column_name="ТИП ДОСТАВКА")
    name_model = Field(attribute="name_model", column_name="Наименование товара")
    pay = Field(attribute="pay", column_name="ТИП ОПЛАТЫ")
    type_pay = Field(attribute="type_pay", column_name="ТИП ПРИОБРЕТЕНИЯ")
    price = Field(attribute="price", column_name="Сумма")
    name_customer = Field(attribute="name_customer", column_name="Имя клиента")
    phone_customer = Field(attribute="name_customer", column_name="Телефонный номер")
    date_delever = Field(attribute="date_delever", column_name="Срок поставки")
    shop = Field(attribute="shop", column_name="Магазин")
    status = Field(attribute="status", column_name="Статус")
    kuryer = Field(attribute="kuryer", column_name="Курьер")
    from_location = Field(attribute="from_location", column_name="Откуда забрать")
    to_location = Field(attribute="to_location", column_name="Куда доставить")
    multiorder = Field(attribute="multiorder", column_name="Мултизаказ")
    dis_comment = Field(attribute="dis_comment", column_name="Примечание")
    a = Field(attribute="a", column_name="Цена пункта A")
    b = Field(attribute="b", column_name="Цена пункта B")
    weight = Field(attribute="weight", column_name="Масса")
    price_partner = Field(attribute="price_partner", column_name="Оплата партнера")


    class Meta:
        model = Order
        exclude = ('admin_id', 'comment', 'active', "step", "delete_message_id", "shop_came", "parent_delevery",
                   "after_image", "before_image", "api", "multi", "comis", "type_delever1", "b1", "b2", "b3")