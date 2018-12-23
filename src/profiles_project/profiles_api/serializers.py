from rest_framework import serializers
from . import models
class HelloSerializer(serializers.Serializer):
    """ Serializes a name field for testing our api"""
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """ A serializer for our user profile object """

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password':{'write_only': True}}

    def create(self, validated_data):
        """ Create a new user """
        user = models.UserProfile(
            email = validated_data['email'],
            name = validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contributor
        fields = ('id', 'name', 'address')
    def create(self, validated_data):
        contributor = models.Contributor.objects.create(**validated_datad)
        contributor.save()
        return contributor
class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """ Profile field serializer """
    user_profile = UserProfileSerializer(read_only = True)
    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on', 'contributors')
        extra_kwargs = {'user_profile': {'read_only': True}}

    


