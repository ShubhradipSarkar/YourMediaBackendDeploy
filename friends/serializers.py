from rest_framework import serializers
from friends.models import User,Friends,Posts, Ids , FriendRequests, Likes
class Userserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields="__all__"

class Friendserializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Friends
        fields="__all__"

class FriendRequestserializer(serializers.ModelSerializer):
    
    class Meta:
        model = FriendRequests
        fields="__all__"
        
class Postsserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Posts
        fields='__all__'

class Likesserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Likes
        fields="__all__"

class IdsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ids
        fields=['id', 'name', 'email', 'password']
        extra_kwargs={
            'password':{'write_only': True}
        }

    def create(self, validated_data):
        password=validated_data.pop('password', None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance