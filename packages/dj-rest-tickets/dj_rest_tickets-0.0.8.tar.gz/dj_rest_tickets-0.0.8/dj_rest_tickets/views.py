from django.shortcuts import render
from django.db.models import Q
from rest_framework import (
    viewsets, 
    permissions, 
    decorators
)
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    TicketSerializer,
    SupportTeamMemberSerializer,
    SupportTeamSerializer,
    AssignTeamTicketSerializer,
    AssignTeamMemberTicketSerializer,
    ChangeStatusTicketSerializer,
    TicketMessageSerializer,
)
from .models import (
    Ticket,
    SupportTeam,
    SupportTeamMember,
    TicketMessage
)
from .permissions import IsSupportAdmin, IsSupportTeamMember
from origin.utils import CustomPageNumberPagination


class TicketViewSet(viewsets.ModelViewSet):

    permission_classes=[permissions.IsAuthenticated,IsSupportTeamMember]
    pagination_class=CustomPageNumberPagination

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        if self.request.user.support_team_member.is_admin:
            return super().get_queryset().filter(
                Q( support_team_member = self.request.user.support_team_member) |
                Q( support_team=self.request.user.support_team_member.support_team ) |
                Q( support_team=None )
            )
        
        return super().get_queryset().filter(support_team_member = self.request.user.support_team_member)
    
    @decorators.action(
        detail=True,
        methods=['POST'],
        permission_classes=[permissions.IsAuthenticated, IsSupportAdmin],
        serializer_class=AssignTeamTicketSerializer
    )
    def change_support_team(self,request,pk):
        return self.update(request,pk)
    
    @decorators.action(
        detail=True,
        methods=['POST'],
        permission_classes=[permissions.IsAuthenticated, IsSupportAdmin],
        serializer_class=AssignTeamMemberTicketSerializer
    )
    def change_support_team_member(self,request,pk):
        return self.update(request,pk)
    
    @decorators.action(
        detail=True,
        methods=['POST'],
        permission_classes=[permissions.IsAuthenticated, IsSupportAdmin],
        serializer_class=ChangeStatusTicketSerializer
    )
    def change_status(self,request,pk):
        return self.update(request,pk)


class SupportTeamMemberViewSet(viewsets.ModelViewSet):

    permission_classes=[permissions.IsAuthenticated, IsSupportAdmin]

    queryset = SupportTeamMember.objects.all()
    serializer_class = SupportTeamMemberSerializer
    pagination_class=CustomPageNumberPagination


class SupportTeamViewSet(viewsets.ModelViewSet):

    permission_classes=[permissions.IsAuthenticated, IsSupportAdmin]

    queryset = SupportTeam.objects.all()
    serializer_class = SupportTeamSerializer
    pagination_class=CustomPageNumberPagination


class TicketMessageViewSet(viewsets.ModelViewSet):
    permission_classes=[permissions.IsAuthenticated]

    queryset = TicketMessage.objects.all()
    serializer_class = TicketMessageSerializer
    pagination_class=CustomPageNumberPagination

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'ticket'
    ]

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(ticket__creator = self.request.user) |
            Q(ticket__support_team_member__user = self.request.user) 
        )