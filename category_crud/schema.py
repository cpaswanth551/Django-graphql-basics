import graphene
from graphene_django import DjangoObjectType


from app.models import Category


class CategoryModelType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")


class Query(graphene.ObjectType):
    category = graphene.List(CategoryModelType)

    def resolve_category(self, info, **kwargs):
        return Category.objects.all()


class CategoryCreateMutation(graphene.Mutation):
    """
    mutation firstmutation {
        createCategory(name:"aswanth"){
        category{
            name
        }
        }
    }

    """

    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryModelType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CategoryCreateMutation(category=category)


class CategoryUpdateMutation(graphene.Mutation):
    """
    mutation {
      updateCategory(id:5,name:"aswanthcp"){
        category{
          name
        }
      }
    }

    """

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    category = graphene.Field(CategoryModelType)

    @classmethod
    def mutate(cls, root, info, name, id):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return CategoryUpdateMutation(category=category)


class CategoryDeleteMutation(graphene.Mutation):
    """
    mutation {
      deleteCategory(id:5){
        category{
          id
        }
      }
    }

    """

    class Arguments:
        id = graphene.Int(required=True)

    category = graphene.Field(CategoryModelType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(id=id)
        if category is not None:
            category.delete()
        return CategoryDeleteMutation(category=category)


class Mutation(graphene.ObjectType):
    create_category = CategoryCreateMutation.Field()
    update_category = CategoryUpdateMutation.Field()
    delete_category = CategoryDeleteMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
