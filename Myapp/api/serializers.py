from Myapp.models import Profile, Blog, Comment, Categroy
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source = 'author.username')
    class Meta:
        model = Profile
        fields = "__all__"
        

    def update(self, instance, validated_data):
        user = self.context['request'].user
    
        if user.profile.pk != instance.pk:
            raise serializers.ValidationError("You don't have permission to update this profile!")

        newInstance = Profile(**validated_data)
        newInstance.id = instance.id
        newInstance.save()

        return newInstance        

class UserCreateSerializer(serializers.HyperlinkedModelSerializer):
    password2 = serializers.CharField(style = {'input_type':'password'}, write_only = True)
    email = serializers.EmailField(validators= [UniqueValidator(User.objects.all())],required = True)


    class Meta:
        model = User
        fields = ['url','pk', 'username','first_name','last_name','email', 'password','password2']

        extra_kwargs = {
            'password':{'write_only':True},
            'first_name':{'required':True},
            'last_name':{'required':True}
        }

    def validate(self, validated_data):
        user = self.context['request'].user
        if validated_data['password'] != validated_data['password2']:
            raise serializers.ValidationError({'password':"Password must match!"})    
        elif not any(c.isupper() for c in validated_data['password']):
            raise serializers.ValidationError({'password':"must contain atleast one capital letter!"})
        return validated_data


    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk = user.pk).filter(email = value).exists():
            raise serializers.ValidationError("email address already taken!")
        return value    

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email= validated_data['email'],
            first_name= validated_data['first_name'],
            last_name = validated_data['last_name']
        )    
        user.set_password(validated_data['password'])
        user.save()
        
        return user

    
    
class UserUpdateSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(validators= [UniqueValidator(User.objects.all())],
                                required = True,
                            )
    profile = UserProfileSerializer(read_only = True)                     
    class Meta:
        model = User
        fields = ['url','profile','username','first_name','last_name','email']

        extra_kwargs = {
            'first_name':{'required':True},
            'last_name':{'required':True}
        }


    def update(self, instance, validated_data):
        user = self.context['request'].user
        
        if user.pk != instance.pk:
            raise serializers.ValidationError("You don't have permission to update this user!")

        instance.username = validated_data.get('username')
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.email = validated_data.get('email')
        instance.save()    

        return instance
        
class CategroySerializer(serializers.HyperlinkedModelSerializer):
    blogs = serializers.HyperlinkedRelatedField(
                                        many = True,
                                        read_only= True,
                                        view_name = 'blog-detail'
                                    )
    class Meta:
        model = Categroy
        fields = '__all__'


class BlogSerializer(serializers.HyperlinkedModelSerializer):
    comments = serializers.HyperlinkedRelatedField(
                                        many = True,
                                        read_only= True,
                                        view_name = 'comment-detail'
                                    )
    categroy = serializers.SlugRelatedField(queryset = Categroy.objects.all(), slug_field = 'name')
    likes = serializers.StringRelatedField(many = True, read_only = True)
    author = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = Blog
        fields = ['url','title','desc','author', 'categroy','date', 'likes','comments']

    def update(self, instance, validated_data):
        user = self.context['request'].user
    
        if user.blog.pk != instance.pk:
            raise serializers.ValidationError("You don't have permission to update this blog!")

        newInstance = Blog(**validated_data)
        newInstance.id = instance.id
        newInstance.save()

        return newInstance    

    

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.StringRelatedField(read_only = True)

    class Meta:
        model = Comment
        fields = ['url','author','blog','content','created']
    

class CommentDetailsSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.StringRelatedField(read_only = True)
    blog = serializers.StringRelatedField(read_only = True)

    class Meta:
        model = Comment
        fields = ['url','author','blog','content','created']

    def update(self, instance, validated_data):
        user = self.context['request'].user
    
        if user.comment.pk != instance.pk:
            raise serializers.ValidationError("You don't have permission to update this comment!")

        newInstance = Comment(**validated_data)
        newInstance.id = instance.id
        newInstance.save()

        return newInstance    
                     
                