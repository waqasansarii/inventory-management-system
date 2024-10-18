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
class SupplierProductSerializer (serializers.ModelSerializer):

    class Meta:
        model = Supplier
        # fields = '__all__'
        fields = ['name','number','email']


 
class ProductSupplierThroughSerializer(serializers.ModelSerializer):
    supplier = SupplierProductSerializer(read_only=True)

    class Meta:
        model = ProductSuppliers
        fields = ['supply','supplier']
        # fields = '__all__'
       
            
        
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True,required=False)
    
    suppliers = ProductSupplierThroughSerializer(many=True,read_only=True,source='productsuppliers_set')
    suppliers_id = serializers.ListField(write_only=True,required=False)
    # supply = serializers.IntegerField(required=False,write_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'category','category_id','suppliers_id','suppliers',"user"]        



# for reverse category data 
class ProductCategorySerializer(serializers.ModelSerializer):
    suppliers = SupplierProductSerializer(many=True,read_only=True,source='productsSupplier')
    
    class Meta:
        model= Product
        fields = ['id', 'name', 'description', 'price', 'quantity','suppliers']        
        
    
    
class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductCategorySerializer(read_only=True,many=True,source='productsCategory')
    class Meta:
        model= Category
        fields = ['id', 'name', 'description', 'products' ]        
           
      
      
# auth serializer            
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
