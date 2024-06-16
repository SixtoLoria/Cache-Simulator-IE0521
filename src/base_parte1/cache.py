

from math import log2, floor
import random

class cache:
    def __init__(self, cache_capacity, cache_assoc, block_size, repl_policy):
        #Escriba aquí el init de la clase
        self.total_access = 0
        self.total_misses = 0
        self.total_reads = 0            # Inicializa el total de lecturas
        self.total_read_misses = 0      # Inicializa el total de fallos de lectura
        self.total_writes = 0           # Inicializa el total de escrituras
        self.total_write_misses = 0     # Inicializa el total de fallos de escritura
            
        # Atributos del cache.
        self.cache_capacity = int(cache_capacity)
        self.cache_assoc = int(cache_assoc)
        self.block_size = int(block_size)
        self.repl_policy = repl_policy
        
        self.byte_offset_size = log2(self.block_size)                                                # Tamaño del offset en bytes
        self.num_sets = int((self.cache_capacity * 1024) / (self.block_size * self.cache_assoc))     # Número de conjuntos
        self.index_size = int(log2(self.num_sets))                                                   # Tamaño del índice
        self.valid_table = [[False for _ in range(self.cache_assoc)] for _ in range(self.num_sets)]  # Tabla de validez
        self.tag_table = [[0 for _ in range(self.cache_assoc)] for _ in range(self.num_sets)]        # Tabla de etiquetas
        self.repl_table = [[0 for _ in range(self.cache_assoc)] for _ in range(self.num_sets)]       # Tabla de reemplazo

    def print_info(self):
        print("Parámetros del caché:")
        print("\tCapacidad:\t\t\t"+str(self.cache_capacity)+"kB")
        print("\tAssociatividad:\t\t\t"+str(self.cache_assoc))
        print("\tTamaño de Bloque:\t\t\t"+str(self.block_size)+"B")
        print("\tPolítica de Reemplazo:\t\t\t"+str(self.repl_policy))

    def print_stats(self):  # Imprime las estadísticas de la simulación
        print("Resultados de la simulación")
        miss_rate = (100.0 * self.total_misses) / self.total_access  # Calcula la tasa de fallos
        miss_rate = "{:.3f}".format(miss_rate)                      # Formatea la tasa de fallos
        read_miss_rate = (100.0 * self.total_read_misses) / self.total_reads  # Calcula la tasa de fallos de lectura
        read_miss_rate = "{:.3f}".format(read_miss_rate)            # Formatea la tasa de fallos de lectura
        write_miss_rate = (100.0 * self.total_write_misses) / self.total_writes  # Calcula la tasa de fallos de escritura
        write_miss_rate = "{:.3f}".format(write_miss_rate)  # Formatea la tasa de fallos de escritura
        stats = (f"{self.total_misses} {miss_rate}%") #+
                 #f"{self.total_read_misses},{read_miss_rate}%," +
                 #f"{self.total_write_misses},{write_miss_rate}%")
        print(stats)

    def access(self, access_type, address):
        """Maneja el acceso al cache

        Args:
            access_type (_type_): _description_
            address (_type_): _description_

        Returns:
            Miss: Cantidad de misses generados
        """
        byte_offset = int(address % (2 ** self.byte_offset_size))  # Calcula el offset de bytes
        index = int(floor(address / (2 ** self.byte_offset_size)) % (2 ** self.index_size))  # Calcula el índice
        tag = int(floor(address / (2 ** (self.byte_offset_size + self.index_size))))  # Calcula la etiqueta
        line = self.find(index, tag)  # Busca la línea en el caché
        miss = False
        if line == -1:  # Si la línea no está en el caché
            self.bring_to_cache(index, tag)  # Trae la línea al caché
            self.total_misses += 1
            if access_type == "r":
                self.total_read_misses += 1
            else:
                self.total_write_misses += 1
            miss = True
        self.total_access += 1
        if access_type == "r":
            self.total_reads += 1
        else:
            self.total_writes += 1
        return miss

    def find(self, index, tag):
        """Busca una etiqueta en el conjunto dado

        Args:
            index (_type_): Indice del bloque buscado
            tag (_type_): Etiqueta del bloque
        """
        for line in range(self.cache_assoc):
            if self.valid_table[index][line] and (self.tag_table[index][line] == tag):
                return line
        return -1
    
    def bring_to_cache(self, index, tag):
        empty_slot_found = False
        for i in range(self.cache_assoc):
            if not self.valid_table[index][i]:
                self.valid_table[index][i] = True
                self.tag_table[index][i] = tag
                self.repl_table[index][i] = self.cache_assoc - 1
                empty_slot_found = True
                break

        if not empty_slot_found:
            # Politica LRU
            if self.repl_policy == 'l':
                lru_index = self.repl_table[index].index(min(self.repl_table[index]))
                self.tag_table[index][lru_index] = tag
                self.repl_table[index][lru_index] = self.cache_assoc - 1
            # Politica Random
            elif self.repl_policy == 'r':
                random_index = random.randint(0, self.cache_assoc - 1)
                self.tag_table[index][random_index] = tag
                self.repl_table[index][random_index] = self.cache_assoc - 1

        if self.repl_policy == 'l':
            for i in range(self.cache_assoc):
                if self.repl_table[index][i] != 0:
                    self.repl_table[index][i] -= 1
    
    
