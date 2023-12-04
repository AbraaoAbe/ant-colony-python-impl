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
		#TODO: atualizar na lista courses original essas duas listas após alocar
		self.different_days = []
		self.different_rooms = []
		self.all_days = []
		self.all_rooms = []
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
		#Adiciona na lista com todos os dias
		self.all_days.append(day)

	def get_penalty_different_days(self):
		return self.min_days - len(self.different_days)

	def remove_different_days(self, day):
		self.different_days.remove(day)
		#Remove somente 1 dia da lista com todos os dias
		self.all_days.remove(day)

	def get_penalty_different_rooms(self):
		return len(self.different_rooms) - 1

	def add_different_rooms(self, room):
		if room not in self.different_rooms:
			self.different_rooms.append(room)
		#Adiciona na lista com todas as salas
		self.all_rooms.append(room)

	def remove_different_rooms(self, room):
		self.different_rooms.remove(room)
		#Remove somente 1 sala da lista com todas as salas
		self.all_rooms.remove(room)

	# Método que checa a unicidade do dia na alocação
	def check_unique_day(self, day):
		cout = 0
		for i in self.all_days:
			if i == day:
				cout += 1

		if cout == 1:
			return True
		else:
			return False

	def check_unique_room(self, room):
		cout = 0
		for i in self.all_rooms:
			if i == room:
				cout += 1

		if cout == 1:
			return True
		else:
			return False

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
	def __init__(self, problem, value=0):
		self.timeslots = problem.days * problem.periods_per_day
		self.periods = problem.periods_per_day
		self.matrix = [[value for i in range(problem.rooms * self.timeslots)] for j in range(problem.courses)]

	def setTrail(self, course, room, day, period, value=1):
		self.matrix[course][(room * self.timeslots) + (day * self.periods) + period] = value

	def getTrail(self, course, room, day, period):
		return self.matrix[course][(room * self.timeslots) + (day * self.periods) + period]

	def updateTrail(self, best_list_allocated, best_value, global_value):
		reward = 1 / (1 + global_value - best_value)
		# Manter os updates positivos
		if reward < 0:
			reward = reward * -1

		for i in best_list_allocated:
			index_course, room, day, period = i
			actual_trail = self.getTrail(index_course, room, day, period)
			self.setTrail(index_course, room, day, period, actual_trail + reward)

	def evaporateTrail(self, rho, tmin, tmax, problem):
		for i in range(problem.courses):
			for j in range(problem.rooms * self.timeslots):
				actual_trail = self.matrix[i][j]
				new_trail = actual_trail * (1 - rho)
				if new_trail < tmin:
					new_trail = tmin
				elif new_trail > tmax:
					new_trail = tmax
				self.matrix[i][j] = new_trail


	def printTrail(self):
		for i in range(problem.courses):
			print(self.matrix[i])
		print("\n")

	def printTrailExpressive(self, problem, courses, rooms, list_allocated):
		for i in list_allocated:
			index_course, room, day, period = i
			print("Disciplina: " + courses[index_course].name + " Sala: " + rooms[room].name + " Dia: " + str(day) + " Período: " + str(period))
		print("\n")


	def check_available(self, course, room, day, period, problem):
		# Verifica se o slot está disponível para todas as disciplinas
		for i in range(problem.courses):
			if i == course:
				continue
			elif self.getTrail(i, room, day, period) != 0:
				return False
		return True

	# Método para verificar as disciplinas que possuem conflito de período com a disciplina atual
	# Ela checa o mesmo horário em todas as salas no mesmo período
	def check_conflicts_same_period(self, courses_indexes, problem, day, period):
		allrooms = problem.rooms
		for i in range(allrooms):
			for j in courses_indexes:
				if self.getTrail(j, i, day, period) != 0:
					return False
		return True

	# Método para checar se a disciplina está isolada no mesmo dia das outras disciplinas do mesmo currículo
	def check_isolated(self, courses_indexes, problem, slot):
		penality = 0
		room, day, period = slot
		adjacent1, adjacent2 = period - 1, period + 1

		count_isolated = 0
		# Verifica se a disciplina está isolada das outras disciplinas do mesmo currículo
		if period == 0:
			for i in courses_indexes:
				if self.getTrail(i, room, day, adjacent2) == 0:
					count_isolated += 1
		elif period == problem.periods_per_day - 1:
			for i in courses_indexes:
				if self.getTrail(i, room, day, adjacent1) == 0:
					count_isolated += 1
		else:
			for i in courses_indexes:
				if self.getTrail(i, room, day, adjacent1) == 0 or self.getTrail(i, room, day, adjacent2) == 0:
					count_isolated += 1

		# Retorna o booleano se a disciplina está isolada ou não
		if count_isolated == len(courses_indexes):
			return True
		else:
			return False

	def copy(self):
		new_trail = Trail(problem)
		for i in range(problem.courses):
			for j in range(problem.rooms * self.timeslots):
				new_trail.matrix[i][j] = self.matrix[i][j]
		return new_trail


