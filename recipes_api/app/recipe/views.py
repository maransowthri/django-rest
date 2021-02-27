from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe.models import Tag, Ingredient, Recipe
from recipe.serializers import TagSerializer, IngredientSerializer, \
                               RecipeSerializer, RecipeDetailSerializer, \
                               RecipeImageSerializer


class BaseRecipeViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.query_params.get('assigned_only')
        if params:
            params_numbers = list(map(int, params.split(',')))
            queryset = queryset.filter(pk__in=params_numbers)
        return queryset.filter(user=self.request.user).order_by('-name')


class TagsView(BaseRecipeViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientsView(BaseRecipeViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipesView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        tags_params = self.request.query_params.get('tags')
        if tags_params:
            tags = list(map(int, tags_params.split(',')))
            queryset = queryset.filter(tags__id__in=tags)
        ingredients_params = self.request.query_params.get('ingredients')
        if ingredients_params:
            ingredients = list(map(int, ingredients_params.split(',')))
            queryset = queryset.filter(ingredients__id__in=ingredients)
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        elif self.action == 'upload-image':
            return RecipeImageSerializer
        return RecipeSerializer

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
