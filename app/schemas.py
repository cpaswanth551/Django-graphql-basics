import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField

from app.models import Answer, Category, Question, Quiz


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")


class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quiz
        fields = ("id", "title", "category", "quiz")


class QuestionType(DjangoObjectType):
    answers = graphene.List(lambda: AnswerType)

    class Meta:
        model = Question
        fields = ("title", "quiz")

    def resolve_answers(root, info):
        return Answer.objects.filter(question=root)


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question", "answer_text")


class Query(graphene.ObjectType):
    """


    GraphQL query examples:

    Fetch a single question:
    query {
    singleQuestion(id: 1) {
        title
        answers {
        answerText
        }
    }
    }

    Fetch all questions with their answers:
    query {
    allQuestions {
        title
        answers {
        answerText
        }
    }
    }
    """

    # Queries for single and all questions
    single_question = graphene.Field(QuestionType, id=graphene.Int())
    all_questions = graphene.List(QuestionType)

    # Queries for answers
    single_question_answers = graphene.List(AnswerType, id=graphene.Int())

    # Resolver for single question
    def resolve_single_question(root, info, id):
        return Question.objects.get(pk=id)

    # Resolver for all questions
    def resolve_all_questions(root, info):
        return Question.objects.all()

    # Resolver for answers of a single question
    def resolve_single_question_answers(root, info, id):
        return Answer.objects.filter(question=id)


schema = graphene.Schema(query=Query)
