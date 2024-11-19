
---

# GraphQL API with Django and Graphene

## Prerequisites

- Python 3.7+
- Django installed (`pip install django`)
- Graphene Django installed (`pip install graphene-django`)

Ensure you have a model named `Category` in your app, like:

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
```

---

## Schema Overview

This API provides the following functionalities for `Category` objects:
1. **Query all categories.**
2. **Create a new category.**
3. **Update an existing category.**
4. **Delete an existing category.**

### Key Files and Classes

1. **`CategoryModelType`**: Represents the `Category` model in GraphQL.
2. **`Query`**: Handles fetching data.
3. **`CategoryCreateMutation`**: Mutation to create a new category.
4. **`CategoryUpdateMutation`**: Mutation to update an existing category.
5. **`CategoryDeleteMutation`**: Mutation to delete an existing category.

---

## Code Breakdown

### `CategoryModelType`
Defines the GraphQL type for the `Category` model:

```python
class CategoryModelType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")
```

### Query
Fetches a list of all categories.

```python
class Query(graphene.ObjectType):
    category = graphene.List(CategoryModelType)

    def resolve_category(self, info, **kwargs):
        return Category.objects.all()
```

### Mutations

#### **Create a Category**
Allows creating a new category using GraphQL.

```python
class CategoryCreateMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryModelType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CategoryCreateMutation(category=category)
```

#### Example Query:
```graphql
mutation {
  createCategory(name: "New Category") {
    category {
      name
    }
  }
}
```

#### **Update a Category**
Allows updating an existing category using its ID.

```python
class CategoryUpdateMutation(graphene.Mutation):
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
```

#### Example Query:
```graphql
mutation {
  updateCategory(id: 1, name: "Updated Name") {
    category {
      name
    }
  }
}
```

#### **Delete a Category**
Allows deleting an existing category using its ID.

```python
class CategoryDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    category = graphene.Field(CategoryModelType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(id=id)
        if category is not None:
            category.delete()
        return CategoryDeleteMutation(category=category)
```

#### Example Query:
```graphql
mutation {
  deleteCategory(id: 1) {
    category {
      id
    }
  }
}
```

### Schema
Combines all queries and mutations.

```python
class Mutation(graphene.ObjectType):
    create_category = CategoryCreateMutation.Field()
    update_category = CategoryUpdateMutation.Field()
    delete_category = CategoryDeleteMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
```

---

## Running the API

1. **Add Graphene to Django Settings**  
   In `settings.py`, add:
   ```python
   GRAPHENE = {
       "SCHEMA": "app.schema.schema"  # Path to your schema file
   }
   ```

2. **Create a GraphQL View**  
   In `urls.py`, add:
   ```python
   from graphene_django.views import GraphQLView
   from django.urls import path

   urlpatterns = [
       path("graphql/", GraphQLView.as_view(graphiql=True)),  # Enables the GraphiQL interface
   ]
   ```

3. **Run the Django Server**  
   Start the server with:
   ```bash
   python manage.py runserver
   ```

4. **Access the GraphQL Playground**  
   Open your browser and go to:
   ```
   http://localhost:8000/graphql/
   ```

5. **Run GraphQL Queries**  
   Use the GraphQL Playground to run queries and mutations like the examples provided above.

---

## Example Usage

### Fetch All Categories
```graphql
query {
  category {
    id
    name
  }
}
```

### Create a Category
```graphql
mutation {
  createCategory(name: "Education") {
    category {
      id
      name
    }
  }
}
```

### Update a Category
```graphql
mutation {
  updateCategory(id: 1, name: "Healthcare") {
    category {
      id
      name
    }
  }
}
```

### Delete a Category
```graphql
mutation {
  deleteCategory(id: 1) {
    category {
      id
    }
  }
}
```

---

This guide provides a comprehensive walkthrough of the API, enabling developers to extend or use it effectively.