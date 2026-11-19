from shellsort import shell_sort
from quicksort import quick_sort
from heapsort import heap_sort
from radix import radix_sort
from interfaz import ejecutar_menu


if __name__ == "__main__":
    ejecutar_menu({
        1: ("ShellSort", shell_sort),
        2: ("QuickSort", quick_sort),
        3: ("HeapSort", heap_sort),
        4: ("Radix", radix_sort),
    })
