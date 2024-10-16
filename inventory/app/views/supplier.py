from django.db.models import Count,Sum

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import Product,Category,Supplier
from ..serializer import ProductSerializer,SupplierSerializer,ProductSupplierSerializer

fields = ['name','number','email']

@api_view(['GET','POST'])
def get_create_supplier(req:Request):
    pass
    if req.method =='GET':
        supplier = Supplier.objects.prefetch_related('productsSupplier').all()
        data = SupplierSerializer(supplier,many=True)
        return Response(data.data,status.HTTP_200_OK)
        
    
    if req.method=='POST':
        print(req.data)
        serializer = SupplierSerializer(data=req.data)
        if serializer.is_valid():
            product_ids = serializer.validated_data.pop('product_ids',[])
            suppliers =serializer.save()
            print('...............................')
            print('product id',product_ids)
            print('*************',*product_ids)
            suppliers.productsSupplier.add(*product_ids)
            return Response({"data":serializer.validated_data,"details":'supplier created'},status.HTTP_201_CREATED)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET',"PUT",'DELETE'])
def get_update_delete_supplier(req:Request,id):
        try:
           pk = int(id)
        except ValueError:
           return Response({'detail': 'ID should be an integer.'}, status=status.HTTP_400_BAD_REQUEST)
       
        try:
            supplier = Supplier.objects.prefetch_related('productsSupplier').get(id=pk)
            if req.method =='GET':
                data = SupplierSerializer(supplier)
                return Response(data.data,status.HTTP_200_OK)
        
            #  updating supplier here 
            if req.method=='PUT':
                products_ids = req.data.get('product_ids')
                for field in fields:
                    val = req.data.get(field)
                    if val is not None:
                        setattr(supplier,field,val)
                    

                if req.data is not None:
                    try:
                        supplier.save()
                        supplier.productsSupplier.set(products_ids)
                        return Response({"name":supplier.name,"number":supplier.number}, status=status.HTTP_201_CREATED)
                    except Exception:
                        return Response({"detail":"Product id does not exists"},status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"details":"enter name or number"}, status=status.HTTP_400_BAD_REQUEST)
            
            if req.method=='DELETE':
                supplier.delete()
                return Response({"data":'Supplier deleted'},status.HTTP_200_OK)
        # throw an error if product does not exist 
        except Supplier.DoesNotExist:
            return Response({'detail': 'Supplier not found'}, status=status.HTTP_404_NOT_FOUND)   
    
    
@api_view(['GET'])
def supplier_matrics(req:Request):
    supplier = req.query_params.get('supplier')
    filters={}
    if supplier is not None:
        filters['name__icontains'] = supplier

    total_product = Supplier.objects.prefetch_related('productsSupplier').filter(**filters).annotate(total_products=Count('productsSupplier'))
    products = Supplier.objects.prefetch_related('productsSupplier').filter(**filters).all()
    highest_count = total_product.order_by('-total_products').first()
    lowest_count = total_product.order_by('total_products').first()
    
    serializer  = SupplierSerializer(products,many=True)
    # print(total_product.count())
    return Response({
        "total_product":total_product.aggregate(total=Count('productsSupplier'))['total'],
                     "highest_count":highest_count.total_products,
                     "lowest_count":lowest_count.total_products,
                     "data":serializer.data
                     },
                    status.HTTP_200_OK)        