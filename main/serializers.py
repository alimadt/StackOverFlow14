from rest_framework import serializers

from .models import Problem, CodeImage


class CodeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeImage
        fields = ('image',)

    def _get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            url = obj.image.url
            return 'http://localhost:8000' + url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(instance.images.all())
        representation['images'] = CodeImageSerializer(instance.images.all(),
                                                       many=True).data
        return representation

class ProblemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        exclude = ('author',)

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        author = request.user
        problem = Problem.objects.create(author=author, **validated_data)
        for image in images_data.getlist('images'):
            CodeImage.objects.create(image=image,
                                     problem=problem)
        return problem

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = CodeImageSerializer(instance.images.all(),
                                                       many=True).data
        return representation