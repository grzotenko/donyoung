from rest_framework import serializers
from .models import FooterPartners, FooterContacts, Main, SocialNet, HeaderOrganizers, HeaderMenu
class MainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Main
        fields = ['banner', 'logo','copyright']

class HeaderMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderMenu
        fields = ['id', 'title', 'path']
class FooterPartnersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FooterPartners
        fields = ['id', 'url']


class FooterContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterContacts
        fields = ['title', 'phone', 'email', 'address', 'map']
class HeaderOrganizersSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderOrganizers
        fields = ['id', 'url', 'image']

class SocialNetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNet
        fields = ['vk', 'instagram', 'youtube', 'facebook']

class CommonSerializer(serializers.Serializer):
    main =  MainSerializer()
    menu = HeaderMenuSerializer(many=True)
    organizers = HeaderOrganizersSerializer(many=True)
    social = SocialNetSerializer()
    partners = FooterPartnersSerializer(many=True)
    contacts = FooterContactsSerializer()
    massMedia = FooterContactsSerializer()

