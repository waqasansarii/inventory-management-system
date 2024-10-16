from django.db.models import Count,Sum

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import Category
from ..serializer import CategorySerializer,CategoryProductSerializer

@api_view(['GET','POST'])
def get_create_category(req:Request):
    if req.method =='GET':
        category = Category.objects.prefetch_related('productsCategory').all()
        data = CategoryProductSerializer(category,many=True)
        return Response(data.data,status.HTTP_200_OK)
    
    if req.method=='POST':
        print(req.data)
        serializer = CategorySerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.validated_data,"details":'category created'},status.HTTP_201_CREATED)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET',"PUT",'DELETE'])
def get_update_delete_category(req:Request,id):
        try:
           pk = int(id)
        except ValueError:
           return Response({'detail': 'ID should be an integer.'}, status=status.HTTP_400_BAD_REQUEST)
       
        try:
            category = Category.objects.get(id=pk)
            if req.method =='GET':
                data = CategorySerializer(category)
                return Response(data.data,status.HTTP_200_OK)
        
            #  updating category here 
            if req.method=='PUT':
                name = req.data.get('name')
                description = req.data.get('description')
                if name is not None:
                    category.name = name
                if description is not None:
                    category.description = description  
                
                if req.data is not None:
                    category.save()
                    return Response({"name":category.name,"description":category.description}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"details":"enter name or description"}, status=status.HTTP_400_BAD_REQUEST)
            
            if req.method=='DELETE':
                category.delete()
                return Response({"data":'category deleted'},status.HTTP_200_OK)
        # throw an error if category does not exist 
        except Category.DoesNotExist:
            return Response({'detail': 'category not found'}, status=status.HTTP_404_NOT_FOUND)   


@api_view(['GET'])
def category_matrics(req:Request):
    categor_id = req.query_params.get('category_id')
    filters={}
    if categor_id is not None:
        filters['id'] = categor_id

    product = Category.objects.filter(**filters).aggregate(total_products=Count('productsCategory'),stock=Sum('productsCategory__quantity'))
    product_stock=product['stock'] or 0
    return Response({"total_product":product['total_products'],"product_stock":product_stock},status.HTTP_200_OK)    