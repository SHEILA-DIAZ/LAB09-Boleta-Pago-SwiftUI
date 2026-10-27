import Foundation

// MODELO: contiene los datos y las reglas de cálculo, sin depender de SwiftUI.
// Por eso el mismo archivo sirve para la app de iOS y las pruebas de Windows.
// Foundation aporta Decimal, NumberFormatter y las herramientas de redondeo.

/// Utilidades para redondear los montos y darles formato al mostrarlos.
public enum Dinero {
    // Decimal trabaja con números decimales y evita muchos residuos típicos de
    // Double. Se redondea cada concepto por separado, antes de sumar los totales.
    public static func redondear(_ valor: Decimal) -> Decimal {
        var origen = valor
        var destino = Decimal()
        // NSDecimalRound escribe en destino. El & permite pasar la variable para
        // modificarla. Dos decimales y .plain: por ejemplo, 52.048 pasa a 52.05.
        NSDecimalRound(&destino, &origen, 2, .plain)
        return destino
    }

    // Esto solo cambia cómo se ve el importe: no calcula ni altera la boleta.
    public static func texto(_ valor: Decimal) -> String {
        let formato = NumberFormatter()
        formato.locale = Locale(identifier: "es_PE")
        formato.numberStyle = .decimal
        formato.minimumFractionDigits = 2
        formato.maximumFractionDigits = 2
        return formato.string(from: NSDecimalNumber(decimal: valor)) ?? "0.00"
    }
}

/// Un struct agrupa datos relacionados. Esta estructura contiene las tres tasas
/// de una AFP: ahorro para pensión, comisión de administración y prima de seguro.
public struct TasasAFP {
    public let fondo: Decimal
    public let comision: Decimal
    public let seguro: Decimal
    // init es el constructor: recibe las tasas como textos decimales exactos.
    // Los ! se usan solo con constantes controladas aquí, no con datos del usuario.
    public init(_ fondo: String, _ comision: String, _ seguro: String) {
        self.fondo = Decimal(string: fondo)!
        self.comision = Decimal(string: comision)!
        self.seguro = Decimal(string: seguro)!
    }
}

/// Todos los parámetros se reúnen aquí para no repetir tasas dentro de las fórmulas.
/// static permite consultarlos directamente, por ejemplo Parametros.rmv.
/// Fuentes y fecha de consulta: docs/fuentes.md y hoja Parámetros del Excel.
public enum Parametros {
    // Perfil académico de Actividad_Grupo_B.docx; no sustituye una planilla legal.
    public static let rmv = Decimal(1230)
    // Una tasa se expresa como fracción: 0.10 equivale a 10%; 0.13 equivale a 13%.
    public static let asignacion = Decimal(string: "0.10")!
    public static let onp = Decimal(string: "0.13")!
    public static let essalud = Decimal(string: "0.09")!
    public static let diasMes = Decimal(30)
    public static let horasDia = Decimal(8)
    // El factor incluye la hora normal más el recargo: 1 + 0.25 = 1.25.
    public static let factor25 = Decimal(string: "1.25")!
    public static let factor35 = Decimal(string: "1.35")!
    // AFP reales: flujo, consulta SBS 2026-10-26. Solo Ejemplo para casos 1–4.
    // Un diccionario relaciona una clave (nombre de AFP) con su valor (TasasAFP).
    // Por ejemplo, afps["Ejemplo"] permite buscar las tres tasas de prueba.
    public static let afps: [String: TasasAFP] = [
        "Ejemplo": TasasAFP("0.10", "0.016", "0.0135"),
        "Habitat (flujo)": TasasAFP("0.10", "0.0147", "0.0137"),
        "Integra (flujo)": TasasAFP("0.10", "0.0155", "0.0137"),
        "Prima (flujo)": TasasAFP("0.10", "0.0160", "0.0137"),
        "Profuturo (flujo)": TasasAFP("0.10", "0.0169", "0.0137")
    ]
    public static let nombresAFP = ["Ejemplo", "Habitat (flujo)", "Integra (flujo)", "Prima (flujo)", "Profuturo (flujo)"]
}

// Un enum limita las opciones a valores válidos. rawValue da el texto ONP o AFP.
public enum Sistema: String, CaseIterable { case onp = "ONP", afp = "AFP" }

