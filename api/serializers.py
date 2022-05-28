from rest_framework import serializers

from nesu.models import *


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("a", "b", "b1", "b2", "b3", "comis",
        "partner", "admin_id", "admin_name", "api", "type_delever", "type_delever1", "name_model", "pay", "price", "name_customer",
        "phone_customer", "date_delever", "from_location", "to_location", "shop", "comment", "type_pay", "weight")


class UpdateSerializers(serializers.Serializer):
    class Meta:
        id = serializers.IntegerField()
        cause = serializers.TimeField()

class UpdateDoneSerializers(serializers.Serializer):
    class Meta:
        id = serializers.IntegerField()
        status = serializers.TimeField()