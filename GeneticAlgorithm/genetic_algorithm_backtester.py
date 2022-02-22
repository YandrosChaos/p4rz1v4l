from Abstract.abstract_genetic_algorithm import AbstractGeneticAlgorithm

from GeneticAlgorithm.classes.individual import Individual

from GeneticAlgorithm.factory.population_factory import PopulationFactory
from Strategy.factory.genetic_strategy_factory import GeneticStrategyFactory

from Data.exchange_factory import ExchangeFactory
from Data.exchange_query import ExchangeQuery
from Data.exchange_service import ExchangeService


def build_strategy(strategy_key: str, individual: Individual):
    strategy_factory: GeneticStrategyFactory = GeneticStrategyFactory(strategy_key, individual)
    return strategy_factory.get_instance()


class GeneticAlgorithmBacktester(AbstractGeneticAlgorithm):

    def __init__(self, strategy_key: str, number_of_generations=20, generation_size=50, mutation_rate=0.1):
        self.strategy_key = strategy_key
        exchange = ExchangeFactory().getInstance()
        self.query = ExchangeQuery()
        self.dataframe = ExchangeService(exchange).getAll(self.query)
        self.number_of_generations: int = int(number_of_generations)
        self.generation_size: int = int(generation_size)
        self.n_genes: int = 5
        self.mutation_rate: float = float(mutation_rate)
        self.population = self.build_population()

    def param_request(self):
        self.number_of_generations = int(input(' -> Number of generations (20): ') or '20')
        self.generation_size = int(input(' -> Generation size (50): ') or '50')
        self.mutation_rate = float(input(' -> Set mutation rate (0.1): ') or '0.1')

    def print_header(self):
        print('<>--< GENETIC ALGORITHM >--<>')
        print()
        print('Use: optimize QUANT strategy')
        print('Symbol: ', self.query.symbol, 'Timeframe: ', self.query.timeframe)
        print('\n\n')

    def run(self):
        for x in range(self.number_of_generations):
            for individual in self.population.population:
                individual.backtester.reset_results()
                strategy = build_strategy(self.strategy_key, individual)
                strategy.set_up(self.dataframe)
                individual.backtester.__backtesting__(self.dataframe, strategy)
            self.population.crossover()
            self.population.mutation()
            self.sort_population()
            self.print_result(x)

    def sort_population(self):
        self.population.population = sorted(
            self.population.population,
            key=lambda indiv: indiv.backtester.return_results(
                symbol=self.query.symbol,
                start_date='-',
                end_date='-',
            )['fitness_function'],
            reverse=True
        )

    def print_result(self, generation_number):
        print()
        print('GENERATION: ', generation_number)
        print('_________________')
        print('\n\n')
        self.print_best_individual()
        self.print_worst_individual()

    def print_best_individual(self):
        print('BEST INDIVIDUAL:')
        print(self.population.population[0].backtester.return_results(
            symbol=self.query.symbol,
            start_date='',
            end_date=''
        ))
        print(self.population.population[0].genes)
        print('\n')

    def build_population(self):
        population_factory = PopulationFactory(self.strategy_key, self.generation_size, self.mutation_rate)
        return population_factory.get_instance()

    def print_worst_individual(self):
        print('WORST INDIVIDUAL:')
        print(self.population.population[-1].backtester.return_results(
            symbol=self.query.symbol,
            start_date='',
            end_date=''
        ))
        print(self.population.population[-1].genes)