def update_course(courses_original, courses_updated):
	for i in courses_updated:
		for j in courses_original:
			if i.name == j.name:
				j.not_allocated_classes = i.not_allocated_classes
				j.different_days = i.different_days
				j.different_rooms = i.different_rooms
				break

def ant_colony_optimization(n_cycles, n_ants, problem, courses, rooms):
	alpha = 2
	beta = 5
	rho = 0.05
	tmin = 0.01
	tmax = 10
	g_best = 99999999999
	g_best_trail_walk = []
	g_best_list_allocated = []

	# Inicializa a trilha de feromonio
	trail_feromone = Trail(problem, tmax)
	same_best_generation = 0
	same_best_improvement = 0

	# Fase de construção das soluções
	for i in range(n_cycles):
		solution_ant = []
		for j in range(n_ants):
			solution_ant.append(ant_walk_generate(alpha, beta, trail_feromone, courses, problem, rooms))

		# Retorna a melhor solução das formigas
		c_best = get_best_solution(solution_ant, courses, problem, rooms)
		best_trail_walk, best_list_allocated, best_value, best_solution_courses = c_best

		# Faça um while se em 10 tentativas não houver melhoria, pare
		while same_best_improvement < 10:
			# Fase de melhoria das soluções
			best_value, best_list_allocated, best_trail_walk = ant_walk_improve( best_trail_walk, best_list_allocated, best_value, courses, problem)
			# Imprime a solução atual
			print("Melhor solução:")
			best_trail_walk.printTrailExpressive(problem, courses, rooms, best_list_allocated)
			print("Penalidade:")
			print(best_value)
			# Se a nova solução for melhor, atualiza a melhor solução
			if best_value < g_best:
				g_best = best_value
				g_best_trail_walk = best_trail_walk
				g_best_list_allocated = best_list_allocated
				same_best_improvement = 0
			else:
				same_best_improvement += 1

		# Se a nova solução for melhor, atualiza a melhor solução
		if best_value < g_best:
			g_best = best_value
			g_best_trail_walk = best_trail_walk
			g_best_list_allocated = best_list_allocated
			same_best_generation = 0

		# Atualiza a trilha de feromonio
		trail_feromone.updateTrail(best_list_allocated, best_value, g_best)
		# Evapora a trilha de feromonio
		trail_feromone.evaporateTrail(rho, tmin, tmax, problem)
		print("Melhor solução global:")
		g_best_trail_walk.printTrailExpressive(problem, courses, rooms, g_best_list_allocated)
		print("Penalidade:")
		print(g_best)

