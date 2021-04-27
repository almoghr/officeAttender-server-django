import graphene
from django.db.models.signals import post_save
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import Employee, WorkSpace, User
from django.db.models import Q
import datetime
from graphql_jwt.shortcuts import get_token


def create_new_user(username, password, email):
    user = get_user_model()(username=username, email=email)
    user.set_password(password)
    user.save()
    return user


def check_user(userInfo):
    user = userInfo
    if user.is_anonymous:
        raise Exception("not logged in")
    return user


class EmployeeType(DjangoObjectType):
    class Meta:
        model = Employee
        convert_choices_to_enum = False


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class WorkSpaceType(DjangoObjectType):
    class Meta:
        model = WorkSpace


class Query(graphene.ObjectType):
    employees = graphene.List(EmployeeType)
    workspaces = graphene.List(WorkSpaceType)
    profile = graphene.Field(UserType)

    def resolve_employees(self, info, search=None):
        check_user(info.context.user)

        if search:
            filter = (
                Q(name__icontains=search),
                Q(username__icontains=search),
                Q(email__icontains=search),
                Q(occupation__icontains=search),
                Q(status__icontains=search),
                Q(address__icontains=search),
                Q(workspace__icontains=search)
            )
            return Employee.objects.filter(filter)
        return Employee.objects.all()

    def resolve_workspaces(self, info):
        return WorkSpace.objects.all()

    def resolve_user(self, info, id):
        user = check_user(info.context.user)
        return get_user_model().objects.get(id=id)

    def resolve_profile(self, info):
        user = check_user(info.context.user)
        return user


class CreateWorkspace(graphene.Mutation):
    workspace = graphene.Field(WorkSpaceType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        address = graphene.String(required=True)

    def mutate(self, info, name, description, address):
        user = check_user(info.context.user)
        workspace = WorkSpace(
            name=name, description=description, address=address)
        workspace.save()
        return CreateWorkspace(workspace=workspace)


class CreateEmployee(graphene.Mutation):
    employee = graphene.Field(EmployeeType)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        name = graphene.String(required=True)
        occupation = graphene.String(required=True)
        occupationDescription = graphene.String(required=True)
        address = graphene.String(required=True)
        is_management = graphene.Boolean()
        status = graphene.String()
        workspace_id = graphene.Int(required=True)

    def mutate(self, info, username, password, email, name, occupation, occupationDescription, address, workspace_id, is_management, status):
        workspace = WorkSpace.objects.get(id=workspace_id)
        user = create_new_user(username, password, email)
        token = get_token(user)
        employee = Employee(user=user, name=name, occupation=occupation, occupationDescription=occupationDescription,
                            is_management=is_management, status=status, address=address, workspace=workspace)
        employee.save()
        return CreateEmployee(employee=employee, token=token)

    def post_employee_create(sender, instance, created, **kwargs):
        if created:
            print('a new employee has joined us!')

    post_save.connect(post_employee_create, sender=Employee)


class UpdateEmployee(graphene.Mutation):
    employee = graphene.Field(EmployeeType)

    class Arguments:
        employee_id = graphene.Int(required=True)
        name = graphene.String()
        occupation = graphene.String()
        occupationDescription = graphene.String()
        status = graphene.String()
        address = graphene.String()
        is_management = graphene.Boolean()
        workspace_id = graphene.Int()
    def mutate(self, info, employee_id, name, occupation, occupationDescription, status, address, is_management, workspace_id):
        workspace = WorkSpace.objects.get(id=workspace_id)
        user = check_user(info.context.user)

        employee = Employee.objects.get(id=employee_id)
        employee.name = name
        employee.occupation = occupation
        employee.occupationDescription = occupationDescription
        employee.status = status
        employee.address = address
        employee.is_management = is_management
        employee.workspace = workspace

        employee.save()
        return UpdateEmployee(employee=employee)

    def post_employee_save(sender, instance, created, **kwargs):
        if not created:
            print('an employee has changed his details!')

    post_save.connect(post_employee_save, sender=Employee)


class DeleteEmployee(graphene.Mutation):
    employee_id = graphene.Int()

    class Arguments:
        employee_id = graphene.Int(required=True)

    def mutate(self, info, employee_id):
        user = check_user(info.context.user)
        employee = Employee.objects.get(id=employee_id)
        employee.delete()
        return DeleteEmployee(employee_id=employee_id)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = create_new_user(username, password, email)
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_employee = CreateEmployee.Field()
    update_employee = UpdateEmployee.Field()
    delete_employee = DeleteEmployee.Field()
    create_workspace = CreateWorkspace.Field()
    create_user = CreateUser.Field()
