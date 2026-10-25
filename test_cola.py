import unittest

from cola import Cola


class PruebasCola(unittest.TestCase):
    def test_respeta_el_orden_fifo(self):
        cola = Cola()
        cola.encolar("primero")
        cola.encolar("segundo")
        cola.encolar("tercero")

        self.assertEqual(cola.frente(), "primero")
        self.assertEqual(cola.desencolar(), "primero")
        self.assertEqual(cola.desencolar(), "segundo")
        self.assertEqual(cola.tamano(), 1)
        self.assertFalse(cola.esta_vacia())
        self.assertEqual(cola.desencolar(), "tercero")
        self.assertTrue(cola.esta_vacia())

    def test_vaciar_actualiza_el_final(self):
        cola = Cola()
        cola.encolar(1)
        cola.desencolar()
        cola.encolar(2)

        self.assertEqual(cola.desencolar(), 2)
        with self.assertRaises(IndexError):
            cola.desencolar()


if __name__ == "__main__":
    unittest.main() 