def ant_walk_improve( best_trail_walk, best_list_allocated, best_value, courses, problem):
	aux_best_list_alocated = best_list_allocated.copy()
	aux_best_trail_walk = best_trail_walk.copy()

	# Sorteia 1 alocação da best_list_allocated
	allocated = random.choice(aux_best_list_alocated)
	al_course, al_room, al_day, al_period = allocated
	# Sorteia 1 sala, 1 dia e 1 periodo aleatório
	random_room = random.randrange(problem.rooms)
	random_day = random.randrange(problem.days)
	random_period = random.randrange(problem.periods_per_day)
	# Verifica se o slot sorteado está ou não ocupado
	if aux_best_trail_walk.check_available(al_course, random_room, random_day, random_period, problem):
		# Avalia o efeito do move e executa caso seja melhor que a solução atual
		# Se for melhor, atualiza a melhor solução
		course = courses[al_course]
		move(aux_best_trail_walk, course, problem, courses, random_room, random_day, random_period)
		# Modifica o allocated para o novo slot
		aux_best_list_alocated.remove(allocated)
		aux_best_list_alocated.append([al_course, random_room, random_day, random_period])
		# Avalia a nova solução
		value, updated_courses = evaluate_solution(aux_best_list_alocated, courses, problem, rooms, aux_best_trail_walk)
	#Faz um swap
	else:
		course_a = courses[al_course]
		# Busca o curso alocado na lista de alocações
		for i in aux_best_list_alocated:
			index_course, room, day, period = i
			if room == random_room and day == random_day and period == random_period:
				course_b = courses[index_course]
				break
		if course_b == []:
			throw("Erro: curso não encontrado")

		# Cria os dois slots a serem trocados do course_a e course_b
		slot_a = [al_room, al_day, al_period]
		slot_b = [random_room, random_day, random_period]
		# Faz o swap
		swap(aux_best_trail_walk, course_a, course_b, problem, courses, slot_a, slot_b)
		# Modifica o allocated para o novo slot
		aux_best_list_alocated.remove(allocated)
		aux_best_list_alocated.append([al_course, room, day, period])
		# Avalia a nova solução
		value, updated_courses = evaluate_solution(aux_best_list_alocated, courses, problem, rooms, aux_best_trail_walk)

	# Se a nova solução for melhor, atualiza a melhor solução
	if value < best_value:
		update_course(courses, updated_courses)
		return value, aux_best_list_alocated, aux_best_trail_walk
	else:
		return best_value, best_list_allocated, best_trail_walk

def move(best_trail, course, problem, courses, room, day, period):
	# Dado uma disciplina, retorna uma lista de disciplinas conflitantes
	courses_conflicts = course.get_conflicts_names()
	courses_conflicts_indexes = get_courses_indexes(courses, courses_conflicts)

	if course.check_constraint_matrix(day, period) \
			and best_trail.check_conflicts_same_period(courses_conflicts_indexes, problem, day, period):
		# Se o slot sorteado estiver disponível, aloca a disciplina no slot escolhido
		best_trail.setTrail(course.index_in_trail, room, day, period)
		# Adiciona o dia na lista de dias que a disciplina foi alocada
		course.add_different_days(day)
		# Adiciona a sala na lista de salas que a disciplina foi alocada
		course.add_different_rooms(room)
		# Limpa a alocação antiga
		best_trail = clear_allocated(course, room, day, period, best_trail)


def swap(best_trail, course_a, course_b, problem, courses, slot_a, slot_b):
	# Dado uma disciplina, retorna uma lista de disciplinas conflitantes
	courses_conflicts_a = course_a.get_conflicts_names()
	courses_conflicts_indexes_a = get_courses_indexes(courses, courses_conflicts_a)
	courses_conflicts_b = course_b.get_conflicts_names()
	courses_conflicts_indexes_b = get_courses_indexes(courses, courses_conflicts_b)

	room_a, day_a, period_a = slot_a
	room_b, day_b, period_b = slot_b

	verif_1 = best_trail.check_available(course_a.index_in_trail, room_b, day_b, period_b, problem)
	verif_2 = best_trail.check_available(course_b.index_in_trail, room_a, day_a, period_a, problem)
	verif_3 = best_trail.check_conflicts_same_period(courses_conflicts_indexes_a, problem, day_b, period_b)
	verif_4 = best_trail.check_conflicts_same_period(courses_conflicts_indexes_b, problem, day_a, period_a)

	if verif_1 and verif_2 and verif_3 and verif_4:
		# Se os slots sorteados estiverem disponíveis, aloca a disciplina no slot escolhido
		best_trail.setTrail(course_a.index_in_trail, room_b, day_b, period_b)
		best_trail.setTrail(course_b.index_in_trail, room_a, day_a, period_a)
		# Adiciona o dia na lista de dias que a disciplina foi alocada
		course_a.add_different_days(day_b)
		course_b.add_different_days(day_a)
		# Adiciona a sala na lista de salas que a disciplina foi alocada
		course_a.add_different_rooms(room_b)
		course_b.add_different_rooms(room_a)
		# Limpa a alocação antiga
		best_trail = clear_allocated(course_a, room_a, day_a, period_a, best_trail)
		best_trail = clear_allocated(course_b, room_b, day_b, period_b, best_trail)




