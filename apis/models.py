from django.db import models


class Base(models.Model):
    data_criacao = models.DateTimeField(auto_now_add = True,
                                        db_column = 't_____criacao',
                                        db_comment = 'Data de inclusão do objeto'
                                        )
    # auto_now_add=True adiciona automaticamente a data de criação da linha
    # é de boa praxe sempre colocar um comentário sobre o que é a coluna
    data_atualizacao = models.DateTimeField(auto_now = True,
                                            db_column = 't_____ulat',
                                            db_comment = 'Data da última atualização do objeto'
                                            )
    ativo = models.BooleanField(default = True,
                                db_column = 'f_____ativo',
                                db_comment = 'Indicador se é objeto ainda está ativo'
                                )

    # Essa classe é "abstrata", não será uma tabela real. Por isso o seguinte código:
    class Meta:
        abstract = True


class CursoTrilha(Base):
    # Automaticamente, o Django cria um id para cada tabela. Mas, para trocar o nome e pôr num padrão:
    id = models.BigAutoField(primary_key = True,  # Sempre há uma e somente uma chave primária
                             db_column = 'ccurtrsequencial',
                             db_comment = 'Chave da tabela tbcursotrilha'
                             )
    # Chave estrangeira (ForeignKey) - liga duas tabelas
    # Sempre que for uma chave estrangeira, devo dizer o que deve acontecer com a possível remoção
    id_curso = models.ForeignKey('Curso',  # nome da classe a ser criada
                                 on_delete = models.RESTRICT,
                                 # Ou seja, se tiver o filho (curso), não é possível apagar o pai (curso/trilha) (outras possibilidades: cascade - apaga o pai, apaga o filho -, setnull, setdefault)
                                 db_column = 'ccursosequencial',
                                 db_comment = 'Chave de ligação com a tabela tbcurso'
                                 )
    id_trilha = models.ForeignKey('Trilha',
                                  on_delete = models.RESTRICT,
                                  db_column = 'ctrilhasequencial',
                                  db_comment = 'Chave de ligação com a tabela tbtrilha'
                                  )

    # Não é obrigatório ter Meta, mas precisa colocar se quiser modificar alguns parâmetros

    class Meta:
        verbose_name = 'Curso Trilha'
        verbose_name_plural = 'Cursos Trilhas'
        unique_together = ('id_curso', 'id_trilha')  # Não pode ter mais de uma associação de curso e trilha com mesmo número
        db_table = "tbcursotrilha"  # Se não colocar o nome aqui, fica com o nome da classe
        indexes = [models.Index(fields = ['id'], name = 'pcurtrchave'),
                   models.Index(fields = ['id_trilha', 'id_curso'], name = 'ucurtrchave'),
                   models.Index(fields = ['id_trilha'], name = 'icurtridtrilha'),
                   models.Index(fields = ['id_curso'], name = 'icurtridcurso'),
                   ]

    def __str__(self):
        return 'Trilha: ' + str(self.id_trilha) + ', Curso: ' + str(self.id_curso)
    # Retorna isso se for pedido um "print(CursoTrilha)"


class Trilha(Base):
    id = models.BigAutoField(primary_key = True,  # Sempre há uma e somente uma chave primária
                             db_column = 'ctrilhsequencial',
                             db_comment = 'Chave da tabela tbtrilha'
                             )
    nome = models.CharField(max_length = 50,  # Obrigatório em CharField
                            unique = True,  # Não aceita mais de uma trilha com mesmo nome
                            blank = False,  # Não aceita deixar com nome em branco
                            null = False,
                            db_column = 'ntrilhnome',
                            db_comment = 'Nome da trilha'
                            )
    valor = models.DecimalField(max_digits = 9,  # Quantos dígitos (7 inteiros + 2 decimais)
                                decimal_places = 2,  # Quantas casas decimais
                                blank = False,
                                null = False,
                                db_column = 'vtrilhpreco',
                                db_comment = 'Valor da trilha'
                                )
    # Abre uma caixa maior do que o CharField
    descricao_trilha = models.TextField(db_column = 'etrilhdescricao',
                                        db_comment = 'Descrição da trilha'
                                        )
    publico_alvo = models.TextField(db_column = 'etrilhpublico',
                                    db_comment = 'Público-alvo da trilha'
                                    )
    carga_horaria = models.IntegerField(db_column = 'atrilhcarga',
                                        db_comment = 'Carga horária da trilha'
                                        )

    class Meta:
        verbose_name = 'Trilha'
        verbose_name_plural = 'Trilhas'
        db_table = 'tbtrilha'
        indexes = [models.Index(fields = ['id'], name = 'ptrilhchave'),
                   models.Index(fields = ['nome'], name = 'utrilhnome'),
                   ]

    def __str__(self):
        return self.nome


