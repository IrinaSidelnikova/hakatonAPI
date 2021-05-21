from rest_framework import serializers

from products.models import Sections, Brand, Product, Recall


class SectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sections
        fields = ('title',)

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('title', 'slug',)


class ProductListSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='slug')

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['brands'] = BrandSerializer(instance.brand, context=self.context).data
        representation['recalls'] = RecallSerializer(instance.recalls.all(), many=True).data
        representation['orders_count'] = instance.orders.count()
        return representation


class RecallSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Recall
        fields = ('user', 'product', 'text', 'created_time')


    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        recall = Recall.objects.create(user=user, **validated_data)
        return recall
