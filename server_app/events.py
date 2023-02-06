import graphene
import channels_graphql_ws
from server_app.types import DynamicScalar

class CharacterEventType(graphene.ObjectType):
    event_type = graphene.String()
    data = DynamicScalar()

class OnCharacterEvent(channels_graphql_ws.Subscription):
    character_event = graphene.Field(CharacterEventType)

    def subscribe(self, info, **kwargs):
        del info
        return ['character_event']

    def publish(self, info, **kwargs):
        return OnCharacterEvent(character_event=self)

    @classmethod
    def char_event(cls, params):
        print(f'publishing {params}')
        cls.broadcast(
            group='character_event',
            payload={"event_type": params['event_type'], 'data': params['data']}
        )