import graphene
import graphql_jwt
import officeAttender.schema


class Query(officeAttender.schema.Query, graphene.ObjectType):
    pass

class Mutation(officeAttender.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)