/// Entradas numéricas listas para calcular. Decimal se usa para dinero y horas;
/// Int para días enteros, Bool para Sí/No y String para el nombre de la AFP.
public struct DatosBoleta {
    public var sueldo: Decimal
    public var dias: Int
    public var hijos: Bool
    public var sistema: Sistema
    public var afp: String
    public var horas25: Decimal
    public var horas35: Decimal
    public var adelantos: Decimal
    // Los valores predeterminados permiten omitir HE y adelantos cuando son cero.
    // self.sueldo es la propiedad de la estructura; sueldo es el argumento recibido.
    public init(sueldo: Decimal, dias: Int, hijos: Bool, sistema: Sistema,
                afp: String = "Ejemplo", horas25: Decimal = 0, horas35: Decimal = 0, adelantos: Decimal = 0) {
        self.sueldo = sueldo; self.dias = dias; self.hijos = hijos; self.sistema = sistema
        self.afp = afp; self.horas25 = horas25; self.horas35 = horas35; self.adelantos = adelantos
    }
}

/// Una fila de la boleta: por ejemplo, nombre = "ONP" y monto = 325.00.
public struct Concepto {
    public let nombre: String
    public let monto: Decimal
}

/// La salida del cálculo. [Concepto] significa un array o lista ordenada de filas.
/// Separamos aportaciones para evitar restar EsSalud del neto del trabajador.
public struct ResultadoBoleta {
    public let remuneraciones: [Concepto]
    public let descuentos: [Concepto]
    public let aportaciones: [Concepto]
    // Son propiedades calculadas: se obtienen al consultarlas, a partir de las filas.
    // reduce empieza en 0 y suma cada monto: $0 es el acumulado y $1 la fila actual.
    public var totalRemuneraciones: Decimal { remuneraciones.reduce(0) { $0 + $1.monto } }
    public var totalDescuentos: Decimal { descuentos.reduce(0) { $0 + $1.monto } }
    public var neto: Decimal { totalRemuneraciones - totalDescuentos }
    public var costoEmpleador: Decimal { totalRemuneraciones + aportaciones.reduce(0) { $0 + $1.monto } }
}

/// Error con un mensaje entendible para la persona que completa el formulario.
/// LocalizedError permite recuperarlo en la pantalla con localizedDescription.
public struct ErrorEntrada: LocalizedError {
    public let mensaje: String
    public var errorDescription: String? { mensaje }
}

/// Convierte el texto del formulario a datos numéricos antes de realizar operaciones.
public enum Entrada {
    // Sin separadores de miles ni notación científica; admite punto o coma decimal.
    public static func decimal(_ texto: String, campo: String, maxDecimales: Int = 2) throws -> Decimal {
        // Quitamos espacios al inicio y final. El patrón acepta solo dígitos y
        // un separador decimal opcional: "2500", "2500.50" o "2500,50".
        let limpio = texto.trimmingCharacters(in: .whitespacesAndNewlines)
        let patron = "^[0-9]+([.,][0-9]{1,\(maxDecimales)})?$"
        // guard exige que las condiciones sean verdaderas; si fallan, sale con error.
        // Normalizamos la coma a punto para convertir siempre con el mismo criterio.
        guard limpio.range(of: patron, options: .regularExpression) != nil,
              let numero = Decimal(string: limpio.replacingOccurrences(of: ",", with: "."), locale: Locale(identifier: "en_US_POSIX")),
              !numero.isNaN else {
            throw ErrorEntrada(mensaje: "\(campo): ingresa un número sin miles, con hasta \(maxDecimales) decimales.")
        }
        return numero
    }

    // Construye DatosBoleta con los textos de la pantalla. throws avisa que puede
    // fallar; quien llame a esta función debe usar try y manejar el error.
    public static func datos(sueldo: String, dias: String, hijos: Bool, sistema: Sistema,
                             afp: String, horas25: String, horas35: String, adelantos: String) throws -> DatosBoleta {
        guard let numeroDias = Int(dias.trimmingCharacters(in: .whitespacesAndNewlines)) else {
            throw ErrorEntrada(mensaje: "Días laborados: ingresa un entero entre 1 y 30.")
        }
        // Los controles TextField entregan textos; cada uno se convierte antes
        // de almacenarlo. Una entrada inválida interrumpe este paso inmediatamente.
        let datos = try DatosBoleta(sueldo: decimal(sueldo, campo: "Sueldo básico"), dias: numeroDias,
            hijos: hijos, sistema: sistema, afp: afp,
            horas25: decimal(horas25, campo: "Horas al 25%"),
            horas35: decimal(horas35, campo: "Horas al 35%"),
            adelantos: decimal(adelantos, campo: "Adelantos"))
        // Además de ser números, deben cumplir las reglas: sueldo positivo,
        // días entre 1 y 30 y horas/adelantos no negativos.
        try Boleta.validar(datos)
        return datos
    }
}