def clear_allocated(course, room, day, period, best_trail):
	# Limpa a alocação de uma disciplina em um slot
	best_trail.setTrail(course.index_in_trail, room, day, period, 0)
	# Remove o dia da lista de dias que a disciplina foi alocada
	if course.check_unique_day(day):
		course.remove_different_days(day)
	# Remove a sala da lista de salas que a disciplina foi alocada
	if course.check_unique_room(room):
		course.remove_different_rooms(room)

	return best_trail

def ant_walk_generate(alpha, beta, trail, courses, problem, rooms):
	not_visited = []
	for i in courses:
		not_visited.append(i.copy())

	temporary_walk = Trail(problem)
	list_allocated = []

	for i in range(len(not_visited)):
		#seleciona uma disciplina aleatória
		course = not_visited.pop(random.randrange(len(not_visited)))

		while course.not_allocated_classes > 0:
			#Retorna uma lista de slots viaveis para a disciplina
			feasible_list = get_feasible_list(temporary_walk, course, problem, courses)
			# Escolhe um slot da lista de slots viaveis dado a probabilidade de cada um
			slot = choose_slot(feasible_list, course, alpha, beta, temporary_walk, problem, trail, rooms)
			# Aloca a disciplina no slot escolhido
			room, day, period = slot
			temporary_walk.setTrail(course.index_in_trail, room, day, period)
			# Lista para função de avaliação de qualidade
			list_allocated.append([course.index_in_trail, room, day, period])
			# Decrementa o número de aulas não alocadas da disciplina
			course.not_allocated_classes -= 1

	return temporary_walk, list_allocated

#Retorna uma lista de slots viaveis para a disciplina que não violam as restrições fortes
def get_feasible_list(walk, course, problem, courses):
	# Dado uma disciplina, retorna uma lista de disciplinas conflitantes
	courses_conflicts = course.get_conflicts_names()
	courses_conflicts_indexes = get_courses_indexes(courses, courses_conflicts)
	feasible_list = []
	# Percorre todas as salas, dias e períodos
	for i in range(problem.rooms):
		for j in range(problem.days):
			for k in range(problem.periods_per_day):
				if walk.check_available(course.index_in_trail, i, j, k, problem) \
						and walk.check_conflicts_same_period(courses_conflicts_indexes, problem, j, k) \
						and course.check_constraint_matrix(j, k):
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
		probabilities.append(calculate_probability(i, course, alpha, beta, walk, problem, trail, rooms))

	sumProbabilities = sum(probabilities)

	# Normaliza as probabilidades
	probabilities_normalized = []
	for i in probabilities:
		probabilities_normalized.append(i / sumProbabilities)

	# Escolhe um slot aleatório dado as probabilidades
	slot = random.choices(feasible_list, probabilities_normalized)[0]
	return slot

