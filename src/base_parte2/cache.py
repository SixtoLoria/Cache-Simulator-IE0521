from math import log2
import random

class cache:
    def __init__(self, cache_capacity, cache_assoc, block_size, repl_policy):
        #Escriba aquí el init de la clase
        # self.total_access = 0
        # self.total_misses = 0
        self.total_reads = 0            # Inicializa el total de lecturas
        self.total_read_misses = 0      # Inicializa el total de fallos de lectura
        self.total_writes = 0           # Inicializa el total de escrituras
        self.total_write_misses = 0     # Inicializa el total de fallos de escritura
            
        # Atributos del cache.
        self.cache_capacity = int(cache_capacity)
        self.cache_assoc = int(cache_assoc)
        self.block_size = int(block_size)
        self.repl_policy = repl_policy
        
        self.byte_offset_size = int(log2(self.block_size))                                           # Tamaño del offset en bytes
        self.num_sets = int((self.cache_capacity * 1024) / (self.block_size * self.cache_assoc))     # Número de sets
        self.index_size = int(log2(self.num_sets))                                                   # Tamaño del índice
        self.valid_table = [[False for _ in range(self.cache_assoc)] for _ in range(self.num_sets)]  # Tabla de validez
        self.tag_table = [[0 for _ in range(self.cache_assoc)] for _ in range(self.num_sets)]        # Tabla de etiquetas

        # la idea con LRU es implementarlo como una cola con la posibilidad de mover un elemento al final de la cola.
        # la primera posición de esta lista es el bloque MRU y la última posición de la lista es el bloque LRU.
        self.repl_table = [[x for x in range(self.cache_assoc)] for _ in range(self.num_sets)]       # Tabla de reemplazo

    def print_info(self):
        print("Parámetros del caché:")
        print("\tCapacidad:\t\t\t"+str(self.cache_capacity)+"kB")
        print("\tAssociatividad:\t\t\t"+str(self.cache_assoc))
        print("\tTamaño de Bloque:\t\t\t"+str(self.block_size)+"B")
        print("\tPolítica de Reemplazo:\t\t\t"+str(self.repl_policy))

    def print_stats(self):
        """Funcion que imprime y retorna los resultados

        Returns:
            results: int
            Resultados de total misses y miss rate
        """
        print("Resultados de la simulación")
        total_misses = self.total_read_misses + self.total_write_misses
        total_access = self.total_reads + self.total_writes

        miss_rate = 100*total_misses/total_access

        result = f'{total_misses} {miss_rate:.3f}%'
        print(result)
        return result # para poder automatizar

    def get_stats_csv(self):
        """
        Imprime los resultados de forma que puedan ser automatizados en CSV   
        """
        total_misses = self.total_read_misses + self.total_write_misses
        total_access = self.total_reads + self.total_writes

        miss_rate = 100*total_misses/total_access

        return f'{total_misses},{miss_rate:.3f}'

    def access(self, access_type, address):
        """Maneja el acceso al cache

        Args:
            access_type (int): tipo de acceso al cache
            address (int): direccion de acceso

        Returns:
            Miss: Cantidad de misses generados
        """
        # obtener el index y el tag
        index =  (address >> self.byte_offset_size) & (self.num_sets - 1)
        tag = address >> (self.byte_offset_size + self.index_size)

        set_number = self.find(index, tag)  # buscar el tag dentro del index

        miss = False

        # traer al cache el bloque en caso de miss
        if set_number == -1:
            self.bring_to_cache(index, tag)
            miss = True
            
            # self.total_misses += 1

            match access_type:
                case 'r': self.total_read_misses += 1
                case 'w': self.total_write_misses += 1
        
        # un acceso siempre actualiza el LRU, incluyendo hits
        else:
            # se busca en qué posición de la cola está el bloque y
            # se mueve a la primera posición (es decir, hacerlo MRU)
            block_index = self.repl_table[index].index(set_number)
            block = self.repl_table[index].pop(block_index)
            self.repl_table[index].insert(0, block)

        # self.total_access += 1
        match access_type:
            case 'r': self.total_reads += 1
            case 'w': self.total_writes += 1

        return miss

    def find(self, index, tag):
        """Busca una etiqueta en el conjunto dado

        Args:
            index (int): Indice del bloque buscado
            tag (int): Etiqueta del bloque
        """
        block_is_in_set = -1

        for set_number in range(self.cache_assoc):
            if self.valid_table[index][set_number] and (self.tag_table[index][set_number] == tag):
                block_is_in_set = set_number
                break

        return block_is_in_set
    
    def bring_to_cache(self, index, tag):
        """Se encarga de implementar las politicas de remplazo del cache

        Args:
            index (int): Indice del bloque buscado
            tag (int): Etiqueta del bloque
        """
        # buscar si hay un espacio vacío
        index_has_space = False

        for set_number in range(self.cache_assoc):
            if not self.valid_table[index][set_number]:
                index_has_space = True
                break
        
        # asignar bloque en espacio vacío
        if index_has_space:
            self.valid_table[index][set_number] = True
            self.tag_table[index][set_number] = tag

            # se busca en qué posición de la cola está el bloque y
            # se mueve a la primera posición (es decir, hacerlo MRU)
            block_index = self.repl_table[index].index(set_number)
            block = self.repl_table[index].pop(block_index)
            self.repl_table[index].insert(0, block)

        # si no, victimizar bloque
        else:
            # Politica LRU
            if self.repl_policy == 'l':

                # victmiza el bloque que está en la última posición
                # y lo trae a la primera posición (MRU)
                block = self.repl_table[index].pop()
                self.tag_table[index][block] = tag
                self.repl_table[index].insert(0, block)