/// Calculadora de la boleta. Es una clase separada de la pantalla, como pide la guía.
/// final indica que no se crearán subclases que cambien este comportamiento.
public final class Boleta {
    public init() {}
    // La validación también pertenece al modelo: no depende de que la interfaz
    // haya revisado antes los datos. Así se protege cualquier llamada desde pruebas.
    public static func validar(_ d: DatosBoleta) throws {
        // isNaN detecta un Decimal que no representa un número válido. El máximo
        // es un límite técnico; la guía pide sueldo mayor que cero, no sueldo ≥ RMV.
        guard !d.sueldo.isNaN, d.sueldo > 0, d.sueldo <= 100_000_000 else {
            throw ErrorEntrada(mensaje: "Sueldo básico: debe ser mayor que cero y no superar S/ 100,000,000.")
        }
        guard (1...30).contains(d.dias) else { throw ErrorEntrada(mensaje: "Días laborados: deben estar entre 1 y 30.") }
        // Revisamos las tres entradas con reglas comunes en un mismo bucle.
        // Comparar con su valor redondeado detecta más de dos decimales significativos.
        for (nombre, valor, limite) in [("Horas al 25%", d.horas25, Decimal(10000)), ("Horas al 35%", d.horas35, Decimal(10000)), ("Adelantos", d.adelantos, Decimal(100_000_000))] {
            guard !valor.isNaN, valor >= 0, valor <= limite else {
                throw ErrorEntrada(mensaje: "\(nombre): ingresa un valor mayor o igual a cero, hasta \(limite).")
            }
            guard Dinero.redondear(valor) == valor else { throw ErrorEntrada(mensaje: "\(nombre): usa como máximo dos decimales.") }
        }
        guard Dinero.redondear(d.sueldo) == d.sueldo else { throw ErrorEntrada(mensaje: "Sueldo básico: usa como máximo dos decimales.") }
        // Solo exigimos una AFP existente cuando el sistema elegido es AFP.
        guard d.sistema != .afp || Parametros.afps[d.afp] != nil else { throw ErrorEntrada(mensaje: "Selecciona una AFP válida.") }
    }

    // Recibe los datos d y devuelve ResultadoBoleta; no modifica la pantalla.
    public func calcular(_ d: DatosBoleta) throws -> ResultadoBoleta {
        // PASO 1: detener el cálculo si alguna entrada no cumple las reglas.
        try Self.validar(d)
        // r es un nombre corto para la misma función Dinero.redondear.
        let r = Dinero.redondear
        // Valor hora conserva precisión: se redondea el concepto final, no este intermedio.
        let valorHora = d.sueldo / Parametros.diasMes / Parametros.horasDia
        // PASO 2: calcular y redondear cada remuneración antes de sumarlas.
        // La expresión condición ? valorSí : valorNo decide si corresponde asignación.
        let remuneraciones = [
            Concepto(nombre: "Sueldo computable", monto: r(d.sueldo / Parametros.diasMes * Decimal(d.dias))),
            Concepto(nombre: "Asignación familiar", monto: d.hijos ? r(Parametros.rmv * Parametros.asignacion) : 0),
            Concepto(nombre: "Horas extras 25%", monto: r(valorHora * Parametros.factor25 * d.horas25)),
            Concepto(nombre: "Horas extras 35%", monto: r(valorHora * Parametros.factor35 * d.horas35))
        ]
        // PASO 3: sumar el array. Esta es la base de ONP, AFP y EsSalud;
        // incluye la asignación familiar y las horas extras, no solo el sueldo.
        let total = remuneraciones.reduce(Decimal(0)) { $0 + $1.monto }
        // Buscar la AFP seleccionada devuelve un valor opcional (podría no existir).
        // validar ya comprobó que exista si se necesita para un descuento AFP.
        let tasas = Parametros.afps[d.afp]
        // PASO 4: calcular descuentos. Solo aplica ONP o AFP; el otro queda en cero.
        // Cada componente AFP se redondea por separado. El ! de tasas es seguro en
        // las ramas AFP después de validar; las ramas no elegidas no se ejecutan.
        // El adelanto se resta completo, pues ya fue validado con hasta dos decimales.
        let descuentos = [
            Concepto(nombre: "ONP", monto: d.sistema == .onp ? r(total * Parametros.onp) : 0),
            Concepto(nombre: "AFP fondo", monto: d.sistema == .afp ? r(total * tasas!.fondo) : 0),
            Concepto(nombre: "AFP comisión", monto: d.sistema == .afp ? r(total * tasas!.comision) : 0),
            Concepto(nombre: "AFP seguro", monto: d.sistema == .afp ? r(total * tasas!.seguro) : 0),
            Concepto(nombre: "Adelantos", monto: d.adelantos)
        ]
        // PASO 5: devolver los tres bloques. ResultadoBoleta obtiene los totales y
        // el neto. EsSalud se guarda aparte porque lo paga la empresa adicionalmente.
        return ResultadoBoleta(remuneraciones: remuneraciones, descuentos: descuentos,
            aportaciones: [Concepto(nombre: "EsSalud (9%)", monto: r(total * Parametros.essalud))])
    }
}