class Curso(Base):
    id = models.BigAutoField(primary_key = True,
                             db_column = 'ccursosequencial',
                             db_comment = 'Chave da tabela tbcurso'
                             )
    nome = models.CharField(max_length = 50,
                            unique = True,
                            blank = False,
                            null = False,
                            db_column = 'ncursonome',
                            db_comment = 'Nome do curso'
                            )
    valor = models.DecimalField(max_digits = 9,
                                decimal_places = 2,
                                blank = False,
                                null = False,
                                db_column = 'vcursopreco',
                                db_comment = 'Valor do curso'
                                )
    descricao_trilha = models.TextField(db_column = 'ecursodescricao',
                                        db_comment = 'Descrição do curso'
                                        )
    publico_alvo = models.TextField(db_column = 'ecursopublico',
                                    db_comment = 'Público-alvo do curso'
                                    )
    carga_horaria = models.IntegerField(db_column = 'acursocarga',
                                        db_comment = 'Carga horária do curso'
                                        )

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        db_table = 'tbcurso'
        indexes = [models.Index(fields = ['id'], name = 'pcursochave'),
                   models.Index(fields = ['nome'], name = 'ucursonome'),
                   ]

    def __str__(self):
        return self.nome


class Turma(Base):
    # Criação de opções de turnos
    TURNO_CHOICE = (
        ('M', 'Manhã'),
        ('T', 'Tarde'),
        ('V', 'Vespertino'),
        ('N', 'Noite'),
        ('I', 'Integral')
    )
    id = models.BigAutoField(primary_key=True,
                             db_column='cturmasequencial',
                             db_comment='Identificador do Curso'
                             )
    id_curso = models.ForeignKey('Curso',
                                 on_delete=models.RESTRICT,
                                 db_column='ccursosequencial',
                                 related_name='curso_participa_turma',
                                 blank=False,
                                 null=False)
    professor = models.CharField( max_length=50,
                                  blank=False,
                                  null=False,
                                  db_column='nturmaprofessor',
                                  db_comment='Nome do Professor'
                                  )
    turno = models.CharField(max_length=1,
                             blank=False,
                             null=False,
                             db_column='cturmaturno',
                             db_comment='Turno da Turma',
                             choices=TURNO_CHOICE
                             )
    seg = models.BooleanField(default=False,
                              db_column='fturmasegunda',
                              db_comment='Indicador se acontece às segundas-feiras'
                              )
    ter = models.BooleanField(default=False,
                              db_column='fturmaterca',
                              db_comment='Indicador se acontece às terças-feiras'
                              )
    qua = models.BooleanField(default=False,
                              db_column='fturmaquarta',
                              db_comment='Indicador se acontece às quartas-feiras'
                              )
    qui = models.BooleanField(default=False,
                              db_column='fturmaquinta',
                              db_comment='Indicador se acontece às quintas-feiras'
                              )
    sex = models.BooleanField(default=False,
                              db_column='fturmasexta',
                              db_comment='Indicador se acontece às sextas-feiras'
                              )
    sab = models.BooleanField(default=False,
                              db_column='fturmasabado',
                              db_comment='Indicador se acontece aos sábados'
                              )
    inicio = models.DateField(blank=False,
                              null=False,
                              db_column='dturmainicio',
                              db_comment='Data do início da turma'
                              )
    final = models.DateField(blank=False,
                             null=False,
                             db_column='dturmafinal',
                             db_comment='Data do final da turma'
                             )
    horario = models.CharField(blank=False,
                               null=False,
                               db_column='eturmahorario',
                               db_comment='Horário da turma', max_length=13
                               )

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        db_table = 'tbturma'
        indexes = [models.Index(fields=['id'], name='pturmachave'),
                   models.Index(fields=['id_curso'], name='fturmacurso'),
                   ]

    def __str__(self):
        return 'Curso: ' + str(self.id_curso) + 'Início: ' + str(self.inicio)