# Desafio Python
# criar um programa com as seguintes caracteristicas
# menu com: cadastrar alunos, materias e notas com opcao de listar e excluir
# cadastrar boletim com notas bimestrais, exibir media e status aprovado/reprovado
# fazer uplado no github

import os, sqlite3
from string import join, split

# Menu do sistema
def menu():
   os.system('clear')
   print '-'*30, 'B O L E T I M   E S C O L A R', '='*8
   print '---------- sistema criado em  python'
   print '-'*60
   print 'Escolha uma Opcao'
   print '-'*30
   print '| - 1 - Cadastrar Aluno'
   print '| - 2 - Cadastrar Materias'
   print '-'*60
   print '| - 3 - Listar Alunos cadastrados'
   print '| - 4 - Exlcuir Alunos cadastrados'
   print '| - 5 - Listar materias cadastradas'
   print '| - 6 - Excluir materias cadastradas'
   print '-'*60
   print '| - 7 - Cadastrar Boletim'
   print '| - 8 - Apagar boletim'
   print '| - 9 - Visualizar boletim'
   print '-'*60
   print '| - 0 - Sair'
   print '-'*60
   print '-'*60

def volta_menu(opcao):
   print 'Voce esta em:', opcao
   raw_input('funcao volta_menu, tecle < enter > para voltar ao menu: ')

porta = sqlite3.connect('boletim.db')
chave = porta.cursor()

try:
   chave.execute('select id from boletim')
   chave.execute('select id from tab_materias')
   chave.execute('select id from notas')
except:
   chave.execute('CREATE TABLE boletim (id INTEGER PRIMARY KEY, nome VARCHAR (30), email VARCHAR (30), serie VARCHAR (10))')   
   chave.execute("CREATE TABLE tab_materias (id INTEGER PRIMARY KEY, serie VARCHAR (10), materias VARCHAR (400))")
   chave.execute("CREATE TABLE notas (id INTEGER PRIMARY KEY, aluno VARCHAR (4), serie VARCHAR (10), materia VARCHAR (20), bimestre VARCHAR (2), nota VARCHAR (2))")

