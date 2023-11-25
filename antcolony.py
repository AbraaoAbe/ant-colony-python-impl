import numpy as np


class AntColony:
	def __init__(self, distances, n_ants, n_best, n_iteration, decay, alpha=1, beta=2):
		"""
        Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=2
        """
		self.distances = distances
		self.pheromone = np.ones(self.distances.shape) / len(distances)
		self.all_inds = range(len(distances))
		self.n_ants = n_ants
		self.n_best = n_best
		self.n_iteration = n_iteration
		self.decay = decay
		self.alpha = alpha
		self.beta = beta

	def run(self):
		"""
        This main method to run the Ant Colony.
        Returns:
            tuple: (best_path, all_paths, all_costs)
        """
		best_path = None
		all_paths = []
		all_costs = []
		for i in range(self.n_iteration):
			paths = self.gen_all_paths()
			self.spread_pheronome(paths, self.n_best, self.distances)
			self.pheromone * self.decay
			self.intensify_pheronome(best_path, self.distances)
			best_path = min(paths, key=lambda x: self.path_cost(x, self.distances))
			all_paths.append(paths)
			all_costs.append(self.path_cost(best_path, self.distances))
		return best_path, all_paths, all_costs

	def spread_pheronome(self, paths, n_best, distances):
		"""
        At each iteration, the ants spread pheromone on the path they traveled
        The amount of pheromone spread is inversely proportional to the cost of the path.
        """
		sorted_paths = sorted(paths, key=lambda x: self.path_cost(x, distances))
		for path in sorted_paths[:n_best]:
			for move in path:
				self.pheromone[move] += 1.0 / self.path_cost(path, distances)

	def intensify_pheronome(self, best_path, distances):
		"""
        Pheronome intensification is depositing extra pheromone on the best path
        """
		for move in best_path:
			self.pheromone[move] += 1.0 / self.path_cost(best_path, distances)

	def gen_path_dist(self, path, distances):
		"""
        returns the total length of the path
        """
		total_dist = 0
		for ele in path:
			total_dist += distances[ele]
		return total_dist

	def gen_all_paths(self):
		"""
        Returns a list of all paths
        """
		all_paths = []
		for i in range(self.n_ants):
			path = self.gen_path_dist(range(len(self.distances)), self.distances)
			all_paths.append(path)
		return all_paths

	def path_cost(self, path, distances):
		"""
        Returns the cost of a particular path
        """
		total_dist = 0
		for ele in path:
			total_dist += distances[ele]
		return total_dist


# Exemplo de uso com o Problema do Caixeiro Viajante (TSP)
if __name__ == "__main__":
	# Matriz de distâncias para o TSP (substitua pelos valores do seu problema)
	distances = np.array([
		[0, 2, 2, 5, 7],
		[2, 0, 4, 8, 2],
		[2, 4, 0, 1, 3],
		[5, 8, 1, 0, 2],
		[7, 2, 3, 2, 0]
	])

	# Parâmetros do algoritmo ACO
	n_ants = 5
	n_best = 2
	n_iteration = 10
	decay = 0.6
	alpha = 1.0
	beta = 2.0

	# Criando uma instância do AntColony
	ant_colony = AntColony(distances, n_ants, n_best, n_iteration, decay, alpha, beta)

	# Executando o algoritmo ACO
	best_path, all_paths, all_costs = ant_colony.run()

	# Exibindo os resultados
	print("Melhor caminho:", best_path)
	print("Todos os caminhos:", all_paths)
	print("Custos de todos os caminhos:", all_costs)
