import Foundation

public enum Dinero {
    public static func redondear(_ valor: Decimal) -> Decimal {
        var origen = valor
        var destino = Decimal()
        NSDecimalRound(&destino, &origen, 2, .plain)
        return destino
    }

    public static func texto(_ valor: Decimal) -> String {
        let formato = NumberFormatter()
        formato.locale = Locale(identifier: "es_PE")
        formato.numberStyle = .decimal
        formato.minimumFractionDigits = 2
        formato.maximumFractionDigits = 2
        return formato.string(from: NSDecimalNumber(decimal: valor)) ?? "0.00"
    }
}

public struct TasasAFP {
    public let fondo: Decimal
    public let comision: Decimal
    public let seguro: Decimal
    public init(_ fondo: String, _ comision: String, _ seguro: String) {
        self.fondo = Decimal(string: fondo)!
        self.comision = Decimal(string: comision)!
        self.seguro = Decimal(string: seguro)!
    }
}

public enum Parametros {
    // Perfil académico de Actividad_Grupo_B.docx; no sustituye una planilla legal.
    public static let rmv = Decimal(1230)
    public static let asignacion = Decimal(string: "0.10")!
    public static let onp = Decimal(string: "0.13")!
    public static let essalud = Decimal(string: "0.09")!
    public static let diasMes = Decimal(30)
    public static let horasDia = Decimal(8)
    public static let factor25 = Decimal(string: "1.25")!
    public static let factor35 = Decimal(string: "1.35")!
    // AFP reales: flujo, consulta SBS 2026-10-26. Solo Ejemplo para casos 1–4.
    public static let afps: [String: TasasAFP] = [
        "Ejemplo": TasasAFP("0.10", "0.016", "0.0135"),
        "Habitat (flujo)": TasasAFP("0.10", "0.0147", "0.0137"),
        "Integra (flujo)": TasasAFP("0.10", "0.0155", "0.0137"),
        "Prima (flujo)": TasasAFP("0.10", "0.0160", "0.0137"),
        "Profuturo (flujo)": TasasAFP("0.10", "0.0169", "0.0137")
    ]
    public static let nombresAFP = ["Ejemplo", "Habitat (flujo)", "Integra (flujo)", "Prima (flujo)", "Profuturo (flujo)"]
}

public enum Sistema: String, CaseIterable { case onp = "ONP", afp = "AFP" }

public struct DatosBoleta {
    public var sueldo: Decimal
    public var dias: Int
    public var hijos: Bool
    public var sistema: Sistema
    public var afp: String
    public var horas25: Decimal
    public var horas35: Decimal
    public var adelantos: Decimal
    public init(sueldo: Decimal, dias: Int, hijos: Bool, sistema: Sistema,
                afp: String = "Ejemplo", horas25: Decimal = 0, horas35: Decimal = 0, adelantos: Decimal = 0) {
        self.sueldo = sueldo; self.dias = dias; self.hijos = hijos; self.sistema = sistema
        self.afp = afp; self.horas25 = horas25; self.horas35 = horas35; self.adelantos = adelantos
    }
}

public struct Concepto {
    public let nombre: String
    public let monto: Decimal
}

public struct ResultadoBoleta {
    public let remuneraciones: [Concepto]
    public let descuentos: [Concepto]
    public let aportaciones: [Concepto]
    public var totalRemuneraciones: Decimal { remuneraciones.reduce(0) { $0 + $1.monto } }
    public var totalDescuentos: Decimal { descuentos.reduce(0) { $0 + $1.monto } }
    public var neto: Decimal { totalRemuneraciones - totalDescuentos }
    public var costoEmpleador: Decimal { totalRemuneraciones + aportaciones.reduce(0) { $0 + $1.monto } }
}

public struct ErrorEntrada: LocalizedError {
    public let mensaje: String
    public var errorDescription: String? { mensaje }
}

public enum Entrada {
    // Sin separadores de miles ni notación científica; admite punto o coma decimal.
    public static func decimal(_ texto: String, campo: String, maxDecimales: Int = 2) throws -> Decimal {
        let limpio = texto.trimmingCharacters(in: .whitespacesAndNewlines)
        let patron = "^[0-9]+([.,][0-9]{1,\(maxDecimales)})?$"
        guard limpio.range(of: patron, options: .regularExpression) != nil,
              let numero = Decimal(string: limpio.replacingOccurrences(of: ",", with: "."), locale: Locale(identifier: "en_US_POSIX")),
              !numero.isNaN else {
            throw ErrorEntrada(mensaje: "\(campo): ingresa un número sin miles, con hasta \(maxDecimales) decimales.")
        }
        return numero
    }

