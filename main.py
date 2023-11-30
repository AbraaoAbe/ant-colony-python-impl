import random as random

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
# Solução -> Contar aulas não alocadas {not_allocated_classes}

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

# sendo que (α1,α2,α3,α4) = (1,5,2,1) representa os pesos atribuídos, respectivamente, a cada
# uma das restrições fracas S1-S4.

yy_benchmark = 108



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
	def __init__(self, name, teacher, classes_per_week, min_days, occupancy, index_in_trail):
		self.name = name
		self.teacher = teacher
		self.index_in_trail = index_in_trail
		self.classes_per_week = classes_per_week
		self.not_allocated_classes = classes_per_week
		self.min_days = min_days
		self.occupancy = occupancy
		self.constraint_matrix = []
		self.curricula = []

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
		if self.constraint_matrix == []:
			# print("Disciplina não possui restrições")
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
	def add_owner_curricula(self, curricula):
		self.curricula.append(curricula)
	def __str__(self):
		curricula_names = []
		for i in self.curricula:
			curricula_names.append(i.name)
		return "Nome: " + self.name + "\n" + "Professor: " + self.teacher + "\n" + "Aulas por semana: " + str(self.classes_per_week) + "\n" + "Dias mínimos: " + str(self.min_days) + "\n" + "Alunos: " + str(self.occupancy) + "\n" + "Currículos: " + str(curricula_names) + "\n"

	# Retorna uma lista com os nomes das disciplinas que possuem conflito com a disciplina atual
	def get_conflicts_names(self):
		courses_names = []
		for i in self.curricula:
			for j in i.courses:
				if j != self.name:
					courses_names.append(j)
		return courses_names


class Room:
	def __init__(self, name, capacity):
		self.name = name
		self.capacity = capacity

	def __str__(self):
		return "Nome: " + self.name + "\n" + "Capacidade: " + str(self.capacity) + "\n"

class Curricula_and_Teacher:
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
		courses.append(Course(course[0], course[1], int(course[2]), int(course[3]), int(course[4]), i))

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
		curricula.append(Curricula_and_Teacher(curriculum[0], int(curriculum[1]), curriculum[2:]))

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


	return problem, courses, rooms, curricula

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


def check_if_exists(teacher_name, curricula):
	for i in curricula:
		if i.name == teacher_name:
			return True
	return False

def create_teacher_curricula(courses, curricula):
	for i in courses:
		if not check_if_exists(i.teacher, curricula):
			curricula.append(Curricula_and_Teacher(i.teacher, 1, [i.name]))
		else:
			for j in curricula:
				if j.name == i.teacher:
					j.size_courses += 1
					j.courses.append(i.name)
					break


class Trail:
	def __init__(self, problem):
		self.timeslots = problem.days * problem.periods_per_day
		self.periods = problem.periods_per_day
		self.matrix = [[0 for i in range(problem.rooms * self.timeslots)] for j in range(problem.courses)]

	def setTrail(self, course, room, day, period, value=1):
		self.matrix[course][(room * self.timeslots) + (day * self.periods) + period] = value

	def getTrail(self, course, room, day):
		return self.matrix[course][(room * self.timeslots) + (day * self.periods) + period]

	def printTrail(self):
		for i in range(problem.courses):
			print(self.matrix[i])
		print("\n")

	def check_available(self, course, room, day, period):
		if self.matrix[course][(room * self.timeslots) + (day * self.periods) + period] == 0:
			return True
		else:
			return False

	# Método para verificar as disciplinas que possuem conflito de período com a disciplina atual
	# Ela checa o mesmo horário em todas as salas no mesmo período
	def check_conflicts_same_period(self, courses_indexes, problem, day, period):
		allrooms = problem.rooms
		for i in range(allrooms):
			for j in courses_indexes:
				if self.matrix[j][(i * self.timeslots) + (day * self.periods) + period] == 1:
					return False
		return True

def ant_walk(alpha, beta, trail, courses, problem):
	not_visited = courses.copy()
	temporary_walk = Trail(problem)

	for i in range(len(not_visited)):
		#seleciona uma disciplina aleatória
		course = not_visited.pop(random.randrange(len(not_visited)))

		while course.not_allocated_classes > 0:
			#Retorna uma lista de slots viaveis para a disciplina
			feasible_list = get_feasible_list(temporary_walk, course, problem, courses)
			if True :
				print(feasible_list)
				break


#Retorna uma lista de slots viaveis para a disciplina que não violam as restrições fortes
def get_feasible_list(walk, course, problem, courses):
	courses_conflicts = course.get_conflicts_names()
	print(course.name)
	courses_conflicts_indexes = get_courses_indexes(courses, courses_conflicts)
	print(courses_conflicts_indexes)
	feasible_list = []
	for i in range(problem.rooms):
		for j in range(problem.days):
			for k in range(problem.periods_per_day):
				if walk.check_available(course.index_in_trail, i, j, k) and walk.check_conflicts_same_period(courses_conflicts_indexes, problem, j, k) and course.check_constraint_matrix(j, k):
					feasible_list.append([i, j, k])
	return feasible_list

def get_courses_indexes(courses, courses_conflicts):
	courses_indexes = []
	for i in courses_conflicts:
		for j in courses:
			if i == j.name:
				courses_indexes.append(j.index_in_trail)
				break
	return courses_indexes

#Method to link the course with the curricula that it belongs
def set_owner_curricula(courses, curricula):
	for i in curricula:
		for j in i.courses:
			for k in courses:
				if j == k.name:
					k.add_owner_curricula(i)
					break


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	# read file
	file = open("Instancias/toy.ctt", "r")
	# file = open("Instancias/comp01.ctt", "r")

	problem, courses, rooms, curricula = read_file(file)

	create_teacher_curricula(courses, curricula)

	set_owner_curricula(courses, curricula)

	print_entries(problem, courses, rooms, curricula)

	trail = Trail(problem)

	trail.printTrail()

	trail.setTrail(1, 0, 1, 3)

	for i in courses:
		print(i.get_conflicts_names())
		print("\n")

	#
	# trail.printTrail()

	ant_walk(2, 8, trail, courses, problem)



