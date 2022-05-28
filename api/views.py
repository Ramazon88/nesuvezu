
from rest_framework.views import APIView
from nesu.models import *
from confcontrol.models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
                Update, Bot
bott = Bot(token=NESU_TOKEN)
class PostCreateApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            a = request.data["weight"]
        except:
            request.data["weight"] = 1
        try:
            price = Price.objects.all()[0]
            request.data["a"] = price.a
            request.data["comis"] = price.comis
            if int(request.data["weight"]) <= 5:
                request.data["b"] = price.b1
                request.data["b1"] = price.b1
            elif int(request.data["weight"]) <= 10:
                request.data["b"] = price.b2
                request.data["b2"] = price.b2
            else:
                request.data["b"] = price.b3
                request.data["b3"] = price.b3
        except:
            pass
        try:
            a = request.data["admin_name"]
        except:
            request.data["admin_name"] = request.user.first_name
        request.data["admin_id"] = request.user.telegram_id
        request.data["partner"] = request.user.partner.partner
        request.data["api"] = True

        try:
            if request.data["pay"] == "Наличные":
                request.data["type_delever"] = "A-B-A"
                request.data["type_delever1"] = "A-B-A"
                a = request.data["price"]
            elif request.data["pay"] != "Наличные":
                if request.data["type_pay"] == "Рассрочка":
                    request.data["type_delever"] = "A-B-A"
                    request.data["type_delever1"] = "A-B-A"
                else:
                    request.data["type_delever"] = "A-B"
                    request.data["type_delever1"] = "A-B"
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        order = PostSerializers(data=request.data)
        data = {}
        if order.is_valid():
            obj = order.save()
            data["id"] = obj.id
            data["status"] = "Заказ оформлен"
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(order.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateApi(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        order = UpdateSerializers(data=request.data)
        if order.is_valid():
            try:
                if request.user.first_name != Order.objects.get(pk=request.data["id"]).admin_name:
                    data = {'error': 'Permission error'}
                    return Response(status=status.HTTP_403_FORBIDDEN, data=data)
            except:
                data = {'error': 'Wrong ID'}
                return Response(status=status.HTTP_403_FORBIDDEN, data=data)

            if len(request.data) != 2:
                data = {'error': 'Bad request'}
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
            try:
                a = request.data["id"]
                b = request.data["cause"]
            except:
                data = {'error': 'Bad request'}
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
            if Order.objects.get(pk=request.data["id"]).status == "Заказ оформлен":
                obj = Order.objects.get(pk=request.data["id"])
            else:
                data = {"error": "Order already finished"}
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
            obj.delete()
            kuryer_group = Kuryer_group.objects.all()
            disp = Dispatcher.objects.all()
            for i in kuryer_group:
                try:
                    bott.send_message(chat_id=i.kuryer_id, parse_mode="HTML",
                                     text=f"Заказ <strong>{request.data['id']}</strong> был отменен партнером \nПричина: <strong>{request.data['cause']}</strong>")
                except:
                    pass

            for i in disp:
                try:
                    bott.send_message(chat_id=i.dispatcher_telegram_id, parse_mode="HTML",
                                     text=f"Заказ <strong>№{request.data['id']}</strong> был отменен партнером \nПричина: <strong>{request.data['cause']}</strong>")
                except:
                    pass
            data = {'ok': 'ok'}
            return Response(status=status.HTTP_200_OK, data=data)
        data = {'error': 'Bad request'}
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data)

class UpdateApiDone(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        order = UpdateDoneSerializers(data=request.data)
        if order.is_valid():
            bott.send_message(chat_id=254118850,
                              text=f"1--{str(request.data)}")
            try:
                if request.user.partner.partner != Order.objects.get(pk=request.data["id"]).partner:
                    data = {'error': 'Permission error'}
                    return Response(status=status.HTTP_403_FORBIDDEN, data=data)
            except:
                data = {'error': 'Wrong ID'}
                return Response(status=status.HTTP_403_FORBIDDEN, data=data)

            if len(request.data) != 2:
                data = {'error': 'Bad request'}
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
            try:
                a = request.data["id"]
                b = request.data["status"]
            except:
                data = {'error': 'Bad request'}
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
            if Order.objects.get(pk=request.data["id"]).status != "✅Завершен" and Order.objects.get(pk=request.data["id"]).status != "🔁Возврат товара":
                bott.send_message(chat_id=254118850,
                                  text=f"2--{str(request.data)}")
                obj = Order.objects.get(pk=request.data["id"])
                kuryer_group = Kuryer_group.objects.all()
                disp = Dispatcher.objects.all()
                kuryer = Kuryer.objects.get(kuryer_name=obj.kuryer)
                if request.data["status"] == "returned":
                    Order.objects.filter(pk=request.data["id"]).update(status="🔁Возврат товара")
                    for i in kuryer_group:
                        try:
                            bott.send_message(chat_id=i.kuryer_id,
                                              text=f"🔁№{obj.id} заказ возврат")
                        except:
                            pass

                    for i in disp:
                        try:
                            bott.send_message(chat_id=i.dispatcher_telegram_id,
                                              text=f"🔁№{obj.id} заказ возврат")
                        except:
                            pass
                    try:
                        bott.send_message(chat_id=obj.admin_id,
                                          text=f"🔁№{obj.id} заказ возврат")
                    except:
                        pass
                    try:
                        bott.send_message(chat_id=kuryer.kuryer_telegram_id,
                                          text=f"🔁№{obj.id} заказ возврат")
                    except:
                        pass
                    data = {'ok': 'ok',
                            "status": "returned"}
                    return Response(status=status.HTTP_200_OK, data=data)
                elif request.data["status"] == "completed":
                    Order.objects.filter(pk=request.data["id"]).update(status="✅Завершен")
                    for i in kuryer_group:
                        try:
                            bott.send_message(chat_id=i.kuryer_id,
                                              text=f"✅№{obj.id} заказ завершён")
                        except:
                            pass

                    for i in disp:
                        try:
                            bott.send_message(chat_id=i.dispatcher_telegram_id,
                                              text=f"✅№{obj.id} заказ завершён")
                        except:
                            pass
                    try:
                        bott.send_message(chat_id=obj.admin_id,
                                          text=f"✅№{obj.id} заказ завершён")
                    except:
                        pass
                    try:
                        bott.send_message(chat_id=kuryer.kuryer_telegram_id,
                                          text=f"🤙№{obj.id} заказ завершён")
                    except:
                        pass
                    data = {'ok': 'ok',
                            "status": "completed"}
                    return Response(status=status.HTTP_200_OK, data=data)
            else:
                data = {"error": "Order already finished"}
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data)

        data = {'error': 'Bad request'}
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data)




