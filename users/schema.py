"""
Schema contendo objetos de usuário para o sistema.
Neste módulo ficarão:
    - Objetos graphql;
    - Queries (consultas) relacionadas a usuários;
    - Mutations:
        + Para cadastro;
        + LogOut do sistema

By Beelzebruno <brunolcarli@gmail.com>
"""
from datetime import datetime
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from users.utils import access_required
# from server_app.models import Character
import graphql_jwt


class UserType(DjangoObjectType):
    """
    Modelo de usuário padrão do django
    """ 
    class Meta:
        model = get_user_model()
        interfaces = (graphene.relay.Node,)


class UserConnection(graphene.relay.Connection):
    """Implementa o relay no objeto User."""
    class Meta:
        node = UserType


class Query(object):
    """
    Consultas GraphQL delimitando-se ao escopo
    de usuários.
    """
    users = graphene.relay.ConnectionField(UserConnection)

    @access_required
    def resolve_users(self, info, **kwargs):
        """
        Retorna uma lista de todos os usuários registrados no sistema.
        """
        return get_user_model().objects.all()


class CreateUser(graphene.relay.ClientIDMutation):
    """
    Cadastra um novo usuário no sistema.
    """
    user = graphene.Field(
        UserType,
        description='The response is a User Object.'
    )

    class Input:
        """inputs"""
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **_input):
        username = _input.get('username')
        password = _input.get('password')
        email = _input.get('email')

        try:
            user = get_user_model().objects.create(
                username=username,
                email=email
            )
            user.set_password(password)
            user.save()
        except Exception as ex:
            print(ex)
            raise Exception(
                'Username or email already registered. Please choose another username!'
            )
        return CreateUser(user=user)


class LogOut(graphene.relay.ClientIDMutation):
    """
    Desloga do sistema.
    """
    response = graphene.Boolean()

    class Input:
        username = graphene.String(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **_input):
        username = _input['username']
        meta_info = info.context.META
        user_token = meta_info.get('HTTP_AUTHORIZATION').split(' ')[1]
        token_metadata = graphql_jwt.utils.jwt_decode(user_token)

        if username != token_metadata['username']:
            raise Exception('Invalid credentials')

        # characters = Character.objects.filter(reference=username, logged=True)
        # for ent in ents:
        #     ent.logged = False
        #     ent.save()

        return LogOut(True)


class LogIn(graphene.relay.ClientIDMutation):
    token = graphene.String()

    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            user = get_user_model().objects.get(
                email=kwargs['email']
            )
        except get_user_model().DoesNotExist:
            raise Exception('User not found')

        if not user.check_password(kwargs['password']):
            raise Exception('Invalid password')

        user.last_login = datetime.now()
        user.save()

        session = graphql_jwt.ObtainJSONWebToken.mutate(
            self,
            info,
            username=user.username,
            email=user.email,
            password=kwargs['password']
        )

        return LogIn(session.token)


class Mutation(object):
    sign_up = CreateUser.Field()
    log_out = LogOut.Field()
    log_in = LogIn.Field()
