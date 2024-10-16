from django.db.models import Count,Q,Sum,Avg
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Product,Category,Supplier,ProductSuppliers
from ..serializer import ProductSerializer,SupplierProductSerializer

fields = ['name','description','price','quantity']
filter_fields = ['name','category','suppliers']

@api_view(['GET','POST'])
def get_create_products(req:Request):
    pass
    if req.method =='GET':
        params = req.query_params
        filter_val ={}
        for field in filter_fields:
            param = params.get(field)
            if param is not None:
                if field == 'name':
                    filter_val[f'{field}__icontains'] = param
                if field =='suppliers':
                    filter_val[f'{field}__in'] = param.split(',')  
                if field=='category':    
                    filter_val[f'{field}'] = param
        try:
                
            product = Product.objects.select_related('category').prefetch_related('suppliers').filter(**filter_val).all()
            data = ProductSerializer(product,many=True)
            return Response(data.data,status.HTTP_200_OK)
        except ValueError:
            return Response({"msg":'Product not found'},status.HTTP_400_BAD_REQUEST)
        
    
    if req.method=='POST':
        print(req.data)
        serializer = ProductSerializer(data=req.data)
        if serializer.is_valid():

            suppliers_id = serializer.validated_data.pop('suppliers_id',[])
            # print(suppliers_id)
            serializer.validated_data['user_id'] = req.user.id
       
            is_suppliers = Supplier.objects.filter(id__in=suppliers_id)

            print('is supplier',len(is_suppliers),suppliers_id)
            if len(is_suppliers) >=1 :
                products = Product.objects.create(**serializer.validated_data)
            else:
                return Response({"detail":"Supplier does not exists"},status.HTTP_400_BAD_REQUEST)
                    
            if suppliers_id is not None or len(is_suppliers) >= 1:
                for supplier in is_suppliers:
                    ProductSuppliers.objects.create(product=products, supplier=supplier,quantity=30)  # Adjust the quantity as needed

                # products.suppliers.set(suppliers_id)f
            return Response({"data":serializer.validated_data,"details":'Products created'},status.HTTP_201_CREATED)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET',"PUT",'DELETE'])
def get_update_delete_product(req:Request,id):
        try:
           pk = int(id)
        except ValueError:
           return Response({'detail': 'ID should be an integer.'}, status=status.HTTP_400_BAD_REQUEST)
       
        try:
            product = Product.objects.select_related('category').prefetch_related('suppliers').get(id=pk)
            if req.method =='GET':
                data = ProductSerializer(product)
                return Response(data.data,status.HTTP_200_OK)
        
            #  updating category here 
            if req.method=='PUT':
                for field in fields:
                    val = req.data.get(field)
                    if val is not None:
                        setattr(product,field,val)
                category = req.data.get('category')
                suppliers = req.data.get('suppliers')
    
                if category is not None:
                    try:
                        category = Category.objects.get(id=category)  
                        product.category = category  
                    except Category.DoesNotExist:
                        return Response({'error': 'Category not found'}, status=status.HTTP_400_BAD_REQUEST)
 
                if suppliers is not None:
                    try:
                        supplier = Supplier.objects.filter(id__in=req.data.get('suppliers'))  
                         
                    except Supplier.DoesNotExist:
                        return Response({'error': 'Supplier not found'}, status=status.HTTP_400_BAD_REQUEST)

                    # product.suppliers = supplier  
                
                if req.data is not None:
                    product.save() 
                    product.suppliers.set(supplier)
                    return Response({"name":product.name,"description":product.description}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"details":"enter name or description"}, status=status.HTTP_400_BAD_REQUEST)
            
            if req.method=='DELETE':
                product.delete()
                return Response({"data":'Product deleted'},status.HTTP_200_OK)
        # throw an error if product does not exist 
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)   


@api_view(['GET'])
def product_matrics(req:Request):
    categor_id = req.query_params.get('category_id')
    product_id = req.query_params.get('product_id')
    products = Product.objects.all()
    filters={}
    if categor_id is not None:
        filters['category'] = categor_id
    if product_id is not None:
        filters['id'] = product_id

    product = Product.objects.filter(**filters).aggregate(total_products=Count('id'),total_stock = Sum('quantity'),average_price=Avg('price'))
    return Response(product,status.HTTP_200_OK)    