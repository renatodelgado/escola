from rest_framework import generics  # Criar uma views genérica
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.shortcuts import render


def index(request):
    context = {"dados": 'APIs para o curso de Django'}
    return render(request, 'index.html', context)


class CursoApiView(generics.ListCreateAPIView):  # Aqui informa o que a API vai fazer. Neste caso, lista e cria
    queryset = Curso.objects.all()   # Ou seja, traga todos os cursos que estão na base de dados
    serializer_class = CursoSerializer


class TrilhaApiView(generics.ListCreateAPIView):
    queryset = Trilha.objects.all()
    serializer_class = TrilhaSerializer


class CursoTrilhaApiView(generics.ListCreateAPIView):
    queryset = CursoTrilha.objects.all()
    serializer_class = CursoTrilhaSerializer


class TurmaApiView(generics.ListCreateAPIView):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer


class AlunoApiView(generics.ListCreateAPIView):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
