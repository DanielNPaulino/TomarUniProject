import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('tomar.db')

values = []

uc=["Matemática",
"Robótica",
"Ciências informáticas",
"Design",
"Gestão e administração",
"Indisponível",
"Gestão"]

for x in range(len(uc)):
	c = conn.cursor()
	c.execute('SELECT uc_nome FROM plano WHERE plano_area =="'+ uc[x] +'"')
	fetch = c.fetchall()
	values.append(len(fetch))
	print(values)

plt.suptitle('UC por Área')

plt.bar(uc, values)

plt.show()

values2 = []

tipoCurso=["Licenciatura",
"TeSP",
"Pós-Graduação",
"Mestrado"]

for x in range(len(tipoCurso)):
	d = conn.cursor()
	d.execute('SELECT nome_curso FROM curso WHERE curso_tipo =="'+tipoCurso[x] +'"')
	fetch = d.fetchall()
	values2.append(len(fetch))
	print(values2)

plt.suptitle('Curso por Tipo de Curso')

plt.bar(tipoCurso, values2)

plt.show()

values3 = []

qualificacoes=["Doutoramento",
"Mestrado",
"Indisponível"]

for x in range(len(qualificacoes)):
	e = conn.cursor()
	e.execute('SELECT nome_docente FROM docente WHERE qualifica_docente =="'+qualificacoes[x] +'"')
	fetch = e.fetchall()
	values3.append(len(fetch))
	print(values3)

plt.suptitle('Qualificações por docente')

plt.bar(qualificacoes, values3)

plt.show()