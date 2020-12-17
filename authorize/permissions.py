from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    #Custom permission to only allow owners of the shop to edit it.
    def has_object_permission(self, request, view, obj):
        if(request.method in permissions.SAFE_METHODS):
            return True
        #print(obj.owner == request.user)
        return obj.owner == request.user

class IsShopOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if(request.method in permissions.SAFE_METHODS):
            return True
        #print(obj.shop.owner)
        #print(request.user)
        #print(obj.shop.owner == request.user)
        return obj.shop.owner == request.user
