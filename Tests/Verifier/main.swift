import Foundation
import BoletaCore

// Este programa prueba el modelo sin abrir la app. Si una comparación falla,
// se detiene para evitar informar como correcto un cálculo que no coincide.
var verificaciones = 0
func comprobar(_ condicion: @autoclosure () -> Bool, _ mensaje: String) {
    verificaciones += 1
    guard condicion() else { fatalError("FALLO: \(mensaje)") }
}
func d(_ s: String) -> Decimal { Decimal(string: s)! }
// Aquí esperamos un error: pasar la prueba significa rechazar el dato inválido.
func rechaza(_ datos: DatosBoleta) {
    do { _ = try Boleta().calcular(datos); fatalError("Se aceptó entrada inválida") }
    catch { verificaciones += 1 }
}

// fixtures.json guarda entradas y resultados esperados de los casos de la guía
// y escenarios adicionales. Puede indicarse otra ruta como argumento del comando.
let ruta = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "Tests/fixtures.json"
let fixtures = try JSONSerialization.jsonObject(with: Data(contentsOf: URL(fileURLWithPath: ruta))) as! [[String: Any]]
var salida = [[String: Any]]()
for f in fixtures {
    // Para cada caso construimos los datos y llamamos a la misma clase que usa iOS.
    let entrada = f["input"] as! [String: Any]
    let datos = DatosBoleta(sueldo: d(entrada["sueldo"] as! String), dias: entrada["dias"] as! Int,
        hijos: entrada["hijos"] as! Bool, sistema: Sistema(rawValue: entrada["sistema"] as! String)!,
        afp: entrada["afp"] as! String, horas25: d(entrada["horas25"] as! String),
        horas35: d(entrada["horas35"] as! String), adelantos: d(entrada["adelantos"] as! String))
    let b = try Boleta().calcular(datos)
    // map(\.monto) extrae el importe de cada fila. Comparamos todos los conceptos,
    // totales, neto y costo; revisar solo el neto podría ocultar errores compensados.
    let valores = b.remuneraciones.map(\.monto) + [b.totalRemuneraciones] + b.descuentos.map(\.monto) + [b.totalDescuentos, b.neto, b.aportaciones[0].monto, b.costoEmpleador]
    let esperado = f["expected"] as! [String]
    comprobar(valores.count == esperado.count, "Cantidad de conceptos")
    for (i, valor) in valores.enumerated() { comprobar(valor == d(esperado[i]), "\(f["name"]!) concepto \(i): \(valor) != \(esperado[i])") }
    salida.append(["name": f["name"]!, "values": valores.map { NSDecimalNumber(decimal: $0).stringValue }])
}
// También se prueba que el modelo rechace importes, días y AFP inválidos.
let base = DatosBoleta(sueldo: 2500, dias: 30, hijos: false, sistema: .onp)
for sueldo in [Decimal(0), -1, Decimal.nan, d("2500.001"), 100_000_001] { var x = base; x.sueldo = sueldo; rechaza(x) }
for dias in [0, -1, 31] { var x = base; x.dias = dias; rechaza(x) }
for valor in [Decimal(-1), Decimal.nan, d("0.001"), 10001] { var x = base; x.horas25 = valor; rechaza(x); x = base; x.horas35 = valor; rechaza(x) }
var invalido = base; invalido.sistema = .afp; invalido.afp = "inexistente"; rechaza(invalido)
for valor in [Decimal(-1), Decimal.nan, d("1.001"), 100_000_001] { var x = base; x.adelantos = valor; rechaza(x) }
// Estos textos no cumplen el formato que aceptan los campos de la aplicación.
for texto in ["", "NaN", "inf", "1e3", "1,000.00", "1.000,00", "-1", "2.345", "3.", "uno"] {
    do { _ = try Entrada.decimal(texto, campo: "Prueba"); fatalError("Parser aceptó \(texto)") }
    catch { verificaciones += 1 }
}
// Verificamos coma decimal, espacios, redondeo de medio centavo y neto negativo.
let coma = try Entrada.decimal("1234,56", campo: "Prueba")
let espacios = try Entrada.decimal(" 1234.56 ", campo: "Prueba")
comprobar(coma == d("1234.56"), "Coma decimal")
comprobar(espacios == d("1234.56"), "Espacios")
comprobar(Dinero.redondear(d("1.005")) == d("1.01"), "Mitad hacia arriba")
comprobar(Dinero.redondear(d("-1.005")) == d("-1.01"), "Mitad negativa")
var alto = base; alto.adelantos = 3000
let negativo = try Boleta().calcular(alto)
comprobar(negativo.neto == -825, "Neto negativo sin recorte artificial")
// Guardamos evidencia real que el script Python puede contrastar con el Excel.
let resultado: [String: Any] = ["checks": verificaciones, "cases": salida]
let json = try JSONSerialization.data(withJSONObject: resultado, options: [.prettyPrinted, .sortedKeys])
try json.write(to: URL(fileURLWithPath: "evidencias/swift_resultados.json"))
print("OK: \(verificaciones) comprobaciones; \(fixtures.count) casos. Ver evidencias/swift_resultados.json")