while True:
   menu()
   mopcao = raw_input('Digite a opcao desejada: ')
      # cadastra Aluno - ok
   if mopcao == '1':
      print 'Cadastrar Aluno - opcao selecionada'
      aluno_nome = raw_input('Nome do Aluno: ')
      aluno_email = raw_input('Email do Aluno: ')
      print '1m - Ensino medio ano 1\n2m - Ensino medio ano 2\n3m - Ensino medio ano 3'
      print '1s - Ensino superior ano 1\n2s - Ensino superior ano 2\n3s - Ensino superior ano 3' 
      aluno_serie = raw_input('Serie do Aluno: ')
      chave.execute("INSERT INTO boletim(nome,email,serie) VALUES ('%s','%s','%s');"% (aluno_nome,aluno_email,aluno_serie,))
      porta.commit()
      volta_menu('Incluir Aluno')

   elif mopcao == '2':
		# Cadastra materias para montar boletim, obs. fazer dinamicamente - ok
		# deve informar o nome da materia, imprimir 4x(referente aos bimestres) - ok
      print '1m - Ensino medio ano 1\n2m - Ensino medio ano 2\n3m - Ensino medio ano 3'
      print '1s - Ensino superior ano 1\n2s - Ensino superior ano 2\n3s - Ensino superior ano 3' 
      serie = raw_input('Qualserie deseja cadastrar as materias: ')
      qtd_materias = int(raw_input('Quantas materias vc deseja cadastrar nessa serie: '))
      materias = []
      uniq_list = []
      contador = 0
      while contador < qtd_materias:
         contador += 1
         print 'Cadastre a materia n:', contador
         materia = raw_input('Nome da materia : ')
         uniq_list.append(materia) 
      uniq_mat = join(uniq_list)
      chave.execute("INSERT INTO tab_materias(serie,materias) VALUES ('%s','%s');"% (serie,uniq_mat,))
      porta.commit()
      volta_menu('Incluir Materia')

   elif mopcao == '3':
      chave.execute("select * from boletim")
      for i in chave:
         print '='*30
         print '| Codigo: ', i[0]
         print '| Aluno: ', i[1]
         print '| Email:', i[2]
         print '| Serie:', i[3]
         print '-'*30
      volta_menu('Lista de Alunos Cadastrados')

   elif mopcao == '4':
      chave.execute("select * from boletim")
      for i in chave:
         print '-'*60
         print 'Codigo: %i - Aluno: %s' % (i[0],i[1])
      print '-'*60
      codigo = input('Digite o codigo do aluno que deseja excluir: ') 
      chave.execute("DELETE from  boletim where id = %d;"%  codigo)
      porta.commit()
      volta_menu('Exluir Aluno')

   elif mopcao == '5' or mopcao == '6':
      chave.execute("select * from tab_materias")
      for i in chave: 
         print 'Cod: %d Serie: %s - Materias: %s'% (i[0],i[1],i[2])
         print '-'*60
      print 'Para deletar lista de materias por serie digite'
      del_materias = raw_input('1 ou  0 para sair: ')
      if del_materias == '1':
         codigo = input('Digite o codigo da materia/serie que deseja excluir: ')
         chave.execute("DELETE from tab_materias where id = %d;"% codigo)
         porta.commit()
         volta_menu('Excluir Materias da serie')
      else:
         volta_menu('Lista de materias cadastradas')

   elif mopcao == '7':
      print 'Para incluir um boletim de notas, voce devera saber o codigo do aluno e sua serie'
      cod_aluno = input('codigo do aluno: ') 
      chave.execute("SELECT * from boletim where id = %d;"% cod_aluno )
      for i in chave:
         cod_serie = i[3]
      chave.execute("SELECT * from tab_materias where serie = '%s'" % cod_serie)
      for m in chave:
         materias_base = m[2]
         print 'Voce ira cadastrar as notas bimestrais de: ', i[1]
      lista_base = materias_base.split()

      notas_materias = []
      for materia in lista_base:
         bimestre = 0
         while bimestre < 4:
            bimestre += 1
            print 'Cadastrando as notas no banco de dados'
            nota = float(raw_input('Digite a nota referente ao bimestre %d da materia %s :'% (bimestre,materia)))
            print 'Gravando nota... '
            notas_materias.append((materia,bimestre,nota))
            chave.execute("INSERT INTO notas(aluno,serie,materia,bimestre,nota) VALUES ('%d','%s','%s','%d','%.2f');"% (cod_aluno, cod_serie, materia, bimestre, nota,))
            porta.commit()
         print 'Finalizado o processo de inlusao de notas...', materia

      volta_menu('Cadastro de Boletim')

   elif mopcao == '8':
      print 'Para excluir um boletim de notas, voce devera saber o codigo do aluno'
      cod_aluno = int(raw_input('codigo do aluno: ')) 

      chave.execute("SELECT * from boletim  WHERE id = '%s'"% cod_aluno)
      for notas in chave:
         print 'Excluir boletim do aluno: ', notas[1]
         chave.execute("DELETE  from notas WHERE aluno = '%s'"% cod_aluno)
         porta.commit()

      volta_menu('Excluir Boletim')

   elif mopcao == '9':
      print 'Para visualizar um boletim voce devera fornecer o cod do aluno.'
      cod_aluno = raw_input('Informe o codigo do aluno: ')
      print 'Conectando banco de dados...boletim'
      chave.execute("SELECT * from boletim  WHERE id = '%s'"% cod_aluno)
      for i in chave:
         print 'Aluno: %s, Serie: %s,'% (i[1],i[3])

      chave.execute("SELECT * from notas  WHERE aluno = '%s'" % cod_aluno)
      print 'materia \t\t | bimestre\t | nota'
      for mat in chave:
         materia = mat[3]
         print '%s \t\t | %d\t\t | %.2f '% (mat[3], int(mat[4]), float(mat[5]))			

      chave.execute("SELECT * from tab_materias WHERE serie = '%s'"% i[3])
      for lista in chave:
         lista_mat = split(lista[2])
         
      print '-'*20
      for i in lista_mat:
         calc_nota = 0
         print 'Materia:', i
         chave.execute("SELECT * from notas  WHERE aluno = '%s' and materia = '%s' "% (cod_aluno,i))
         for search in chave:
            calc_nota += float(search[5])
         media = calc_nota / 4
         print 'Soma total da materia: %.1f - Media: %.1f'% (calc_nota, media),
         if media < 7.0:
            print ' - reprovado nessa materia'
         else:
            print ' - aprovado nessa materia'
         print '-'*20

      volta_menu("Lista Boletim")

   elif mopcao == '0':
      print 'Saindo do Sistema - volte sempre...'
      raw_input('Pressione < enter > para sair: ')
      break

   else:
      print 'opcao invalida'
      raw_input('Pressione enter para voltar ao menu: ')

# chamar funcao para gravar notas das materias
# aluno.calcula_notas()


