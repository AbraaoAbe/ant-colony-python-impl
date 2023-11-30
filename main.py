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
		self.different_days = []
		self.different_rooms = []

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

	#METODOS PARA A RESTRIÇÃO S2 - NÚMERO MÍNIMO DE DIAS DE AULA
	# Ao ser testado, deve ser utilizado em cópias da disciplina
	# Ao ser realmente alocado, deve ser utilizado na disciplina original
	def check_different_days(self, day):
		if day in self.different_days:
			return False
		else:
			return True

	def add_different_days(self, day):
		if self.check_different_days(day):
			self.different_days.append(day)

	def get_penalty_different_days(self):
		return self.min_days - len(self.different_days)

	def get_penalty_different_rooms(self):
		return len(self.different_rooms) - 1

	def add_different_rooms(self, room):
		if room not in self.different_rooms:
			self.different_rooms.append(room)

	def copy(self):
		return Course(self.name, self.teacher, self.classes_per_week, self.min_days, self.occupancy, self.index_in_trail)

	# Retorna uma lista com os nomes das disciplinas que possuem conflito com a disciplina atual
	def get_conflicts_names(self, just_curricula=False):
		courses_names = []
		if just_curricula:
			for i in self.curricula:
				if i.teacher == False:
					for j in i.courses:
						if j != self.name:
							courses_names.append(j)
		else:
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
	def __init__(self, name, size, courses, teacher=False):
		self.name = name
		self.size_courses = size
		self.courses = courses
		self.teacher = teacher

	def __str__(self):
		return "Nome: " + self.name + "\n" + "Tamanho: " + str(self.size_courses) + "\n" + "Disciplinas: " + str(self.courses) + "\n" + "Professor: " + str(self.teacher) + "\n"

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
			curricula.append(Curricula_and_Teacher(i.teacher, 1, [i.name], True))
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

	def getTrail(self, course, room, day, period):
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

	# Método para checar se a disciplina está isolada no mesmo dia das outras disciplinas do mesmo currículo
	def check_isolated_same_day(self, courses_indexes, problem, day):
		penality = 0
		for i in courses_indexes:
			for j in range(problem.rooms):
				for k in range(problem.periods_per_day):
					if self.matrix[i][(j * self.timeslots) + (day * self.periods) + k] != 0:
						break
			penality += 1



def ant_walk(alpha, beta, trail, courses, problem, rooms):
	not_visited = courses.copy()
	temporary_walk = Trail(problem)

	for i in range(len(not_visited)):
		#seleciona uma disciplina aleatória
		course = not_visited.pop(random.randrange(len(not_visited)))

		while course.not_allocated_classes > 0:
			#Retorna uma lista de slots viaveis para a disciplina
			feasible_list = get_feasible_list(temporary_walk, course, problem, courses)
			# Escolhe um slot da lista de slots viaveis dado a probabilidade de cada um
			slot = choose_slot(feasible_list, course, alpha, beta, temporary_walk, problem, trail, rooms)
			if True :
				break


#Retorna uma lista de slots viaveis para a disciplina que não violam as restrições fortes
def get_feasible_list(walk, course, problem, courses):
	courses_conflicts = course.get_conflicts_names()
	# print(course.name)
	courses_conflicts_indexes = get_courses_indexes(courses, courses_conflicts)
	# print(courses_conflicts_indexes)
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

def choose_slot(feasible_list, course, alpha, beta, walk, problem, trail, rooms):
	# Calcula a probabilidade de cada slot
	probabilities = []
	for i in feasible_list:
		probabilities.append(calculate_probability(i, course, alpha, beta, walk, problem, len(feasible_list), trail, rooms))
	# Escolhe um slot aleatório dado a probabilidade de cada um
	# print(probabilities)
	return feasible_list[0]

def calculate_probability(slot, course, alpha, beta, walk, problem, feasible_list_size, trail, rooms):
	# Calcula a probabilidade de um slot
	room, day, period = slot
	pheronome = trail.getTrail(course.index_in_trail, room, day, period)
	penality1 = soft_rule_1(slot, course, problem, rooms)
	# print(penality1)
	penality2 = soft_rule_2(slot, course)
	# print(penality2)
	penality3 = soft_rule_3(slot, course)
	# print(penality3)
	penality4 = soft_rule_4(slot, course)
	# print(penality4)

	return penality1



def soft_rule_1(slot, course, problem, rooms):
	# – S1-Capacidade de Sala: Para cada disciplina, o número de alunos que está
	# matriculado na disciplina deve ser menor ou igual ao número de assentos
	# disponíveis em todas as salas que ocorrem aulas dessa disciplina. Cada aluno
	# acima da capacidade conta como uma violação.
	penality = 0
	room, day, period = slot
	# Verifica se a capacidade da sala é menor que o número de alunos da disciplina
	if rooms[room].capacity < course.occupancy:
		penality += course.occupancy - rooms[room].capacity
	return penality

def soft_rule_2(slot, course):
	# – S2-Número Mínimo de Dias de Aula: As aulas de uma disciplina devem ser
	# espalhadas em um número mínimo de dias. Cada dia abaixo do número mínimo
	# de dias conta como uma violação.
	penality = 0
	room, day, period = slot
	# Cria uma copia temporaria da disciplina para não alterar a disciplina original
	temp_course = course.copy()
	# Adiciona o dia na lista de dias que a disciplina foi alocada
	temp_course.add_different_days(day)
	# Retorna o valor da penalidade da disciplina nesse quesito
	penality += temp_course.get_penalty_different_days()
	return penality

def soft_rule_3(slot, course):
	# – S3-Aulas Isoladas: Aulas de disciplinas de um mesmo currículo devem ser
	# adjacentes uma à outra. Para cada currículo, uma violação é contada quando há
	# uma aula não adjacente à nenhuma outra aula do mesmo currículo no mesmo dia.
	# Percorrer os curriculos daquela disciplina e verificar se as disciplinas pertencentes aquele curriculo estão no mesmo dia
	penality = 0
	room, day, period = slot
	# Cria uma copia temporaria da disciplina para não alterar a disciplina original
	temp_course = course.copy()

	same_curricula_courses = temp_course.get_conflicts_names(True)
	same_curricula_courses_indexes = get_courses_indexes(courses, courses_conflicts)

	# Verifica se a disciplina está isolada no mesmo dia das outras disciplinas do mesmo currículo
	penality += temp_course.check_isolated_same_day(same_curricula_courses_indexes, problem, day)

	return penality

def soft_rule_4(slot, course):
	# – S4-Estabilidade de Sala: Todas as aulas de uma disciplina devem acontecer
	# na mesma sala. Cada sala distinta usada para aulas dessa disciplina, além da
	# primeira, contam como uma violação.
	penality = 0
	room, day, period = slot
	# Cria uma copia temporaria da disciplina para não alterar a disciplina original
	temp_course = course.copy()
	# Adiciona a sala na lista de salas que a disciplina foi alocada
	temp_course.add_different_rooms(room)
	# Retorna o valor da penalidade da disciplina nesse quesito
	penality += temp_course.get_penalty_different_rooms()
	return penality


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

	#
	# trail.printTrail()

	ant_walk(2, 8, trail, courses, problem, rooms)



