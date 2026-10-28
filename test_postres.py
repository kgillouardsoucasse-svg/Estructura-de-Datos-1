import contextlib
import io
import unittest
from unittest.mock import patch
from postres import (
    ListaIngredientes, Postre, alta_postre, baja_postre, buscar, consultar,
    datos_ejemplo, eliminar_ingrediente, eliminar_repetidos,
    insertar_ingredientes, main,
)


class PruebasPostres(unittest.TestCase):
    def setUp(self):
        self.postres = datos_ejemplo()

    def test_orden_inicial(self):
        self.assertEqual([p.nombre for p in self.postres],
                         ["Arroz con leche", "Flan", "Gelatina"])

    def test_consultar_existente(self):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            consultar(self.postres, "Flan")
        self.assertIn("Flan: Leche, Huevo, Azúcar", salida.getvalue())

    def test_consultar_lista_vacia(self):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            consultar(self.postres, "Gelatina")
        self.assertIn("Sin ingredientes", salida.getvalue())

    def test_operaciones_sobre_postre_inexistente(self):
        operaciones = [
            lambda: consultar(self.postres, "Otro"),
            lambda: insertar_ingredientes(self.postres, "Otro", ["Sal"]),
            lambda: eliminar_ingrediente(self.postres, "Otro", "Sal"),
            lambda: baja_postre(self.postres, "Otro"),
        ]
        for operacion in operaciones:
            with self.subTest(operacion=operacion):
                with self.assertRaisesRegex(ValueError, "no existe"):
                    operacion()

    def test_arreglo_vacio(self):
        with self.assertRaises(ValueError):
            buscar([], "Flan")
        vacio = []
        self.assertEqual(eliminar_repetidos(vacio), (0, 0))

    def test_normalizar_mayusculas_espacios(self):
        self.assertEqual(buscar(self.postres, "  ARROZ  con leche ").nombre,
                         "Arroz con leche")

    def test_insertar_en_lista_vacia(self):
        insertar_ingredientes(self.postres, "Gelatina", ["Agua", "Grenetina"])
        self.assertEqual(list(buscar(self.postres, "Gelatina").ingredientes),
                         ["Agua", "Grenetina"])

    def test_insertar_en_lista_no_vacia(self):
        insertar_ingredientes(self.postres, "Flan", ["Vainilla", "Leche"])
        self.assertEqual(list(buscar(self.postres, "Flan").ingredientes),
                         ["Leche", "Huevo", "Azúcar", "Vainilla", "Leche"])

    def test_insercion_invalida_no_modifica_lista(self):
        for entrada in ([], ["Canela", " "]):
            with self.assertRaises(ValueError):
                insertar_ingredientes(self.postres, "Gelatina", entrada)
            self.assertEqual(list(buscar(self.postres, "Gelatina").ingredientes), [])

    def test_eliminar_cabeza_medio_cola(self):
        for objetivo in ("Leche", "Huevo", "Azúcar"):
            with self.subTest(objetivo=objetivo):
                postres = datos_ejemplo()
                eliminar_ingrediente(postres, "Flan", objetivo)
                self.assertEqual(list(buscar(postres, "Flan").ingredientes),
                                 [x for x in ["Leche", "Huevo", "Azúcar"]
                                  if x != objetivo])

    def test_eliminar_unico_nodo(self):
        lista = ListaIngredientes(["Agua"])
        self.assertTrue(lista.eliminar("AGUA"))
        self.assertIsNone(lista.cabeza)

    def test_eliminar_inexistente_o_lista_vacia(self):
        for postre in ("Flan", "Gelatina"):
            with self.assertRaisesRegex(ValueError, "ingrediente no existe"):
                eliminar_ingrediente(self.postres, postre, "Cacao")

    def test_eliminar_solo_primera_coincidencia(self):
        lista = ListaIngredientes(["Agua", "Agua"])
        lista.eliminar("Agua")
        self.assertEqual(list(lista), ["Agua"])

    def test_alta_en_inicio_medio_final(self):
        postres = []
        for nombre in ["Flan", "Arroz", "Zanahoria", "Brownie"]:
            alta_postre(postres, nombre, [])
        self.assertEqual([p.nombre for p in postres],
                         ["Arroz", "Brownie", "Flan", "Zanahoria"])

    def test_orden_vocales_acentuadas_y_enie(self):
        postres = []
        for nombre in ["Oblea", "Ñame", "Nuez", "Éclair", "Flan"]:
            alta_postre(postres, nombre, [])
        self.assertEqual([p.nombre for p in postres],
                         ["Éclair", "Flan", "Nuez", "Ñame", "Oblea"])

    def test_alta_duplicada(self):
        with self.assertRaisesRegex(ValueError, "ya existe"):
            alta_postre(self.postres, " FLAN ", ["Chocolate"])
        self.assertEqual(len(self.postres), 3)

    def test_alta_invalida_es_atomica(self):
        for nombre, ingredientes in [(" ", []), ("Pastel", ["Harina", ""])]:
            with self.assertRaises(ValueError):
                alta_postre(self.postres, nombre, ingredientes)
        self.assertEqual(len(self.postres), 3)

    def test_nombres_vacios(self):
        for valor in ("", "  "):
            with self.assertRaises(ValueError):
                buscar(self.postres, valor)
            with self.assertRaises(ValueError):
                eliminar_ingrediente(self.postres, "Flan", valor)

    def test_baja_inicio_medio_final(self):
        for nombre in ["Arroz con leche", "Flan", "Gelatina"]:
            postres = datos_ejemplo()
            referencia = buscar(postres, nombre)
            baja_postre(postres, nombre)
            self.assertEqual(len(postres), 2)
            self.assertNotIn(nombre, [p.nombre for p in postres])
            self.assertIsNone(referencia.ingredientes.cabeza)

    def test_baja_unico_postre(self):
        postres = []
        alta_postre(postres, "Flan", ["Leche"])
        baja_postre(postres, "Flan")
        self.assertEqual(postres, [])

    def test_listas_independientes(self):
        baja_postre(self.postres, "Flan")
        self.assertIn("Leche", list(buscar(self.postres, "Arroz con leche").ingredientes))

    def test_repetidos_consecutivos_y_separados(self):
        lista = ListaIngredientes(["Agua", "AGUA", "Sal", "Agua", "Sal"])
        self.assertEqual(lista.quitar_repetidos(), 3)
        self.assertEqual(list(lista), ["Agua", "Sal"])
        self.assertIsNone(lista.cabeza.siguiente.siguiente)

    def test_sin_repetidos_y_lista_vacia(self):
        for valores in ([], ["Agua"], ["Agua", "Sal"]):
            lista = ListaIngredientes(valores)
            self.assertEqual(lista.quitar_repetidos(), 0)
            self.assertEqual(list(lista), valores)

    def test_fusion_conserva_ingredientes_y_arreglo(self):
        postres = [
            Postre("Flan", ListaIngredientes(["Leche", "Huevo", "Leche"])),
            Postre("flan", ListaIngredientes(["Azúcar", "Huevo"])),
            Postre("Gelatina"),
        ]
        referencia = postres
        self.assertEqual(eliminar_repetidos(postres), (1, 2))
        self.assertIs(referencia, postres)
        self.assertEqual([p.nombre for p in postres], ["Flan", "Gelatina"])
        self.assertEqual(list(postres[0].ingredientes), ["Leche", "Huevo", "Azúcar"])
        self.assertEqual(eliminar_repetidos(postres), (0, 0))

    def test_tres_postres_duplicados_con_lista_vacia(self):
        postres = [Postre("Flan"), Postre("FLAN", ListaIngredientes(["Leche"])),
                   Postre("flan", ListaIngredientes(["Leche", "Huevo"]))]
        self.assertEqual(eliminar_repetidos(postres), (2, 1))
        self.assertEqual(list(postres[0].ingredientes), ["Leche", "Huevo"])

    def test_menu_invalido_error_y_salida(self):
        salida = io.StringIO()
        with patch("builtins.input", side_effect=["x", "1", "Otro", "0"]):
            with contextlib.redirect_stdout(salida):
                main()
        self.assertIn("Opción inválida", salida.getvalue())
        self.assertIn("Error: El postre no existe", salida.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