def calculate_probability(slot, course, alpha, beta, walk, problem, trail, rooms):
	# Calcula a probabilidade de um slot
	room, day, period = slot
	pheronome = trail.getTrail(course.index_in_trail, room, day, period)
	penality1 = soft_rule_1(slot, course, problem, rooms)
	# print(penality1)
	penality2 = soft_rule_2(slot, course)
	# print(penality2)
	penality3 = soft_rule_3(slot, course, walk, problem)
	# print(penality3)
	penality4 = soft_rule_4(slot, course)
	# print(penality4)
	all_penality = penality1 + (penality2*5) + (penality3*2) + penality4
	if all_penality == 0:
		value = pheronome ** alpha
	else:
		value = (pheronome ** alpha) + ((1/all_penality) ** beta)
	return value

def evaluate_solution(list_allocated, courses, problem, rooms, walk):
	penality = 0
	aux_courses = []
	for i in courses:
		aux_courses.append(i.copy())

	for i in list_allocated:
		index_course, room, day, period = i
		penality += soft_rule_1([room, day, period], aux_courses[index_course], problem, rooms)
		penality += (soft_rule_2([room, day, period], aux_courses[index_course]) * 5)
		penality += (soft_rule_3([room, day, period], aux_courses[index_course], walk, problem) * 2)
		penality += soft_rule_4([room, day, period], aux_courses[index_course])
	return penality, aux_courses

#TODO: A melhor solução tem que escrever diretamente em courses, pois é a solução final
def get_best_solution(solution_ant, courses, problem, rooms):
	best_value = 99999999999
	best_solution = []
	best_trail = []
	best_solution_courses = []


	for i in solution_ant:
		trail, list_allocated = i
		value, updated_courses = evaluate_solution(list_allocated, courses, problem, rooms, trail)

		if value < best_value:
			best_value = value
			best_list_allocated = list_allocated
			best_trail = trail
			best_solution_courses = updated_courses

	# print("Melhor solução:")
	# best_trail.printTrailExpressive(problem, courses, rooms, best_list_allocated)
	# print("Penalidade:")
	# print(best_value)
	return best_trail, best_list_allocated, best_value, best_solution_courses

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
	# Adiciona o dia na lista de dias que a disciplina foi alocada
	course.add_different_days(day)
	# Retorna o valor da penalidade da disciplina nesse quesito
	penality += course.get_penalty_different_days()
	return penality

def soft_rule_3(slot, course, walk, problem):
	# – S3-Aulas Isoladas: Aulas de disciplinas de um mesmo currículo devem ser
	# adjacentes uma à outra. Para cada currículo, uma violação é contada quando há
	# uma aula não adjacente à nenhuma outra aula do mesmo currículo no mesmo dia.
	# Percorrer os curriculos daquela disciplina e verificar se as disciplinas pertencentes aquele curriculo estão no mesmo dia
	penality = 0
	room, day, period = slot

	same_curricula_courses = course.get_conflicts_names(True)
	same_curricula_courses_indexes = get_courses_indexes(courses, same_curricula_courses)

	# Verifica se a disciplina está isolada no mesmo dia das outras disciplinas do mesmo currículo
	if walk.check_isolated(same_curricula_courses_indexes, problem, slot):
		penality += 1

	return penality

def soft_rule_4(slot, course):
	# – S4-Estabilidade de Sala: Todas as aulas de uma disciplina devem acontecer
	# na mesma sala. Cada sala distinta usada para aulas dessa disciplina, além da
	# primeira, contam como uma violação.
	penality = 0
	room, day, period = slot
	# Adiciona a sala na lista de salas que a disciplina foi alocada
	course.add_different_rooms(room)
	# Retorna o valor da penalidade da disciplina nesse quesito
	penality += course.get_penalty_different_rooms()
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
	# file = open("Instancias/toy.ctt", "r")
	file = open("Instancias/comp01.ctt", "r")

	problem, courses, rooms, curricula = read_file(file)
	# Transforma o nome do professor em um currículo
	create_teacher_curricula(courses, curricula)
	# Atribui o curriculo de cada disciplina para a disciplina
	set_owner_curricula(courses, curricula)

	ant_colony_optimization(10, 5, problem, courses, rooms)


