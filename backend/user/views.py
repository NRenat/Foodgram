from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import Subscription, User
from user.serializers import FollowListSerializer, FollowSerializer


class FollowApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        data = {'user': request.user.id, 'following': id}
        serializer = FollowSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        follow = get_object_or_404(
            Subscription, user=user, following=following
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListAPIView(ListAPIView):
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowListSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
