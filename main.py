# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Name: Fis0506-1
# Courses: 30
# Rooms: 6
# Days: 5
# Periods_per_day: 6
# Curricula: 14
# Constraints: 53

#### Restrições Fortes:
# – H1-Aulas: Todas as aulas de uma disciplina devem ser alocadas, e em períodos
# diferentes. Uma violação ocorre se uma aula não é alocada, ou se duas aulas da
# mesma disciplina são alocadas no mesmo período.
# – H2-Ocupação de Sala: Duas aulas não podem ser alocadas em uma mesma sala
# e no mesmo período. Cada aula extra em uma mesma sala e no mesmo período
# conta como uma violação.
# – H3-Conflitos: Aulas de disciplinas de um mesmo currículo, ou ministradas
# pelo mesmo professor devem ser alocadas em períodos diferentes. Duas aulas
# conflitantes no mesmo período representa uma violação.
# – H4-Indisponibilidade: Se o professor de uma disciplina não está disponível para
# lecioná-la em determinado período, nenhuma aula dessa disciplina pode ser
# alocada nesse período. Cada aula alocada em um período não disponível para a
# disciplina conta como uma violação.
#### Restrições Fracas:
# – S1-Capacidade de Sala: Para cada disciplina, o número de alunos que está
# matriculado na disciplina deve ser menor ou igual ao número de assentos
# disponíveis em todas as salas que ocorrem aulas dessa disciplina. Cada aluno
# acima da capacidade conta como uma violação.
# – S2-Número Mínimo de Dias de Aula: As aulas de uma disciplina devem ser
# espalhadas em um número mínimo de dias. Cada dia abaixo do número mínimo
# de dias conta como uma violação.
# – S3-Aulas Isoladas: Aulas de disciplinas de um mesmo currículo devem ser
# adjacentes uma à outra. Para cada currículo, uma violação é contada quando há
# uma aula não adjacente à nenhuma outra aula do mesmo currículo no mesmo
# dia.
# – S4-Estabilidade de Sala: Todas as aulas de uma disciplina devem acontecer
# na mesma sala. Cada sala distinta usada para aulas dessa disciplina, além da
# primeira, contam como uma violação.

yy_benchmark = 108
timeslots = 0


class Problem:
	def __init__(self, name, courses, rooms, days, periods_per_day, curricula, constraints):
		self.name = name
		self.courses = courses
		self.rooms = rooms
		self.days = days
		self.periods_per_day = periods_per_day
		self.curricula = curricula
		self.constraints = constraints


	def __str__(self):
		return "Nome: " + self.name + "\n" + "Disciplinas: " + str(self.courses) + "\n" + "Salas: " + str(self.rooms) + "\n" + "Dias: " + str(self.days) + "\n" + "Períodos por dia: " + str(self.periods_per_day) + "\n" + "Currículos: " + str(self.curricula) + "\n" + "Restrições: " + str(self.constraints) + "\n"

class Course:
	def __init__(self, name, teacher, classesPerWeek, min_days, occupancy):
		self.name = name
		self.teacher = teacher
		self.classesPerWeek = classesPerWeek
		self.min_days = min_days
		self.occupancy = occupancy
		self.constraint_matrix = []
		self.owner_curricula = []

	def init_constraint_matrix(self, days, periods_per_day):
		# Inicializa a matriz de restrição com todos os valores como True
		for _ in range(periods_per_day):
			self.constraint_matrix.append([True] * days)

	def is_init_constraint_matrix(self):
		# Verifica se a matriz de restrição foi inicializada
		if self.constraint_matrix == []:
			return False
		else:
			return True

	def set_constraint_matrix(self, day, period, value=False):
		# Define o valor de uma posição da matriz de restrição
		self.constraint_matrix[period][day] = value

	def check_constraint_matrix(self, day, period):
		if self.constraint_matriz == []:
			print("Disciplina não possui restrições")
			return True
		else:
			# Verifica a disponibilidade de uma posição da matriz de restrição
			return self.constraint_matrix[period][day]

	def print_constraint_matrix(self):
		# Imprime a matriz de restrição
		print("Matriz de restrição da disciplina " + self.name + ":")

		print(days_str)
		for i in range(periods):
			print(self.constraint_matrix[i])

		print("\n")
	def set_owner_curricula(self, curricula):
		self.owner_curricula = curricula
	def __str__(self):
		return "Nome: " + self.name + "\n" + "Professor: " + self.teacher + "\n" + "Aulas por semana: " + str(self.classesPerWeek) + "\n" + "Dias mínimos: " + str(self.min_days) + "\n" + "Alunos: " + str(self.occupancy) + "\n"

class Room:
	def __init__(self, name, capacity):
		self.name = name
		self.capacity = capacity

	def __str__(self):
		return "Nome: " + self.name + "\n" + "Capacidade: " + str(self.capacity) + "\n"

class Curricula:
	def __init__(self, name, size, courses):
		self.name = name
		self.size_courses = size
		self.courses = courses

	def __str__(self):
		return "Nome: " + self.name + "\n" + "Tamanho: " + str(self.size_courses) + "\n" + "Disciplinas: " + str(self.courses) + "\n"

def clean_empty_lines(file):
	# clean empty line
	file.readline()
	# clean Title line
	file.readline()

	#read file problem until END
def read_file(file):
	# read problem and put in Problem class
	problem = Problem(file.readline().split()[1], int(file.readline().split()[1]), int(file.readline().split()[1]),
	                  int(file.readline().split()[1]), int(file.readline().split()[1]), int(file.readline().split()[1]),
	                  int(file.readline().split()[1]))

	clean_empty_lines(file)

	# define timeslots
	timeslots = problem.days * problem.periods_per_day

	# read courses and put in Course class
	courses = []
	for i in range(problem.courses):
		course = file.readline().split()
		courses.append(Course(course[0], course[1], int(course[2]), int(course[3]), int(course[4])))

	clean_empty_lines(file)

	# read rooms and put in Room class
	rooms = []
	for i in range(problem.rooms):
		room = file.readline().split()
		rooms.append(Room(room[0], int(room[1])))

	clean_empty_lines(file)

	# read curricula and put in Curricula class
	curricula = []
	for i in range(problem.curricula):
		curriculum = file.readline().split()
		curricula.append(Curricula(curriculum[0], int(curriculum[1]), curriculum[2:]))

	clean_empty_lines(file)

	# read constraints
	for i in range(problem.constraints):
		constraint = file.readline().split()
		for j in courses:
			if j.name == constraint[0]:
				# Verifica se a matriz de restrição foi inicializada
				if not j.is_init_constraint_matrix():
					# Inicializa a matriz de restrição
					j.init_constraint_matrix(problem.days, problem.periods_per_day)
				# Define o timeslot como indisponível na matriz de restrição
				j.set_constraint_matrix(int(constraint[1]), int(constraint[2]), False)
				break
		j.print_constraint_matrix()

	#print_entries(problem, courses, rooms, curricula)


def print_entries(problem, courses, rooms, curricula):
	print(problem)
	print("Cursos:")
	for i in courses:
		print(i)

	print("Salas:")
	for i in rooms:
		print(i)

	print("Currículos:")
	for i in curricula:
		print(i)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	# read file
	file = open("Instancias/toy.ctt", "r")

	read_file(file)





