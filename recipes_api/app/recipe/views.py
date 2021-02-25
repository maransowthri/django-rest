from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe.models import Tag, Ingredient
from recipe.serializers import TagSerializer, IngredientSerializer


class BaseRecipeViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagsView(BaseRecipeViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class ingredientsView(BaseRecipeViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
