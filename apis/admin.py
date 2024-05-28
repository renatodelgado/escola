from django.contrib import admin
from apis.models import *


# Register your models here.
@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'nome',)


@admin.register(CursoTrilha)
class CursoTrilhaAdmin(admin.ModelAdmin):
    list_display = ('id_curso', 'id_trilha',)


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome',)


@admin.register(Trilha)
class TrilhaAdmin(admin.ModelAdmin):
    list_display = ('nome',)


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('id_curso', 'turno',)
