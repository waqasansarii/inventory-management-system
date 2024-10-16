from rest_framework import serializers
from .models import Category,Product,Supplier,ProductSuppliers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  

class CategorySerializer (serializers.ModelSerializer):
    class Meta :
        model = Category
        fields = ['name','id','description']


# for supplier 
class ProductSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'category']        


class SupplierSerializer (serializers.ModelSerializer):
    products = ProductSupplierSerializer(read_only=True,many=True,source='productsSupplier')
    # product_ids = serializers.ListField(write_only=True,allow_null=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    class Meta :
        model = Supplier
        fields = ['name','id','number','email','products','product_ids']



#// for products serializera
class ProductSupplierThroughSerializer(serializers.ModelSerializer):
    # suppliers = SupplierProductSerializer(read_only=True,many=True)
    class Meta:
        model = ProductSuppliers
        fields = ['quantity','id','createdAt']
        # fields = '__all__'
        
class SupplierProductSerializer (serializers.ModelSerializer):
    suppliers = ProductSupplierThroughSerializer(read_only=True,many=True)
    class Meta:
        model = Supplier
        fields = ['name','id','number','email','suppliers']

#  {
#         "name": "Laptop dell 2",
#         "description": null,
#         "price": 700,
#         "quantity": 4,
#         "suppliers_id": [1,2]
# }
        
            
        
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True,required=False)
    
    suppliers = ProductSupplierThroughSerializer(many=True,read_only=True)
    suppliers_id = serializers.ListField(write_only=True,required=False)
    user = UserSerializer(read_only=True)
    # user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'category','suppliers','category_id','suppliers_id',"user"]        



# for reverse category data 
class ProductCategorySerializer(serializers.ModelSerializer):
    suppliers = SupplierProductSerializer(many=True,read_only=True,source='productsSupplier')
    
    class Meta:
        model= Product
        fields = ['id', 'name', 'description', 'price', 'quantity','suppliers']        
        
    
    
class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductCategorySerializer(read_only=True,many=True,source='productsCategory')
    # products = productsCategory 
    class Meta:
        model= Category
        fields = ['id', 'name', 'description', 'products' ]        
           
           
class SignupSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name= serializers.CharField()
    last_name = serializers.CharField()
    username= serializers.CharField()
    is_superuser = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True) 
    date_joined = serializers.DateTimeField(read_only=True)          
    
class LoginSerializer(serializers.Serializer):
    username= serializers.CharField()
    password = serializers.CharField() 
    # class Meta:
        # models = User
        # fields =['username','password']    