    public static func datos(sueldo: String, dias: String, hijos: Bool, sistema: Sistema,
                             afp: String, horas25: String, horas35: String, adelantos: String) throws -> DatosBoleta {
        guard let numeroDias = Int(dias.trimmingCharacters(in: .whitespacesAndNewlines)) else {
            throw ErrorEntrada(mensaje: "Días laborados: ingresa un entero entre 1 y 30.")
        }
        let datos = try DatosBoleta(sueldo: decimal(sueldo, campo: "Sueldo básico"), dias: numeroDias,
            hijos: hijos, sistema: sistema, afp: afp,
            horas25: decimal(horas25, campo: "Horas al 25%"),
            horas35: decimal(horas35, campo: "Horas al 35%"),
            adelantos: decimal(adelantos, campo: "Adelantos"))
        try Boleta.validar(datos)
        return datos
    }
}

public final class Boleta {
    public init() {}
    public static func validar(_ d: DatosBoleta) throws {
        guard !d.sueldo.isNaN, d.sueldo > 0, d.sueldo <= 100_000_000 else {
            throw ErrorEntrada(mensaje: "Sueldo básico: debe ser mayor que cero y no superar S/ 100,000,000.")
        }
        guard (1...30).contains(d.dias) else { throw ErrorEntrada(mensaje: "Días laborados: deben estar entre 1 y 30.") }
        for (nombre, valor, limite) in [("Horas al 25%", d.horas25, Decimal(10000)), ("Horas al 35%", d.horas35, Decimal(10000)), ("Adelantos", d.adelantos, Decimal(100_000_000))] {
            guard !valor.isNaN, valor >= 0, valor <= limite else {
                throw ErrorEntrada(mensaje: "\(nombre): ingresa un valor mayor o igual a cero, hasta \(limite).")
            }
            guard Dinero.redondear(valor) == valor else { throw ErrorEntrada(mensaje: "\(nombre): usa como máximo dos decimales.") }
        }
        guard Dinero.redondear(d.sueldo) == d.sueldo else { throw ErrorEntrada(mensaje: "Sueldo básico: usa como máximo dos decimales.") }
        guard d.sistema != .afp || Parametros.afps[d.afp] != nil else { throw ErrorEntrada(mensaje: "Selecciona una AFP válida.") }
    }

    public func calcular(_ d: DatosBoleta) throws -> ResultadoBoleta {
        try Self.validar(d)
        let r = Dinero.redondear
        // Valor hora conserva precisión: se redondea el concepto final, no este intermedio.
        let valorHora = d.sueldo / Parametros.diasMes / Parametros.horasDia
        let remuneraciones = [
            Concepto(nombre: "Sueldo computable", monto: r(d.sueldo / Parametros.diasMes * Decimal(d.dias))),
            Concepto(nombre: "Asignación familiar", monto: d.hijos ? r(Parametros.rmv * Parametros.asignacion) : 0),
            Concepto(nombre: "Horas extras 25%", monto: r(valorHora * Parametros.factor25 * d.horas25)),
            Concepto(nombre: "Horas extras 35%", monto: r(valorHora * Parametros.factor35 * d.horas35))
        ]
        let total = remuneraciones.reduce(Decimal(0)) { $0 + $1.monto }
        let tasas = Parametros.afps[d.afp]
        let descuentos = [
            Concepto(nombre: "ONP", monto: d.sistema == .onp ? r(total * Parametros.onp) : 0),
            Concepto(nombre: "AFP fondo", monto: d.sistema == .afp ? r(total * tasas!.fondo) : 0),
            Concepto(nombre: "AFP comisión", monto: d.sistema == .afp ? r(total * tasas!.comision) : 0),
            Concepto(nombre: "AFP seguro", monto: d.sistema == .afp ? r(total * tasas!.seguro) : 0),
            Concepto(nombre: "Adelantos", monto: d.adelantos)
        ]
        return ResultadoBoleta(remuneraciones: remuneraciones, descuentos: descuentos,
            aportaciones: [Concepto(nombre: "EsSalud (9%)", monto: r(total * Parametros.essalud))])
    }
}
